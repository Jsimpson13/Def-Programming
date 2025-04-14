from pathlib import Path
import sys
project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))
from Server import Db

class pointsPage:

    #View Points
    def viewPoints(currUser):
        retpoints= Db.checkPoints(currUser)
        if not retpoints: 
             return "User not not found or no profile exists"
        retpoints=retpoints[0]
        #points=retpoints[0]    
        return retpoints
    
    #Add Points
    def addPoints(currUser):
        while(True):
                addpoint=input("Enter the amount of points you want to add: ")
                if addpoint.isdigit():
                     Db.addPoints(currUser, addpoint)
                     return(addpoint+" points added!")
                     break
                else:
                    return("Please enter a whole number or 0")
    # return a displayable 


    def pageDisplay(currUser):
        print("Floral Pirates Hockey\n      POINTS PAGE")
        print(currUser+"'s points: ", pointsPage.viewPoints(currUser))
        #pointsPage.addPoints(currUser)
        #("Press 1 or enter menu to return to the menu")