import asyncio
import base64
import json
import sys
import websockets
import ssl
import requests

async def twilo_handler(twilio_ws):
    streamsid_queue = asyncio.Queue()

    async def twilo_receiver(twilio_ws):
        async for message in twilio_ws:
            try:
                data = json.loads(message)

                if data["event"] == "start":
                    streamsid_queue.put_nowait(data["start"]["streamsSid"])
            except:
                break
    
    async def twilio_sender(twilio_ws):
        print("twilio_sender started")

        # wait to recieve the streamsid for this connection from one of Twilio's messages
        streamsid = await streamsid_queue.get()

        