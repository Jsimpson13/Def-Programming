# Handles user authentication and registration
# Allows users to log in, verifying credentials through the database
# Provides functionality for adding new users

import getpass

import sys

import os

sys.path.append(os.path.expanduser('~/Desktop/Def-Programming'))

from Server import Db, serverMain





class loginPage:

# Prompts the user to login in, checks credentials, limits failed attempts
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


# Prompts for new user details and adds them to the database
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

        

                
