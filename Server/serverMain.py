import sys

import threading

import os

sys.path.append(os.path.expanduser('~/Desktop/Def-Programming'))

#from Client.GUI.login_UI import loginUI

#from Client.GUI import mainGUI

from Server.events import events

from Server.mainPage import mainPage

from Server.pointsPage import pointsPage

from Server.server import DiffieHellmanServer

#from server import DiffieHellmanServer



def process_message(message):

    """Handles incoming messages and calls corresponding functions.""" 

    if ":" in message:

         usrNm, command=message.split(":", 1)

    else:

         usrNm, command =None, message

         

    print (f"Debug: Recieved request from user '{usrNm}' with command ''{command}") 



    process_messaged= str(command).replace(" ", "").lower()

    if process_messaged=="exit" or process_messaged=="5":

        return exit_server()

    

    if process_messaged=="events" or process_messaged=="4":

         return events.pageDisplay(usrNm)



    if process_messaged=="Points" or process_messaged=="3":

         return pointsPage.pageDisplay(usrNm)

    

    if process_messaged=="main" or process_messaged=="2":    

            return mainPage.pageDisplay(usrNm)

    

    if process_messaged=="menu"or process_messaged=="1":

         return menuDisplay()

    

    else: return "no option"



def menuDisplay():

     return "WELCOME TO THE FLORAL PRIATES\n"+" Options: \n[1]Menu\n[2]Main\n[3]Points\n[4]Events\n[5]Exit"



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