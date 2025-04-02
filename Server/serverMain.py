import sys
import threading
sys.path.append('C:\\Users\\jsimp\\OneDrive\\Desktop\\Def-Programming')
#from Client.GUI.login_UI import loginUI
#from Client.GUI import mainGUI
from Server.mainPage import mainPage
from Server.server import DiffieHellmanServer
#from server import DiffieHellmanServer

username="Bob123"

def getloggedinUser():
     return username

def setloggedinUser(newusr):
     username=newusr
     return username

def process_message(message):
    """Handles incoming messages and calls corresponding functions.""" 
    process_messaged= str(message).replace(" ", "").lower()
    if process_messaged=="exit" or process_messaged=="3":
        return exit_server()
    if process_messaged=="main" or process_messaged=="2":    
            """threading.Thread(target=mainGUI().run, daemon=True).start()
            return "main page"""
            return mainPage.pageDisplay()
    if process_messaged=="menu"or process_messaged=="1":
         return menuDisplay()
    else: return "no option"

def menuDisplay():
     return "WELCOME TO THE FLORAL PRIATES\n"+" Options: \n[1]Menu\n[2]Main\n[3]Exit\n"

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
