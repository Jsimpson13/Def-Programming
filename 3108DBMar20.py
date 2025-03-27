#Database for Def Prog Group Assignment
#Judson Whiteside
#Feb 26 2025

#SQLite import
import sqlite3

#function for creating database tables
#creates profile, purchase, and event tables
def createDB():
#creating cursor
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
#creating profile table 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profile
        (uid INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL UNIQUE,
        phone TEXT,
        points INTEGER NOT NULL)
        ''')
    conn.commit()
#creating event table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS event
        (eid INTEGER PRIMARY KEY AUTOINCREMENT,
        cost INTEGER,
        name TEXT UNIQUE)
        ''')
    conn.commit()
#create purchase table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchase
        (tid INTEGER PRIMARY KEY AUTOINCREMENT,
        uid INTEGER NOT NULL,
        eid INTEGER NOT NULL,
        CONSTRAINT fk_uid FOREIGN KEY (uid) REFERENCES profile(uid),
        CONSTRAINT fk_eid FOREIGN KEY (eid) REFERENCES event(eid))
        ''')
    conn.commit()
    conn.close()

#add entry to profile table function
def addProfile(profileUsername, profilePassword, profileName, profilePhone):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    try:
        #user points default to 0
        cursor.execute('''
        INSERT INTO profile (username, password, name, phone, points) VALUES (?, ?, ?, ?, ?)''', (profileUsername,profilePassword, profileName, profilePhone, 0))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error: user already exists.")
    conn.close()

#add entry to event table function
def addEvent(eventCost, eventName):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT INTO event (cost, name) VALUES (?, ?)''', (eventCost, eventName))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Error: event already exists.")
    conn.close()

#point query function
def checkPoints(usrnm):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    try:
        cursor.execute('''
        SELECT points FROM profile WHERE username = ?''', (usrnm,))
        pointBalance = cursor.fetchall()
        #pointBalance counts as array; this gets the first (and only) value
        retBal = pointBalance[0]
    except:
        print("Error: Unable to find user")
    conn.close()
    return retBal

#point add function
def addPoints(usrnm, newPoints):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()    
    try:
        cursor.execute('''
        UPDATE profile SET points = points + ? WHERE username = ?''', (newPoints, usrnm))
        conn.commit()
    except:
        print("Error: user does not exist")
    conn.close()

#purchase ticket function
def buyTickets(usrnm, evntNm):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    #checking if user has enough points for tickets
    currBal = checkPoints(usrnm)
    #formatting from tuple to integer
    frmtCurrBal = currBal[0]
    #checking event price
    try:
        cursor.execute('''
        SELECT cost FROM event WHERE name = ?''', (evntNm,))
        event = cursor.fetchall()
        #formatting from array to tuple to integer
        evCst = event[0]
        frmtCst = evCst[0]
    except:
        print("Error: event does not exist")
    try:
        #making sure the profile can pay for the tickets
        if(frmtCst > frmtCurrBal):
            #remove purchase record if tickets are too expensive
            print("Error: ticket cost exceeds user balance")
        else:
            #deducting points after purchase
            cursor.execute('''
            UPDATE profile SET points = points - ? WHERE username = ?''', (frmtCst, usrnm))
            conn.commit()
            #getting uid for new purchase entry
            cursor.execute('''
            SELECT uid FROM profile WHERE username = ?''', (usrnm,))
            userID = cursor.fetchall()
            #formatting from array to tuple to integer
            uid = userID[0]
            frmtUID = uid[0]
            #getting eid for new purchase entry
            cursor.execute('''
            SELECT eid FROM event WHERE name = ?''', (evntNm,))
            eventID = cursor.fetchall()
            #formatting from array to tuple to integer
            eid = eventID[0]
            frmtEID = eid[0]
            #creating a purchase table entry using the uid and eid
            cursor.execute('''
            INSERT INTO purchase (uid, eid) VALUES (?, ?)''', (frmtUID, frmtEID))
            conn.commit()
    except:
        print("Error: unable to make purchase (invalid user or event)")
    conn.close()
        

#query event function
def checkEvents():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    try:
        cursor.execute('''
        SELECT name, cost FROM event''')
        events = cursor.fetchall()
    except:
        print("Error: no events found")
    conn.close()
    return events

