#Database for Def Prog Group Assignment

#Judson Whiteside

#Feb 26 2025



#SQLite import

import sqlite3



# Define a constant path to the database

DB_PATH = "~/Desktop/Def-Programming/database.db"



# Function for creating database tables

def createDB():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute('''

        CREATE TABLE IF NOT EXISTS profile

        (uid INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT NOT NULL UNIQUE,

        password TEXT NOT NULL,

        name TEXT NOT NULL,

        phone TEXT,

        points INTEGER NOT NULL)

    ''')

    conn.commit()

    cursor.execute('''

        CREATE TABLE IF NOT EXISTS event

        (eid INTEGER PRIMARY KEY AUTOINCREMENT,

        cost INTEGER,

        name TEXT UNIQUE)

    ''')

    conn.commit()

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



def addProfile(profileUsername, profilePassword, profileName, profilePhone):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    try:

        cursor.execute('''

        INSERT INTO profile (username, password, name, phone, points) VALUES (?, ?, ?, ?, ?)''', 

        (profileUsername, profilePassword, profileName, profilePhone, 0))

        conn.commit()

    except sqlite3.IntegrityError:

        print("Error: user already exists.")

    conn.close()



def addEvent(eventCost, eventName):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    try:

        cursor.execute('''

        INSERT INTO event (cost, name) VALUES (?, ?)''', (eventCost, eventName))

        conn.commit()

    except sqlite3.IntegrityError:

        print("Error: event already exists.")

    conn.close()



def checkPoints(usrnm):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    retBal = []

    try:

        cursor.execute('''

        SELECT points FROM profile WHERE username = ?''', (usrnm,))

        pointBalance = cursor.fetchall()

        retBal = pointBalance[0]

    except:

        print("Error: Unable to find user")

    conn.close()

    return retBal



def addPoints(usrnm, newPoints):
	points = int(newPoints)
	
	conn = sqlite3.connect(DB_PATH)

	cursor = conn.cursor()    

	try:

		cursor.execute('''UPDATE profile SET points = points + ? WHERE username = ?''', (points, usrnm))

		conn.commit()

	except:

		print("Error: user does not exist")

	conn.close()



def buyTickets(usrnm, evntNm):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    print("Connected")

    currBal = checkPoints(usrnm)

    print("Checked Points")

    frmtCurrBal = currBal[0]

    try:

        cursor.execute('''

        SELECT cost FROM event WHERE name = ?''', (evntNm,))

        event = cursor.fetchall()

        evCst = event[0]

        frmtCst = evCst[0]

    except:

        print("Error: event does not exist")

        conn.close()

        return

    try:

        if(frmtCst > frmtCurrBal):

            print("Error: ticket cost exceeds user balance")

        else:

            cursor.execute('''

            UPDATE profile SET points = points - ? WHERE username = ?''', (frmtCst, usrnm))

            conn.commit()

            print("updated points")

            cursor.execute('''

            SELECT uid FROM profile WHERE username = ?''', (usrnm,))

            userID = cursor.fetchall()

            uid = userID[0]

            frmtUID = uid[0]

            print("get uid")

            cursor.execute('''

            SELECT eid FROM event WHERE name = ?''', (evntNm,))

            eventID = cursor.fetchall()

            print("made new eid for purchase")

            eid = eventID[0]

            frmtEID = eid[0]

            cursor.execute('''

            INSERT INTO purchase (uid, eid) VALUES (?, ?)''', (frmtUID, frmtEID))

            # print("frmtUID: ", frmtUID, "\n frmtEID", frmtEID)

            conn.commit()

            print("finished")

    except:

        print("Error: unable to make purchase (invalid user or event)")

    conn.close()



def checkEvents():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    events = []

    try:

        cursor.execute('''

        SELECT name, cost FROM event''')

        events = cursor.fetchall()

    except:

        print("Error: no events found")

    conn.close()

    return events



def checkPurchases(usrnm):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    purchases = []

    try:

        cursor.execute('''

        SELECT event.name, event.cost 

        FROM purchase

        JOIN profile ON purchase.uid = profile.uid

        JOIN event ON purchase.eid = event.eid

        WHERE profile.username = ?''', (usrnm,))

        purchases = cursor.fetchall()

        print(purchases, len(purchases))

    except Exception as e:

        print("Error retrieving purchases:", e)

    finally:

        conn.close()

    return purchases



def checkProfile(usrnm):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    profiles = []

    try:

        cursor.execute('''

        SELECT username, password, name, phone, points FROM profile WHERE username = ?''', (usrnm,))

        profiles = cursor.fetchall()

    except:

        print("Error: no profile found")

    conn.close()

    return profiles   



def editProfile(usrnm, chngType, chngVal):

    upChngType = chngType.upper()

    conn = sqlite3.connect(DB_PATH)

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

        else:

            print("Error: please provide a valid field to change")

        conn.commit()

    except:

        print("Error: profile does not exist")

    conn.close()



def checkLoginCreds(usrnm, psswd):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    profiles = []

    try:

        cursor.execute('''

        SELECT * FROM profile WHERE username = ? AND password = ?''', (usrnm, psswd))

        profiles = cursor.fetchall()

    except sqlite3.Error as e:

        print("Error: profile not found", e)

    finally:

        conn.close()

    return profiles



# Test main

if __name__ == "__main__":

    createDB()

    print("DB successfully created\n")

    addProfile("Bob123", "Password123", "Robert", "123-456-7890")

    addProfile("41ic3", "SecurePassword", "Alice", "987-654-3210")

    print("Profiles successfully created\n")

    addEvent(150, "Bruins @ Sabres")

    addEvent(200, "Islanders @ Devils")

    addEvent(300, "Oilers @ Canucks")

    print("Events successfully added\n")

    balance = checkPoints("Bob123")

    print("Point Balance: ", balance[0],"\n")

    addPoints("Bob123", 1000)

    postAddBal = checkPoints("Bob123")

    print("Point Balance After Addition: ", postAddBal[0],"\n")

    currEvents = checkEvents()

    print("Current Events:")

    for name, cost in currEvents:

        print(name,"\t",cost)

    dispProf = checkProfile("41ic3")

    print("\nUser Information:")

    for username, password, name, phone, points in dispProf:

        print(username,"\t",password,"\t",name,"\t",phone,"\t",points)

    editProfile("41ic3", "name", "Alice S.")

    editProfile("41ic3", "phone", "314-159-2653")

    editProfile("41ic3", "username", "AliceS1999")

    editProfile("AliceS1999", "password", "NewPassword")

    updtdProf = checkProfile("AliceS1999")

    print("\nUpdated User Information:")

    for username, password, name, phone, points in updtdProf:

        print(username,"\t",password,"\t",name,"\t",phone,"\t",points)

    buyTickets("Bob123", "Oilers @ Canucks")

    buyTickets("Bob123", "Islanders @ Devils")

    postBuyBalance = checkPoints("Bob123")

    print("\nPoints after Purchase: ", postBuyBalance[0])

    dispPurch = checkPurchases("Bob123")

    print("\nPurchases:")

    for name, cost in dispPurch:

        print(name,"\t",cost)

    result = checkLoginCreds("Bob123", "Password123")

    print("\nAccount exists" if result else "\nAccount not found")

    result = checkLoginCreds("Bob123", "WrongPassword")

    print("\nAccount exists" if result else "\nAccount not found")

    print("\nTest concluded successfully")


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
    addPoints("Bob123", 1000)
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
    buyTickets("Bob123", "Oilers @ Canucks")
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
