import sys
sys.path.append('C:\\Users\\jsimp\\OneDrive\\Desktop\\Def-Programming')


class mainPage:

    def getUser():
        return "John Doe" #when we meet we need to discus this
    def getPoints():
        return "3000 points"
    def getEvents():
        return "Event 1 \nEvent 2\nEvent 3 \n"

    def pageDisplay():    
       return """\nWELCOME TO THE FLORAL PRIATES TICKET PAGE\n"""+'User: '+mainPage.getUser()+'\n'+'Number of Points: '+mainPage.getPoints()+'\n'+'UPCOMING EVENTS: '+mainPage.getEvents()+'\n'

if __name__ == "__main__":
    mainPage.pageDisplay()

