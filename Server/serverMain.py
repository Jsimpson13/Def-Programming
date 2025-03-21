import sys
import threading

sys.path.append('C:\\Users\\jsimp\\OneDrive\\Desktop\\Def-Programming')
#from Client.GUI.login_UI import loginUI
#from Client.GUI import mainGUI
from server import DiffieHellmanServer
from mainPage import mainPage
from loginPage import loginPage


def process_message(message):
    """Handles incoming messages and calls corresponding functions."""  
    if message=="exit":
        return exit_server()
    if message=="main page":    
            """threading.Thread(target=mainGUI().run, daemon=True).start()
            return "main page"""
            return mainPage.pageDisplay()
    else: return "no option"


def exit_server():
    return 

def server_status():
    """Returns server status."""
    return "Server is running and healthy."

def mainServer():
    """Starts the server and forwards messages to `process_message`."""
    Server = DiffieHellmanServer()
    Server.start()
    Server.handle_messages(process_message)

if __name__ == "__main__":
    mainServer()
