# Implements the server side of our secure communication system
# Supports encrypted client-server message
# Initializes the server environment and database

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
from Server import Db


class DiffieHellmanServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = None
        self.client_address = None
        self.shared_key = None
        self.running = True

# Starts the server, sets up socket options, creates the database, and accepts client connection
    def start(self):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        Db.createDB()
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print(f"Server listening on {self.host}:{self.port}...")

        self.connection, self.client_address = self.server_socket.accept()
        print(f"Connection established with {self.client_address}")
        self.perform_key_exchange()

# Performs Diffie-Hellman key exchange to establish a shared secret key with the client
    def perform_key_exchange(self):
        parameters = dh.generate_parameters(generator=2, key_size=512, backend=default_backend())
        server_private_key = parameters.generate_private_key()
        server_public_key = server_private_key.public_key()

        server_parameters_bytes = parameters.parameter_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.ParameterFormat.PKCS3
        )
        server_public_bytes = server_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # Combine and send with delimiter
        DELIMITER = b"-----DH-SPLIT-----"
        payload = server_parameters_bytes + DELIMITER + server_public_bytes
        print("Sending DH parameters and public key...")
        self.connection.sendall(payload)

        # Receive client's public key
        client_public_bytes = self.connection.recv(4096)
        client_public_key = serialization.load_pem_public_key(client_public_bytes, backend=default_backend())

        shared_key = server_private_key.exchange(client_public_key)

        self.shared_key = HKDF(
            algorithm=SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
            backend=default_backend()
        ).derive(shared_key)

        print("Key exchange successful. Secure communication established.")

# Handles continuous communication with the client
    def handle_messages(self, message_handler):
        try:
            while self.running:
                client_message = self.connection.recv(10000).decode('utf-8')
                if not client_message:
                    continue
                if client_message.lower() == "exit":
                    self.exit_server()
                    break

                decrypted_message = Decrypt.DECS(client_message, int(self.shared_key.hex(), 16))
                print(f"Received from client: {decrypted_message}")

                response = message_handler(decrypted_message)

                encrypted_response = Encoding.Encrypt(response, int(self.shared_key.hex(), 16))
                self.connection.sendall(encrypted_response.encode('utf-8'))

        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.exit_server()

# Shuts down the server, closes client connection, and stops the socket
    def exit_server(self):
        print("Shutting down server...")
        self.running = False
        if self.connection:
            self.connection.close()
        self.server_socket.close()
        print("Server stopped.")
        sys.exit(0)
