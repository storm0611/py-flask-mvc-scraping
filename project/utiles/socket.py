import websockets
import asyncio

from websockets.server import WebSocketServer

class MyWebSocketServer(WebSocketServer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    

# server = WebSocketServer("localhost", 8001)
# server.serve_forever()

# async def socket(websocket, path):
#     name = await websocket.recv()
#     print(f"Received message from {name}")
#     greeting = f"Hello {name}!"
#     await websocket.send(greeting)
#     print(f"Sent message to {name}")

# async def main():
#     async with websockets.serve(socket, "localhost", 8001):
#         print("Socket Server started")
#         await asyncio.Future()  # Run forever

# asyncio.run(main())