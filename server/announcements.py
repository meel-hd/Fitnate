import threading
import asyncio
import websockets
import customtkinter
import socket

from config import websocket_url

### Handles the websocket connection to the server ###
### and displays the messages in the GUI ###
### The messages are displayed in the messages_frame ###
### We use a separate thread to run the event loop ###


async def connect_to_websocket_server(messages_frame):
    # Clear the connecting to the server message
    for label in messages_frame.winfo_children():
        label.destroy()
    connecting_message = customtkinter.CTkLabel(messages_frame, text="Connecting to the server...", text_color="orange")
    connecting_message.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    # Connect to the websocket server
    try:
        websocket = await websockets.connect(websocket_url)
    except ConnectionRefusedError:
        print("Failed to connect to the server")
        # Clear the connecting to the server message
        for label in messages_frame.winfo_children():
            label.destroy()
            
        inform_label = customtkinter.CTkLabel(messages_frame, text="Failed to connect to the server", text_color="red")
        inform_label.grid(row=1, column=0, padx=10, pady=10)
        retry_button = customtkinter.CTkButton(messages_frame, text="Retry", command=lambda: start_the_feed(messages_frame))
        retry_button.grid(row=2, column=0, padx=10, pady=10)
        return
    finally:
        # Send a message to the server
        my_ip_address = socket.gethostbyname(socket.gethostname())
        await websocket.send(my_ip_address + " has joined")
        # Clear the connecting message
        for label in messages_frame.winfo_children():
            label.destroy()
    try:        
        while not stop_event.is_set():
            # Receive messages from the server
            message = await websocket.recv()
            message = message.decode("utf-8")
            sender = "Anonymous"
            sender_color = "yellow"
            
            # Check if the message is from the admin
            if message.startswith("Admin:"):
                sender = "Admin"
                message = message[6:]
                sender_color = "red"
            # Check if the message is an announcement
            if message.startswith("Announcement:"):
                sender = "Announcement"
                message = message[13:]
                sender_color = "violet"
            # Display the message with the sender
            sender_label = customtkinter.CTkLabel(
                    master=messages_frame, text=f'{sender}' , 
                    text_color=sender_color,
                )
            sender_label.pack(anchor='w', padx=10,)
            # Separate the message into small chunks
            for i in range(0, len(message), 80):
                # show the current 80 characters
                message_chunk = message[i:i+80]
                message_label = customtkinter.CTkLabel(master=messages_frame, text=message_chunk)
                message_label.pack(anchor='w',padx=20,)
            # Separation between messages
            separation_label = customtkinter.CTkLabel(master=messages_frame, text='')
            separation_label.pack()
    except websockets.exceptions.ConnectionClosed:
        print("Disconnected from the server")
        # Clear the connecting to the server message
        for label in messages_frame.winfo_children():
            label.destroy()
            
        inform_label = customtkinter.CTkLabel(messages_frame, text="Disconnected from the server", text_color="red")
        inform_label.grid(row=1, column=0, padx=10, pady=10)
        retry_button = customtkinter.CTkButton(messages_frame, text="Retry", command=lambda: start_the_feed(messages_frame))
        retry_button.grid(row=2, column=0, padx=10, pady=10)
        return

def start_the_feed(messages_frame):
    print("Starting the feed in separate thread...")
    global stop_event
    stop_event = threading.Event()

    # Create and run an event loop in a separate thread
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=loop.run_forever)
    t.start()

    # Run the coroutine in the event loop
    asyncio.run_coroutine_threadsafe(connect_to_websocket_server(messages_frame), loop=loop)
    
    def stop_feed():
            print("Stopping the feed thread...")
            stop_event.set()

            # Stop the event loop
            loop.stop()
        
    return stop_feed

if __name__ == "__main__":
    start_the_feed()
