import asyncio
import websockets

### Websocket client ###
### It is used to send the announcements and admin messages to clients ###

# @deprecated: It is going to be replaced by a web client

### Commands ###
# Admin: send message to users as an admin
# Announcement: send message to users as an announcement

async def send_message(websocket, message):
    await websocket.send(message)

async def receive_message(websocket):
    message = await websocket.recv()
    return message

async def main():
    # Connect to the WebSocket server
    async with websockets.connect('ws://localhost:8080/') as websocket:
        while True:
            # Send a message to the server
            message_to_send = input("message: ")
            await send_message(websocket, message_to_send)

            # Receive messages from the server
            message_received = await receive_message(websocket)
            print(message_received)

asyncio.get_event_loop().run_until_complete(main())
