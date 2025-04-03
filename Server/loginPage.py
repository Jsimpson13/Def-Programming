import getpass
import sys
sys.path.append('C:\\Users\\jsimp\\OneDrive\\Desktop\\Def-Programming')
from Server import Db, serverMain


class loginPage:
    def loggedin(max_attempts=5):
        attempts = 0
        while attempts < max_attempts:
            user = input("Please Input Username: ")
            pwd = getpass.getpass("Please Input Password: ")
            try:
                result = Db.checkLoginCreds(user, pwd)
            except Exception as e:
                print("An error has occurred", e)
                return False
            
            if result:
                print("Login successful!")
                print("Welcome " + user)
                return user
            else:
                attempts += 1
                remaining = max_attempts - attempts
                print(f"Wrong login credentials. Attempts left: {remaining}")
        
        print("Too many failed login attempts. Access denied")
        return ""

    def addUser():
        usr=input("Enter Username: ")
        psw=input("Enter Password: ")
        name=input("Enter your Name: ")
        pnum=input("Enter your Phone Number: ")
        try:
            Db.addProfile(usr,psw,name,pnum)
            print("Welcome "+ usr)
            return usr
        except Exception as e:
            print("Error adding New User: ",e )
        
                