#query past transactions
def checkPurchases(usrnm):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    try:
        cursor.execute('''
        SELECT name, cost FROM event WHERE eid = 
        (SELECT eid FROM purchase WHERE uid = 
        (SELECT uid FROM profile WHERE username = ?))''', (usrnm,))
        purchases = cursor.fetchall()     
    except:
        print("Error: no purchases found")
    conn.close()
    return purchases

#query profile function
def checkProfile(usrnm):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    try:
        cursor.execute('''
        SELECT username, password, name, phone, points FROM profile WHERE username = ?''', (usrnm,))
        profiles = cursor.fetchall()
    except:
        print("Error: no events found")
    conn.close()
    return profiles   

#edit profile function
def editProfile(usrnm, chngType, chngVal):
    #all uppercase to correct formatting for input validation
    upChngType = chngType.upper()
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    try:
        if(upChngType == "USERNAME"):
            cursor.execute('''
            UPDATE profile SET username = ? WHERE username = ?''', (chngVal, usrnm))
        elif(upChngType == "NAME"):
            cursor.execute('''
            UPDATE profile SET name = ? WHERE username = ?''', (chngVal, usrnm))
        elif(upChngType == "PHONE"):
            cursor.execute('''
            UPDATE profile SET phone = ? WHERE username = ?''', (chngVal, usrnm))
        elif(upChngType == "PASSWORD"):
            cursor.execute('''
            UPDATE profile SET password = ? WHERE username = ?''', (chngVal, usrnm))
        #no option for changing points; point changes should be done through addPoints
        else:
            print("Error: please provide a valid field to change")
        conn.commit()
    except:
        print("Error: profile does not exist")
    conn.close()

#query login information function
#returns True/False (only checking for valid login credentials)
def checkLoginCreds(usrnm, psswd):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    try:
        cursor.execute('''
        SELECT * FROM profile WHERE username = ? AND password = ?''', (usrnm,psswd))
        profiles = cursor.fetchall()
    except:
        print("Error: profile not found")
    conn.close()
    return profiles

#test main function
#this is example scenarios to make sure everything functions as intended
if __name__ == "__main__":
#create database test
    createDB()
    print("DB successfully created\n")
#add profiles event test
    addProfile("Bob123", "Password123", "Robert", "123-456-7890")
    addProfile("41ic3", "SecurePassword", "Alice", "987-654-3210")
    print("Profiles successfully created\n")
#add events test
    addEvent(150, "Bruins @ Sabres")
    addEvent(200, "Islanders @ Devils")
    addEvent(300, "Oilers @ Canucks")
    print("Events successfully added\n")
#show point balance test
    balance = checkPoints("Bob123")
    #balance is a tuple; this gets cleans up the formatting
    print("Point Balance: ", balance[0],"\n")
#add points test
    addPoints("Bob123", 250)
    postAddBal = checkPoints("Bob123")
    print("Point Balance After Addition: ", postAddBal[0],"\n")
#display events test
    currEvents = checkEvents()
    print("Current Events:")
    for name, cost in currEvents:
        print(name,"\t",cost)
#display profile test
    dispProf = checkProfile("41ic3")
    print("\nUser Information:")
    for username, password, name, phone, points in dispProf:
        print(username,"\t",password,"\t",name,"\t",phone,"\t",points)
#edit profile test
    editProfile("41ic3", "name", "Alice S.")
    editProfile("41ic3", "phone", "314-159-2653")
    editProfile("41ic3", "username", "AliceS1999")
    editProfile("AliceS1999", "password", "NewPassword")
    updtdProf = checkProfile("AliceS1999")
    print("\nUpdated User Information:")
    for username, password, name, phone, points in updtdProf:
        print(username,"\t",password,"\t",name,"\t",phone,"\t",points)
#purchase test (sufficient balance)
    buyTickets("Bob123", "Islanders @ Devils")
    postBuyBalance = checkPoints("Bob123")
    print("\nPoints after Purchase: ", postBuyBalance[0])
#purchase display test
    dispPurch = checkPurchases("Bob123")
    print("\nPurchases:")
    for name, cost in dispPurch:
        print(name,"\t",cost)
#check login credentials (valid)
    result = checkLoginCreds("Bob123", "Password123")
    if(result):
        print("\nAccount exists")
    else:
        print("\nAccount not found")
#check login credentials (invalid)
    result = checkLoginCreds("Bob123", "WrongPassword")
    if (result):
        print("\nAccount exists")
    else:
        print("\nAccount not found")
#the end (for now)
    print("\nTest concluded successfully")
