import sys
import os
#sys.path.append('C:\\Users\\jsimp\\OneDrive\\Desktop\\Def-Programming')
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from Server.Db import checkEvents, checkProfile




class mainPage:
    
    def getUser():
        from Server import serverMain
        usr=serverMain.getloggedinUser()
        profileData=checkProfile(serverMain.username)[0]
        print(profileData)
        if profileData:
            USERNAME = profileData[0]
            POINTS = profileData[4]
            return 'User: '+str(USERNAME)+'\n'+'Number of Points: '+str(POINTS)+'\n'
        else: return "User not Found"

    def getEvents():
        evntStr=""
        eventData=checkEvents()
        if eventData:
            for event in eventData:
                name=event[0]
                cost=event[1]
                evntStr+= name+" Cost per ticket: "+str(cost)+" points\n"
            return evntStr
        else: return "No events"    
            
    def pageDisplay():    
       return """\nWELCOME TO THE FLORAL PRIATES MainPage\n"""+mainPage.getUser()+mainPage.getEvents()

if __name__ == "__main__":
    
    print(mainPage.pageDisplay())
