import tkinter as tk
from PIL import Image, ImageTk

class NewUserUI: 
    def __init__(self):
        newuser = tk.Toplevel()  # Opens as a new window on top of the main one
        newuser.title("New User")
        newuser.geometry("250x300")
        newuser.configure(bg="black")

        # Load the logo image
        self.image = Image.open("C:\\Users\\jsimp\\OneDrive\\Desktop\\Def-Programming\\Client\\GUI\\skulllogo.png")
        self.image = self.image.resize((75, 75))
        self.logoimage_tk = ImageTk.PhotoImage(self.image)

        # Add logo
        self.logobutton = tk.Label(newuser, image=self.logoimage_tk, bg="black")
        self.logobutton.pack()

        # Username Entry
        self.usrnamelabel = tk.Label(newuser, text="User Name", bg="black", fg="white")
        self.usrnamelabel.pack()
        self.usrname = tk.Entry(newuser, width=20)
        self.usrname.pack()

        # Password Entry
        self.passwordlabel = tk.Label(newuser, text="Password", bg="black", fg="white")
        self.passwordlabel.pack()
        self.password = tk.Entry(newuser, width=20, show="*")
        self.password.pack()

        # Name Entry
        self.namelabel = tk.Label(newuser, text="First and Last Name", bg="black", fg="white")
        self.namelabel.pack()
        self.name = tk.Entry(newuser, width=20)
        self.name.pack()

        # Phone Entry
        self.phonelabel = tk.Label(newuser, text="Phone Number", bg="black", fg="white")
        self.phonelabel.pack()
        self.phone = tk.Entry(newuser, width=20)
        self.phone.pack()

        # Submit Button
        self.newuserbtn = tk.Button(newuser, text="Welcome", width=7, bg="pink", fg="green")#, command=self.submit_new_user)
        self.newuserbtn.pack(pady=10)

    def submit_new_user(self):
        # Logic for saving new user data
        username = self.usrname.get()
        password = self.password.get()
        name = self.name.get()
        phone = self.phone.get()
        print(f"New user created: {username}, {name}, {phone}")