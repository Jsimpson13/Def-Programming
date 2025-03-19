import sys
import threading
sys.path.append('C:\\Users\\jsimp\\OneDrive\\Desktop\\Def-Programming')
from Client.GUI.loginUI import LoginUI
import server

def process_message(message):
    """Handles incoming messages and calls corresponding functions."""  
    if message=="exit":
        return exit_server()
    if message=="main page":
        return main_page()
    if message=="login":
        threading.Thread(target=LoginUI().run, daemon=True).start()
        return "login"
    else: return "no option"


def exit_server():
    return 
def main_page():
    """Function triggered when client sends 'main page'."""
    return "You are on the main page."

def server_status():
    """Returns server status."""
    return "Server is running and healthy."

def mainServer():
    """Starts the server and forwards messages to `process_message`."""
    Server = server.DiffieHellmanServer()
    Server.start()
    Server.handle_messages(process_message)

if __name__ == "__main__":
    mainServer()
