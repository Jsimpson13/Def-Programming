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
    cursor.execute('''
    SELECT points FROM profile WHERE username = ?''', (usrnm,))
    pointBalance = cursor.fetchall()
    conn.close()
    return pointBalance

#test main function
if __name__ == "__main__":
#create database test
    createDB()
    print("DB successfully created")
#add profiles event test
    addProfile("Bob123", "Robert", "123-456-7890")
    addProfile("A1ic3", "Alice", "987-654-3210")
    print("Profiles successfully created")
#add events test
    addEvent(150, "Bruins @ Sabres")
    addEvent(200, "Islanders @ Devils")
    addEvent(300, "Oilers @ Canucks")
    print("Events successfully added")
#show point balance test
    balance = checkPoints("Bob123")
    if balance:
        print("Point balance: ", balance)
    else:
        print("Error: User not found")
#the end (for now)
    print("Test concluded successfully")
