import requests
import threading
import time
import customtkinter

from config import target

### Responsible for sending requests to the target server ###
### and displaying the results in the GUI (logs- seeds-frame) ###

count = 0 # Seeds count (requests sent)
next_delete = 1 # Track when to clear the frame

def send_request(target_frame,sleep_time,clear_at,seed_count_label):
    global count
    global next_delete
    while not stop_event.is_set():
        try:
            # Send request
            response = requests.get(target)
            count += 1
            seed_count_label.configure(text=f'{count} seed')
            if (count / clear_at == next_delete):
                label = customtkinter.CTkLabel(target_frame, text='Clearing Seeds History...', text_color='yellow')
                label.pack()
                # Clear the frame
                for widget in target_frame.winfo_children():
                    # Error sometimes occurs when the frame is cleared 
                    widget.destroy()
                next_delete += 1
                label = customtkinter.CTkLabel(target_frame, text=f'Cleared at seed {count}', text_color='yellow')
                label.pack()
            # show logs
            if response.status_code < 300: # Successfull request
                label = customtkinter.CTkLabel(target_frame, text="Seed {}: Success".format(count), text_color="#30E399") # Add Labe to status Frame
            else:
                label = customtkinter.CTkLabel(target_frame, text="Seed {}: Failed: {}.".format(count, response.status_code), text_color="red") # Add Labe to status Frame
            label.pack()
        
        except requests.exceptions.RequestException as e:
            # Handle request exceptions
            error_message = str(e)[:20] + "..." if len(str(e)) > 100 else str(e)  # Truncate error message to max length of 100 characters
            label = customtkinter.CTkLabel(target_frame, text="Seed {}: Failed: {}. Retrying".format(count, error_message), text_color="violet") # Add Labe to status Frame
            label.pack()
        
        if sleep_time > 0:
            label = customtkinter.CTkLabel(target_frame, text="Sleeping {} sec.".format(sleep_time))
            label.pack()
            time.sleep(sleep_time)

def start_requests(target_frame, sleep_time, clear_at, seed_count_label):
    print("Sending requests...")
    global stop_event
    stop_event = threading.Event()
    # Start requests in a separate thread
    thread = threading.Thread(target=send_request,args=(target_frame,sleep_time, clear_at,seed_count_label))
    thread.start()

def stop_requests():
    print("Stopping requests...")
    stop_event.set()

if __name__ == "__main__":
    start_requests()
