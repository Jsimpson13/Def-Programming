from pathlib import Path
import sys
project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))
from Server.Db import checkPurchases, checkProfile



class mainPage:
    
    def getUser(currUser):
        print(f"Debug: Current user -> {currUser}")  # Print for debugging
        
        profileData = checkProfile(currUser)
        print(f"Debug: checkProfile() returned {profileData}")  # Print what DB returns
        
        if not profileData:  # If the list is empty
            return "User not found or no profile exists."

        profileData = profileData[0]  # Now safe to access [0]
        print(profileData)  # Debugging output

        USERNAME = profileData[0]
        POINTS = profileData[4]
        return f'User: {USERNAME}\nNumber of Points: {POINTS}\n'


    def getEvents(currUser):
        evntStr=""
        eventData=checkPurchases(currUser)
        if eventData:
            for event in eventData:
                name=event[0]
                cost=event[1]
                evntStr+= name+" Cost per ticket: "+str(cost)+" points\n"
            return evntStr
        else: return "No events"    
            
    def pageDisplay(currUser):    
       return """\nWELCOME TO THE FLORAL PRIATES MainPage\n"""+mainPage.getUser(currUser)+mainPage.getEvents(currUser)

if __name__ == "__main__":
    
    print(mainPage.pageDisplay())
