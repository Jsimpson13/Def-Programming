# Handles points system for users
# Viewing and adding points


import sys

import os

sys.path.append(os.path.expanduser('~/Desktop/Def-Programming'))



from Server import Db



class pointsPage:

    #Retrieves current user's points from the database
    def viewPoints(currUser):

        retpoints= Db.checkPoints(currUser)

        if not retpoints: 

             return "User not not found or no profile exists"

        retpoints=retpoints[0]

        #points=retpoints[0]    

        return retpoints

    

    #Adds a user-specified number of points to the current user's profile
    def addPoints(currUser):

        while(True):

                addpoint=input("Enter the amount of points you want to add: ")

                Db.addPoints(currUser, addpoint)

                return (addpoint + " points added!\n")


                break

                return("Please enter a whole number or 0")
        print("\nWELCOME TO THE FLORAL PIRATES\nOptions:") 




    # Displays the user's current points
    def pageDisplay(currUser):

        print("Floral Pirates Hockey\n      POINTS PAGE")

        print(currUser+"'s points: ", pointsPage.viewPoints(currUser))

        #pointsPage.addPoints(currUser)

        #("Press 1 or enter menu to return to the menu")
