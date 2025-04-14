from pathlib import Path
import sys
project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))
import socket
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import serialization
from Decrypt import Decrypt  # Import your Decrypt class
from Encoding import Encoding
from Server.loginPage import loginPage  # Import your Encoding function or class
from Server.pointsPage import pointsPage
from Server.events  import events

class DiffieHellmanClient:
    loggedin=False
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.shared_key = None

    def connect(self):
        """Connects to the server and initiates the key exchange."""
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to server at {self.host}:{self.port}")

        self.perform_key_exchange()

    def perform_key_exchange(self):
        """Handles the Diffie-Hellman key exchange with the server."""
        # Receive server parameters and public key
        server_parameters_bytes = self.client_socket.recv(2048)
        server_parameters = serialization.load_pem_parameters(server_parameters_bytes)

        server_public_bytes = self.client_socket.recv(2048)
        server_public_key = serialization.load_pem_public_key(server_public_bytes)

        # Generate client private and public key
        client_private_key = server_parameters.generate_private_key()
        client_public_key = client_private_key.public_key()

        # Send client public key to server
        client_public_bytes = client_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        self.client_socket.sendall(client_public_bytes)

        # Compute shared key
        shared_key = client_private_key.exchange(server_public_key)

        # Derive symmetric key
        self.shared_key = HKDF(
            algorithm=SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
        ).derive(shared_key)

        print("Key exchange successful. Secure communication established.")

    def send_message(self, message,usrNm):
        """Encrypts and sends a message to the server."""
        formatmsg=f"{usrNm}:{message}"
        encrypted_message = Encoding.Encrypt(formatmsg, int(self.shared_key.hex(), 16))
        self.client_socket.sendall(encrypted_message.encode('utf-8'))

    def receive_message(self):
        """Receives and decrypts a message from the server."""
        encrypted_message = self.client_socket.recv(10000).decode('utf-8')
        if not encrypted_message:
            return None

        decrypted_message = Decrypt.DECS(encrypted_message, int(self.shared_key.hex(), 16))
        return decrypted_message

    def interactive_chat(self):
        """Allows the client to chat interactively with the server."""
        try:
            currUser=client.loggin()
            print("WELCOME TO THE FLORAL PRIATES\n"+" Options: \n[1]Menu\n[2]Main\n[3]Points\n[4]Events\n[5]Exit\n")
            while (True):
                premessage = input("Client: ")
                message= str(premessage).replace(" ","").lower()
                if message == "exit" or message=="5":
                    self.send_message("exit", currUser)
                    break
                if message=="points" or message=="3":
                    pointsPage.pageDisplay(currUser)
                    pointsPage.addPoints(currUser)
                elif message=="events" or message=="4":
                    events.pageDisplay(currUser)
                else:    
                    self.send_message(message,currUser)
                    response = self.receive_message()
                    print(f"Server: {response}")
        finally:
            self.disconnect()

    def disconnect(self):
        """Closes the connection to the server."""
        self.client_socket.close()
        print("Disconnected from server.")

    def loggin(self): 
        while(True):
            choice=str(input("Login or Add User (Login or Add): ")).replace(" ", "").lower()
            if choice=='login':
                user=loginPage.loggedin()
                if (user==""):
                    user=loginPage.addUser()
                return user
                break
            elif choice=='add':
                return loginPage.addUser()
                break
            else: print("Please put a valid choice, Login or Add")
            

if __name__ == "__main__":
    client = DiffieHellmanClient()
    client.connect()
    client.interactive_chat()
