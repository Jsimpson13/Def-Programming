import tkinter as tk
from PIL import Image, ImageTk
from tkinter.ttk import Label

class mainGUI():
   def __init__(self):
       # Initialize the Tkinter root window
        self.root = tk.Tk()
        self.root.title("The Floral Reapers")#Skull and Bloom
        self.root.geometry("450x500")  # Initial window size
        self.root.configure(bg="black")
        # Load the logo image
        self.image = Image.open("Client/GUI/skulllogo.png")
        self.image = self.image.resize((75, 75))  # Resize image before converting to PhotoImage
        self.image_tk = ImageTk.PhotoImage(self.image)  # Keep a reference

        #Words
        self.teamName=tk.Label(self.root, text="The Floral Reapers",fg="white", bg="black", font=("Times New Roman",35)).pack()
        self.teamSlogan=tk.Label(self.root, text="Skull and Bloom", fg="white", bg="black",font=("Times New Roman",20)).pack()

        # Image button
        self.logobutton = tk.Button(self.root, image=self.image_tk)  # Button with image

        self.logobutton.pack(pady=10)
        self.root.mainloop()



mainGUI()