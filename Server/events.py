import sys

import getpass

import os

sys.path.append(os.path.expanduser('~/Desktop/Def-Programming'))



from Server import Db





class events: 


# Retrieves event names and ticket costs from the database
# Formats them into a string
    def getEvents():

        evntStr=""

        eventData=Db.checkEvents()

        if eventData:

            for event in eventData:

                name=event[0]

                cost=event[1]

                evntStr+= name+" Cost per ticket: "+str(cost)+" points\n"

            return evntStr

        else: return "No events"   

    

    
# Prompts user to buy a ticket and processes the purchase through the database
    def buyEvnt(currUser):

        choice=str(input("Do you want to buy a ticket: ")).replace(" ","").lower()

        if choice=="n" or choice=="no":

            print("ok thank you")

        if choice=="y"or choice=="yes":

            eventname=input("Please provide the event name:  ")

            try: 

                Db.buyTickets(currUser,eventname)

                

            except Exception as e:

                print("error: ",e)

            """else:

                print("no event found")

            finally: 

                print("WELCOME TO THE FLORAL PRIATES\n"+" Options: \n[1]Menu\n[2]Main\n[3]Points\n[4]Events\n[5]Exit")"""




# Displays the list of events and prompts the user to buy a ticket
    def pageDisplay(currUser):

        print( events.getEvents())

        events.buyEvnt(currUser)


