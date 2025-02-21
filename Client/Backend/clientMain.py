from multiprocessing.connection import Client


def main():
    print("Hello World!")
    Client.Backend.loginPage.loginUI()
    # mainUI()    

if __name__=="__main__":
    main()