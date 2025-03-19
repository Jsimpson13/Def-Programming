import tkinter as tk
import sys
sys.path.append('C:\\Users\\jsimp\\OneDrive\\Desktop\\Def-Programming')
#import Backend.loginPage as loginPage

class LoginUI:

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
if __name__=="__main__":
    app=LoginUI()