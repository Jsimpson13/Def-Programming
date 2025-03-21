import sys
sys.path.append('C:\\Users\\jsimp\\OneDrive\\Desktop\\Def-Programming')

class loginPage:
    
    def login():
        user=input("Please Input Username: ")
        while True: 
            if (user=="John"):
                #this needs to be changed to look through the user names of the db
                psd=input("Please Input Password: ")
                if (psd=="JohnDoe123"):
                    return True
                    break
            print("Please put in valid input")
