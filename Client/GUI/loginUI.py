import tkinter as tk
#import Backend.loginPage as loginPage

class loginUI:

    def __init__(self):
        self.root=tk.Tk()
        self.root.title("Login Page")
        self.root.geometry("250x300")
        usrlabel=tk.Label(text="Username:")
        pswdlabel=tk.Label(text="Password: ")
        usr=tk.Entry(self.root, width="20")
        pswd=tk.Entry(self.root, width="20", show="*")
        signinbtn=tk.Button(text="Sign in", width="5")

        usrlabel.pack()
        usr.pack()
        pswdlabel.pack()
        pswd.pack()
        signinbtn.pack()
        self.root.mainloop()
loginUI()