import socket
import ssl
def client_main():
    """
    Initializes and runs a secure chat client using SSL.
    """
    host = '127.0.0.1'  # Server address
    port = 12345  # Server port number
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    secure_socket = ssl.wrap_socket(
        client_socket,
        certfile="client_cert.pem",  # Path to the client certificate
        keyfile="client_key.pem",  # Path to the client private key
        ssl_version=ssl.PROTOCOL_TLS  # Use TLS for secure communication
    )
    
    secure_socket.connect((host, port))
    print("Connected to the secure chat server.")
    
    try:
        while True:
            message = input("Client: ")
            if(message!="bye"):
                secure_socket.send(message.encode('utf-8'))  # Send message to server
                data = secure_socket.recv(1024).decode('utf-8')  # Receive response from server
                print(f"Server: {data}")
            else:
                print("Connection Closed")
                secure_socket.close()
    except Exception as e:
        print(f"Error: {e}")  # Handle exceptions gracefully
    finally:
        secure_socket.close()  # Ensure the connection is closed

if __name__ == '__main__':
    client_main()
