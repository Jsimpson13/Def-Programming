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
def addProfile(profileUsername, profileName, profilePhone):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    try:
        #user points default to 0
        cursor.execute('''
        INSERT INTO profile (username, name, phone, points) VALUES (?, ?, ?, ?)''', (profileUsername, profileName, profilePhone, 0))
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

    
##    #creating new entry in purchase table
##    cursor.execute('''INSERT INTO purchase (uid, eid)
##    SELECT uid FROM profile WHERE username = ?
##    UNION ALL
##    SELECT eid FROM event WHERE name = ?''', (usrnm, evntNm,))
##    conn.commit()

    
    #checking if user has enough points for tickets
    currBal = checkPoints(usrnm)
    #LIMIT 1 gets the latest entry
    #as buyTickets always creates a new entry, it will always get the uid from the profile that just purchased tickets
    cursor.execute('''SELECT points FROM profile WHERE uid =
    (SELECT uid FROM profile WHERE uid =
    (SELECT uid FROM purchase LIMIT 1)''')
    tcktCstArr = cursor.fetchall()
    #formatting
    ticketCost = tcktCstArr[0]
    #making sure the profile can pay for the tickets
    if(ticketCost > currBal):
        #remove purchase record if tickets are too expensive
        print("Error: ticket cost exceeds user balance")
        cursor.execute('''DELETE FROM purchase WHERE eid =
        (SELECT eid FROM purchase LIMIT 1)''')
    else:
        cursor.execute('''
        UPDATE profile SET points = points - ? WHERE username = ?''', (ticketCost, usrnm))
    conn.commit()
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
#NOT IMPLEMENTED
#TO-DO

#query profile function
def checkProfile(usrnm):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    try:
        cursor.execute('''
        SELECT username, name, phone, points FROM profile WHERE username = ?''', (usrnm,))
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
        #no option for changing points; point changes should be done through addPoints
        else:
            print("Error: please provide a valid field to change")
        conn.commit()
    except:
        print("Error: profile does not exist")
    conn.close()

#query login information function
#NOT IMPLEMENTED
#TO-DO

#test main function
if __name__ == "__main__":
#create database test
    createDB()
    print("DB successfully created\n")
#add profiles event test
    addProfile("Bob123", "Robert", "123-456-7890")
    addProfile("41ic3", "Alice", "987-654-3210")
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
    for username, name, phone, points in dispProf:
        print(username,"\t",name,"\t",phone,"\t",points)
#edit profile test
    editProfile("41ic3", "name", "Alice S.")
    editProfile("41ic3", "phone", "314-159-2653")
    editProfile("41ic3", "username", "AliceS1999")
    updtdProf = checkProfile("AliceS1999")
    print("\nUpdated User Information:")
    for username, name, phone, points in updtdProf:
        print(username,"\t",name,"\t",phone,"\t",points)
#purchase test (sufficient balance)
    buyTickets("Bob123", "Islanders @ Devils")
    postBuyBalance = checkPoints("Bob123")
    print("Points after Purchase: ", postBuyBalance[0])
#the end (for now)
    print("\nTest concluded successfully")
