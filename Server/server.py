from pathlib import Path
import sys
project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root))
import socket
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives import serialization
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

    def start(self):
        Db.createDB()
        """Starts the server and waits for a client connection."""
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print(f"Server listening on {self.host}:{self.port}...")

        self.connection, self.client_address = self.server_socket.accept()
        print(f"Connection established with {self.client_address}")

        self.perform_key_exchange()

    def perform_key_exchange(self):
        """Performs the Diffie-Hellman key exchange."""
        parameters = dh.generate_parameters(generator=2, key_size=512)
        server_private_key = parameters.generate_private_key()
        server_public_key = server_private_key.public_key()

        # Send parameters and public key to the client
        server_parameters_bytes = parameters.parameter_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.ParameterFormat.PKCS3
        )
        server_public_bytes = server_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        self.connection.sendall(server_parameters_bytes)
        self.connection.sendall(server_public_bytes)

        # Receive client's public key
        client_public_bytes = self.connection.recv(4096)
        client_public_key = serialization.load_pem_public_key(client_public_bytes)

        # Compute shared key
        shared_key = server_private_key.exchange(client_public_key)

        # Derive symmetric key
        self.shared_key = HKDF(
            algorithm=SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
        ).derive(shared_key)

        print("Key exchange successful. Secure communication established.")

    def handle_messages(self, message_handler):
        """
        Forwards received messages to the `message_handler` function in `main.py`.
        """
        try:
            while self.running:
                client_message = self.connection.recv(10000).decode('utf-8')
                if not client_message:
                    continue

                if client_message.lower() == "exit":
                    self.exit_server()
                    break

                # Decrypt message
                decrypted_message = Decrypt.DECS(client_message, int(self.shared_key.hex(), 16))
                print(f"Received from client: {decrypted_message}")

                # Pass the message to the handler in `main.py`
                response = message_handler(decrypted_message)

                # Encrypt and send response
                encrypted_response = Encoding.Encrypt(response, int(self.shared_key.hex(), 16))
                self.connection.sendall(encrypted_response.encode('utf-8'))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.exit_server()

    def exit_server(self):
        """Gracefully shuts down the server."""
        print("Shutting down server...")
        self.running = False
        if self.connection:
            self.connection.close()
        self.server_socket.close()
        print("Server stopped.")
