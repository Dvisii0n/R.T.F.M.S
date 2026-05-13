import asyncio
import websockets
import json

async def test_client():
    uri = "ws://localhost:8080"
    async with websockets.connect(uri) as websocket:
        print("Connected to websocket")
        try:
            while True:
                message = await websocket.recv()
                print(f"Received: {message}")
        except:
            pass

asyncio.run(test_client())