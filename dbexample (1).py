import sqlite3

def create_table():
    """Create the users table if it doesn't exist."""
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            address TEXT NOT NULL,
            balance REAL
        )
    ''')
    conn.commit()
    conn.close()

def add_user(name, address,  balance):
    """Add a new user with their address to the database."""
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (name, address, balance) VALUES (?, ?, ?)', (name, address, balance))
        conn.commit()
        print(f"User '{name}' added successfully.")
    except sqlite3.IntegrityError:
        print(f"User '{name}' already exists.")
    conn.close()

def get_all_users():
    """Retrieve all users and their addresses from the database."""
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, address, balance FROM users')
    users = cursor.fetchall()
    conn.close()
    return users
    
def get_user(name):
    """Retrieve user with name."""
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    item=(name,)
    #cursor.execute('SELECT * FROM users WHERE name = ?', (name,))
    cursor.execute('SELECT * FROM users WHERE name = ?', item)
    user = cursor.fetchall()
    conn.close()
    return user

# Main Program
if __name__ == "__main__":
    create_table()

    while True:
        print("\nMenu:")
        print("1. Add a user with address")
        print("2. View all users and addresses")
        print("3. Find user")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter the name: ")
            address = input("Enter the address: ")
            balance=input("Enter the balance: ")
            add_user(name, address,balance)
        elif choice == '2':
            users = get_all_users()
            if users:
                print("\nUser Information:")
                for user, address, balance in users:
                    print(user,address, balance)
            else:
                print("\nNo users found.")
        elif choice == '3':
            name = input("Enter name: ")     
            user = get_user(name)
            if user:
                print(user)
            else:
                print("\nNo users found.")
        elif choice == '4':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
