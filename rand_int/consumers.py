from channels.generic.websocket import AsyncWebsocketConsumer
from random import randint
import asyncio
import json

class IntConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        await self.accept()

        while 1:
            await self.send(json.dumps({
                'int': randint(1,100)
            }))

            await asyncio.sleep(1)