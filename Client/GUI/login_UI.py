import sys
sys.path.append('C:/Users/jsimp/OneDrive/Desktop/Def-Programming')
import tkinter as tk
from PIL import Image, ImageTk
from Client.GUI.newusr_UI import NewUserUI

class loginUI:
    def __init__(self):
        # Initialize the Tkinter root window
        self.root = tk.Tk()
        self.root.title("Login Page")
        self.root.geometry("250x300")  # Initial window size

        # Load the logo image
        self.image = Image.open("Client/GUI/skulllogo.png")
        self.image = self.image.resize((75, 75))  # Resize image before converting to PhotoImage
        self.image_tk = ImageTk.PhotoImage(self.image)  # Keep a reference

        # Load the background image
        self.bgimage = Image.open("Client/GUI/HD-wallpaper-bit-city.jpg")
        self.bgimage_tk = ImageTk.PhotoImage(self.bgimage)  # Keep a reference

        # Set background image as label
        self.bg_label = tk.Label(self.root, image=self.bgimage_tk)
        self.bg_label.place(relwidth=1, relheight=1)  # Make the background cover the window

        # Create UI elements
        self.usrlabel = tk.Label(self.root, text="Username:")
        self.pswdlabel = tk.Label(self.root, text="Password: ")
        self.usr = tk.Entry(self.root, width=20)
        self.pswd = tk.Entry(self.root, width=20, show="*")
        self.signinbtn = tk.Button(self.root, text="Sign in", width=7)
        self.newuserbtn=tk.Button(self.root,text="New User", width=7, command=self.open_new_user_page)

        # Image button
        self.logobutton = tk.Button(self.root, image=self.image_tk)  # Button with image

        # Pack other elements
        self.usrlabel.pack()
        self.usr.pack()
        self.pswdlabel.pack()
        self.pswd.pack()
        self.signinbtn.pack(side="left")
        self.newuserbtn.pack(side="right")
        self.logobutton.pack(pady=10)

        # Bind the window resize event to the on_resize method
        self.root.bind("<Configure>", self.on_resize)

        # Start the mainloop
        self.root.mainloop()

    def on_resize(self, event):
        """This method is called when the window is resized"""
        # Get the new window width and height
        new_width = event.width
        new_height = event.height

        # Resize the background image dynamically
        bgimage_resized = self.bgimage.resize((new_width, new_height))
        self.bgimage_tk = ImageTk.PhotoImage(bgimage_resized)

        # Update the background label with resized image
        self.bg_label.config(image=self.bgimage_tk)

        # Resize the logo image dynamically but cap the max size
        max_logo_size = (new_width // .5, new_height // .5)  # Set a max size (1/3 of window width and height)
        logo_resized = self.image.resize(max_logo_size)
        self.image_tk = ImageTk.PhotoImage(logo_resized)

        # Update the logo button with resized image
        self.logobutton.config(image=self.image_tk)
    def open_new_user_page(self):
        NewUserUI()
    def sign_in(self):
        return "print"
# Run the UI
#loginUI()
