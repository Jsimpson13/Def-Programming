import getpass
import sys
sys.path.append('C:\\Users\\jsimp\\OneDrive\\Desktop\\Def-Programming')
from Server import Db

class loginPage:
    
    def loggedin(max_attempts=5):
        attempts=0
        while attempts<max_attempts:
            user=input("Please Input Username: ")
            pwd=getpass.getpass("Please Input Password: ")
            try:
                result= Db.checkLoginCreds(user, pwd)
            except Exception as e:
                print("An error has occured", e)
                return False
            
            if  result: 
                print("Login successful!")
                return True
            else: 
                attempts+=1
                remaining=max_attempts-attempts
                print("Wrong login credentials. Attempts left: ", remaining)
                
        print ("Too many failed login attempts. Access denied")
        return False
                