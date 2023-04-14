import asyncio
import websockets

### Websocket server ###
### It is used to send the announcements to the clients ###
### @deprecated: It is not used anymore, we use a js websockets server now ###

# Set up a set to store the connected clients
clients = set()

async def handle_message(message, sender):
    # Iterate through the connected clients and send the message to all except the sender
    for client in clients:
        # if client != sender:
        await client.send(message)

async def handle_client(websocket, path):
    # Add the websocket to the clients set
    clients.add(websocket)

    try:
        while True:
            # Wait for incoming messages from the client
            message = await websocket.recv()
            print(message)
            # Handle the message (e.g., broadcast to other clients)
            await handle_message(message, websocket)

    finally:
        # Remove the websocket from the clients set when the connection is closed
        clients.remove(websocket)

start_server = websockets.serve(handle_client, 'localhost', 8080)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
