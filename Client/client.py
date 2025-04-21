# DiffieHellmanClient.py
# This client script establishes a secure connection with a server using the Diffie-Hellman key exchange protocol
# Once connected, it uses a shared key for encrypted communication
# The client can log in or add users, and interact with various features like viewing/adding points or events
# Encryption and decryption are handled by custom Encoding/Decrypt modules


import sys
import os
import socket

from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

sys.path.append(os.path.expanduser('~/Desktop/Def-Programming'))

from Decrypt import Decrypt
from Encoding import Encoding
from Server.loginPage import loginPage
from Server.pointsPage import pointsPage
from Server.events import events

# Initializes the client with a target host and port, creates a socket, and prepares shared key storage
class DiffieHellmanClient:
    loggedin = False

    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.shared_key = None

# Establishes connection to the server
    def connect(self):
        self.client_socket.connect((self.host, self.port))
        print(f"Connected to server at {self.host}:{self.port}")
        self.perform_key_exchange()

# Performs key exchange and derives shared key using HKDF
    def perform_key_exchange(self):
        # Read until delimiter
        DELIMITER = b"-----DH-SPLIT-----"
        buffer = b""
        while DELIMITER not in buffer:
            buffer += self.client_socket.recv(2048)

        server_parameters_bytes, server_public_bytes = buffer.split(DELIMITER)

        server_parameters = serialization.load_pem_parameters(server_parameters_bytes, backend=default_backend())
        server_public_key = serialization.load_pem_public_key(server_public_bytes, backend=default_backend())

        client_private_key = server_parameters.generate_private_key()
        client_public_key = client_private_key.public_key()

        client_public_bytes = client_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        self.client_socket.sendall(client_public_bytes)

        shared_key = client_private_key.exchange(server_public_key)

        self.shared_key = HKDF(
            algorithm=SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
            backend=default_backend()
        ).derive(shared_key)

        print("Key exchange successful. Secure communication established.")

# Encrypts a message using shared key and sends it to the server
    def send_message(self, message, usrNm):
        formatted_message = f"{usrNm}:{message}"
        encrypted_message = Encoding.Encrypt(formatted_message, int(self.shared_key.hex(), 16))
        self.client_socket.sendall(encrypted_message.encode('utf-8'))

# Receives encrypted message from the server and decrypts it
    def receive_message(self):
        encrypted_message = self.client_socket.recv(10000).decode('utf-8')
        if not encrypted_message:
            return None
        decrypted_message = Decrypt.DECS(encrypted_message, int(self.shared_key.hex(), 16))
        return decrypted_message

# Handles the interactive client interface, user input, and routing to points and event interface
    def interactive_chat(self):
        try:
            curr_user = self.loggin()
            while True:
                print("\nWELCOME TO THE FLORAL PIRATES\nOptions:")
                print("[1] Menu\n[2] Main\n[3] Points\n[4] Events\n[5] Exit\n")
                premessage = input("Client: ")
                message = premessage.replace(" ", "").lower()

                if message in ["exit", "5"]:
                    self.send_message("exit", curr_user)
                    break
                elif message in ["points", "3"]:
                    pointsPage.pageDisplay(curr_user)
                    pointsPage.addPoints(curr_user)
                elif message in ["events", "4"]:
                    events.pageDisplay(curr_user)
                else:
                    self.send_message(message, curr_user)
                    response = self.receive_message()
                    print(f"Server: {response}")
        finally:
            self.disconnect()

# Closes the socket connection to the server
    def disconnect(self):
        self.client_socket.close()
        print("Disconnected from server.")

# Prompts the user to login or create a new account
    def loggin(self):
        while True:
            choice = input("Login or Add User (Login or Add): ").replace(" ", "").lower()
            if choice == 'login':
                user = loginPage.loggedin()
                if user == "":
                    user = loginPage.addUser()
                return user
            elif choice == 'add':
                return loginPage.addUser()
            else:
                print("Please enter a valid choice: Login or Add")


if __name__ == "__main__":
    client = DiffieHellmanClient()
    client.connect()
    client.interactive_chat()
