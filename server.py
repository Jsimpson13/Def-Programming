import socket
import ssl
import threading

def handle_client(conn, addr):
    """
    Handles communication with a connected client.
    
    Parameters:
        conn (ssl.SSLSocket): The SSL-wrapped client socket.
        addr (tuple): The address of the connected client.
    """
    print(f"Connection from {addr}")
    try:
    	while True:
            data = conn.recv(1024).decode('utf-8')  # Receive data from client
            if not data:
            	break  # Exit loop if client disconnects
            if (data=="bye"):
            	print("client left \nWaiting for a new connection")
            	break
            print(f"Client: {data}")
            
            message = input("Server: ")  # Prompt server operator for response
            conn.send(message.encode('utf-8'))  # Send response to client
    except Exception as e:
        print(f"Error: {e}")  # Handle exceptions gracefully
    finally:
        conn.close()  # Ensure the connection is closed

def main():
    """
    Initializes and runs a secure chat server using SSL.
    """
    host = '127.0.0.1'  # Localhost address
    port = 12345  # Port number for the server
    
    # Create a standard TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Wrap the socket with SSL encryption
    secure_socket = ssl.wrap_socket(
        server_socket,
        server_side=True,
        certfile="server_cert.pem",  # Path to the server certificate
        keyfile="server_key.pem",  # Path to the server private key
        ssl_version=ssl.PROTOCOL_TLS  # Use TLS for secure communication
    )
    
    secure_socket.bind((host, port))  # Bind the socket to the address and port
    secure_socket.listen(5)  # Listen for incoming connections (up to 5 clients in queue)
    print(f"Secure chat server started on {host}:{port}")
    
    while True:
        conn, addr = secure_socket.accept()  # Accept a client connection
        threading.Thread(target=handle_client, args=(conn, addr)).start()  # Handle client in a new thread

if __name__ == '__main__':
    main()
