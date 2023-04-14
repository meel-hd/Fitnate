import socket
from tkinter import messagebox

"""Check if the network is available, if not, ask the user to retry or cancel"""

def check_network():
    while True:
        try:
            socket.create_connection(
                address=("www.google.com", 80), timeout=1 # checkig if google is reachable
            )
            return True # Network is available
        except OSError:
            retry = messagebox.askretrycancel("Network Error", "Check your network,\n and retry to continue")
            if not retry:
                return False