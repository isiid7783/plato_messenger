import asyncio
import websockets
import json
from crypto import decrypt

peers = set()

async def handler(websocket):
    peers.add(websocket)
    try:
        async for message in websocket:
            for peer in peers:
                if peer != websocket:
                    await peer.send(message)
    finally:
        peers.remove(websocket)

async def start_server(port=8765):
    return await websockets.serve(handler, "0.0.0.0", port)

async def connect_and_send(uri, payload):
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps(payload))
