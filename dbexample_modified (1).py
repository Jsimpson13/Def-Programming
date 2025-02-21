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

def add_user(input_name, input_address,  input_balance):
    """Add a new user with their address to the database."""
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (name, address, balance) VALUES (?, ?, ?)', (input_name, input_address, input_balance))
        conn.commit()
        print(f"User '{input_name}' added successfully.")
    except sqlite3.IntegrityError:
        print(f"User '{input_name}' already exists.")
    conn.close()

def get_all_users():
    """Retrieve all users and their addresses from the database."""
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, address, balance FROM users')
    users = cursor.fetchall()
    conn.close()
    return users
    
def get_user(input_name):
    """Retrieve user with name."""
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    item=(input_name,)
    cursor.execute('SELECT * FROM users WHERE name = ?', item)
    #cursor.execute('SELECT * FROM users WHERE name = ?', (input_name,))
    user = cursor.fetchall()
    conn.close()
    return user

# Main Program
if __name__ == "__main__":
    create_table()

    while True:
        print("\nMenu:")
        print("1. Add a user")
        print("2. View all users and their info")
        print("3. Find user")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            customer_name = input("Enter the name: ")
            customer_address = input("Enter the address: ")
            customer_balance=input("Enter the balance: ")
            add_user(customer_name, customer_address,customer_balance)
        elif choice == '2':
            users = get_all_users()
            if users:
                print("\nUser Information:")
                for user, address, balance in users: #can use any variable instead of user, address, balance
                    print(user,address, balance) #us eteh same variable set you used in previous line
            else:
                print("\nNo users found.")
        elif choice == '3':
            customer_name = input("Enter name: ")     
            user = get_user(customer_name)
            if user:
                print(user)
            else:
                print("\nNo users found.")
        elif choice == '4':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
