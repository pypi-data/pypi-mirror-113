import asyncio
from abc import ABC, abstractmethod
from asyncio.futures import Future
from bergen.messages.postman.log import LogLevel
from bergen.handlers.unprovide import UnprovideHandler
from bergen.clients.base import BaseBergen
from bergen.handlers.base import Connector
from bergen.messages import *
from bergen.hookable.base import Hookable
import logging
from typing import Dict, Type
from bergen.models import Pod
from bergen.actors.base import Actor
from functools import partial
from bergen.console import console
from bergen.legacy.utils import create_task



logger = logging.getLogger(__name__)

class ProtocolError(Exception):
    pass

class TaskAlreadyDoneError(ProtocolError):
    pass




class BaseEntertainer(Hookable):
    ''' Is a mixin for Our Bergen '''
    def __init__(self, client: BaseBergen, raise_exceptions_local=False, loop=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.provisions = {}
        self.raise_exceptions_local = raise_exceptions_local
        self.loop = loop or client.loop or asyncio.get_event_loop()
        self.client = client

        self.connector = Connector(self)

        self.template_id_actorClass_map: Dict[str, Type[Actor]] = {}

        self.provision_actor_map: Dict[str, Actor] = {}
        self.provision_actor_run_map: Dict[str, asyncio.Task]= {}
        self.provision_actor_queue_map: Dict[str, asyncio.Queue] = {}


        self.unprovide_futures: Dict[str, Future] = {}
        self.provide_futures: Dict[str, Future] = {}

        self.all_pod_assignments = {}
        self.all_pod_reservations = {}

        self.entertainments = {}
        self.assignments = {}

        self.pending = []

        self.tasks = []

    @abstractmethod
    async def connect(self) -> str:
        raise NotImplementedError("Please overwrite")

    @abstractmethod
    async def disconnect(self) -> str:
        raise NotImplementedError("Please overwrite")

    @abstractmethod
    async def activateProvision(self):
         raise NotImplementedError("Please overwrite")

    @abstractmethod
    async def deactivateProvision(self):
         raise NotImplementedError("Please overwrite")

    @abstractmethod
    async def forward(self, message: MessageModel):
        raise NotImplementedError("Overwrite this in your Protocol")


    async def on_message(self, message: MessageModel):
        
        if isinstance(message, ProvideDoneMessage): 
            # As we send the Activate Provide request to the Platform we will get a Return Statement
            logger.info("Arkitekt acknowledged the creation of a Pod for our Actor [this has no consequences??]")
            self.provide_futures[message.meta.reference].set_result(message.data.pod)

        elif isinstance(message, UnprovideDoneMessage): 
            # As we send the Activate Provide request to the Platform we will get a Return Statement
            logger.info("Arkitekt acknowledged the deletion of the Pod our our former Actor")
            self.unprovide_futures[message.meta.reference].set_result(message.data)


        elif isinstance(message, BouncedForwardedAssignMessage):
            assert message.data.provision is not None, "Received assignation that had no Provision???"
            assert message.data.provision in self.provision_actor_queue_map, f"Provision not entertained {message.data.provision} {self.provision_actor_queue_map}"
            await self.provision_actor_queue_map[message.data.provision].put(message)
            self.all_pod_assignments[message.meta.reference] = message.data.provision # Run in parallel

        elif isinstance(message, BouncedUnassignMessage):
            if message.data.assignation in self.all_pod_assignments: 
                logger.info("Cancellation for task received. Canceling!")
                hosting_provising = self.all_pod_assignments[message.data.assignation]
                await self.provision_actor_queue_map[hosting_provising].put(message)
            else:
                logger.error("Received Cancellation for Assignation that is not running with us. Sending Done back..")
                unassign_done = UnassignDoneMessage(data={
                    "assignation": message.data.assignation
                }, meta={"extensions": message.meta.extensions, "reference": message.meta.reference})
                await self.forward(unassign_done)

        else:
            logger.error(f"This Message shouldn't apear in the entertainer {message}")

                


    async def deactivateProvision(self, bounced_unprovide: BouncedUnprovideMessage):
        # Where should we do this?
        future = self.loop.create_future()
        self.unprovide_futures[bounced_unprovide.meta.reference] = future
        await self.forward(bounced_unprovide)
        reference = await future # is just a loopback??
        return reference

    async def activateProvision(self, bounced_provide: BouncedProvideMessage):
        
        #We are forwarding the Provision to Arkitekt and wait for its acknowledgement of the creation of this Pod
        future = self.loop.create_future()
        self.provide_futures[bounced_provide.meta.reference] = future
        await self.forward(bounced_provide)
        id = await future
        pod = await Pod.asyncs.get(id=id)
        return pod

    
    def actor_cancelled(self, actor: Actor, future: Future):
        logger.info("Actor is done! Cancellation or Finished??")
        if future.cancelled():
            logger.info("Future was cancelled everything is cools")


    async def get_actorclass_for_template(self, template_id):
        assert template_id in self.template_id_actorClass_map, "We have no Actor stored in our list"
        return self.template_id_actorClass_map[template_id]


    def registerActor(self, template_id: str, actorClass: Type[Actor]):
        assert template_id not in self.template_id_actorClass_map, "We cannot register two Actors for the same template on the same provider"
        self.template_id_actorClass_map[template_id] = actorClass


    async def unentertain(self, bounced_unprovide: BouncedUnprovideMessage):
        unprovide_handler = UnprovideHandler(bounced_unprovide, self.connector)

        try:
            provision_reference = bounced_unprovide.data.provision 
            assert provision_reference in self.provision_actor_run_map, "We dont entertain this provision"
            task = self.provision_actor_run_map[provision_reference]

            if not task.done():
                await unprovide_handler.pass_log("Cancelling", level=LogLevel.INFO)
                task.cancel()
                await unprovide_handler.pass_done()
            else:
                raise TaskAlreadyDoneError("Task was already done")

            
        except ProtocolException as e:
            console.print_exception()
            await unprovide_handler.pass_error(e)
        except Exception as e:
            console.print_exception()
            await unprovide_handler.pass_critical(e)
        
        
        # THIS Comes form the Arkitekt Platform

    
    async def entertain(self, bounced_provide: BouncedProvideMessage, actorClass: Type[Actor]):
        ''' Takes an instance of a pod, asks arnheim to activate it and accepts requests on it,
        cancel this task to unprovide your local implementatoin '''
        provision_reference = bounced_provide.meta.reference # We register Actors unter its provision
        actor = actorClass(self.connector)

        try:
            self.provision_actor_map[provision_reference] = actor
            self.provision_actor_queue_map[provision_reference] = actor.queue
            run_task = create_task(actor.run(bounced_provide))
            run_task.add_done_callback(partial(self.actor_cancelled, actor))
            self.provision_actor_run_map[provision_reference] = run_task

        except Exception as e:
            logger.error("We have a provision error")
            logger.error(e)
            # This error gets passed back to the provider
            raise e


