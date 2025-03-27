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

#add entry to event table function
#creates new event
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

#test main function
if __name__ == "__main__":
#create database test
    createDB()
    print("DB successfully created")
#add event test
    addEvent(150, "Bruins @ Sabres")
    print("Event successfully added")
#the end (for now)
    print("Test concluded successfully")
