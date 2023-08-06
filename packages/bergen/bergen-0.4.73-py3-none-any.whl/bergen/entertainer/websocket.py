
from bergen.clients.base import BaseBergen
from websockets.exceptions import ConnectionClosedError
from bergen.messages.base import MessageModel
from bergen.messages.utils import expandToMessage
import json
from bergen.entertainer.base import BaseEntertainer
import logging
import asyncio
import websockets
from bergen.console import console
import asyncio
from bergen.legacy.utils import create_task


logger = logging.getLogger()





class WebsocketEntertainer(BaseEntertainer):
    ''' Is a mixin for Our Bergen '''

    def __init__(self, client: BaseBergen, **kwargs) -> None:
        super().__init__(client, **kwargs)
        self.websocket_host = client.config.host
        self.websocket_port = client.config.port
        self.websocket_protocol = "wss" if client.config.secure else "ws"
        
        self.auto_reconnect= True
        self.allowed_retries = 2
        self.current_retries = 0

    async def connect(self):
        self.incoming_queue = asyncio.Queue()
        self.outgoing_queue = asyncio.Queue()
        self.tasks = []

        self.startup_task = create_task(self.startup())

    async def disconnect(self) -> str:
        for reference, task in self.assignments.items():
            if not task.done():
                logger.info(f"Cancelling Assignment {task}")
                task.cancel()

        if self.connection: await self.connection.close()

        if self.pending:
            for task in self.pending:
                task.cancel()

        logger.info("Entertainer disconnected")

        
    async def startup(self):
        try:
            await self.connect_websocket()
        except Exception as e:

            logger.error(f"[red] Connection attempt as Entertainer failed")
            self.current_retries += 1
            if self.auto_reconnect:
                sleeping_time = (self.current_retries + 1)
                console.print(f"[red] Trying to Reconnect as Entertainer in {sleeping_time} seconds")
                await asyncio.sleep(sleeping_time)
                await self.startup()
            else:
                console.print("[red] Entertainer: No reconnecting attempt envisioned. Shutting Down!")
                console.print_exception()

        console.print("[red] Successfully established Entertainer Connection")

        self.consumer_task = create_task(
            self.consumer()
        )

        self.producer_task = create_task(
            self.producer()
        )

        self.worker_task = create_task(
            self.workers()
        )

        done, self.pending = await asyncio.wait(
            [self.consumer_task, self.worker_task, self.producer_task],
            return_when=asyncio.FIRST_EXCEPTION
        )

        logger.error(f"Lost connection inbetween everything :( {[ task.exception() for task in done]}")
        logger.error(f'Reconnecting')

        try:
            for task in done:
                if task.exception():
                    raise task.exception()
                    
        except ConnectionClosedError:
            console.print("[red] Entertainer Connection was closed. Trying Reconnect")
        except:
            console.print_exception()
            

        for task in self.pending:
            task.cancel()

        if self.connection: await self.connection.close()
        self.current_retries = 0 # reset retries after one successfull connection
        await self.startup() # Attempt to ronnect again
        

    async def connect_websocket(self):
        try:
            uri = f"{self.websocket_protocol}://{self.websocket_host}:{self.websocket_port}/entertainer/?token={self.client.auth.access_token}"
            self.connection = await websockets.client.connect(uri)
        except:
            #TODO: Better TokenExpired Handling
            self.client.auth.refetch()
            uri = f"{self.websocket_protocol}://{self.websocket_host}:{self.websocket_port}/entertainer/?token={self.client.auth.access_token}"
            self.connection = await websockets.client.connect(uri)

        logger.info("Sueccess fully connected Provider ")


    async def consumer(self):
        logger.warning(" [x] Awaiting Entertaining Calls")
        async for message in self.connection:
            await self.incoming_queue.put(message)

    async def producer(self):
        while True:
            message = await self.outgoing_queue.get()
            await self.connection.send(message.to_channels())

            self.outgoing_queue.task_done()

    async def forward(self, message: MessageModel):
        await self.outgoing_queue.put(message)


    async def workers(self):
        while True:
            message_str = await self.incoming_queue.get()
            message = expandToMessage(json.loads(message_str))
            logger.info(f"Received Message {message}")
            await self.on_message(message)
            self.incoming_queue.task_done()


    


    
    

