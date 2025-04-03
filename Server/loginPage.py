import getpass
import sys
import os
#sys.path.append('C:\\Users\\jsimp\\OneDrive\\Desktop\\Def-Programming')
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
from Server import Db, serverMain

class loginPage:
    #username="" #this is not being reset
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
                serverMain.username=user#serverMain.setloggedinUser(user)
                print("Welcome "+serverMain.getloggedinUser())
                return True
            else: 
                attempts+=1
                remaining=max_attempts-attempts
                print("Wrong login credentials. Attempts left: ", remaining)    
        print ("Too many failed login attempts. Access denied")

    def addUser():
        usr=input("Enter Username: ")
        psw=input("Enter Password: ")
        name=input("Enter your Name: ")
        pnum=input("Enter your Phone Number: ")
        try:
            Db.addProfile(usr,psw,name,pnum)
            loginPage.username=usr
            print("Welcome "+ name)
            
        except Exception as e:
            print("Error adding New User: ",e )
        
                