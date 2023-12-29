import socket
import threading

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8446


def handle_client(client_socket):
    while True:
        # Receive data from the client
        data = client_socket.recv(1024)
        if not data:
            break

        # Print the received message
        print(f"Received message from {client_socket.getpeername()}: {data.decode('utf-8')}")

    # Close the client socket when the connection is terminated
    client_socket.close()


def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind((SERVER_HOST, SERVER_PORT))

    # Listen for incoming connections (maximum of 5)
    server_socket.listen(5)
    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        # Accept a connection from a client
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")

        # Start a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    start_server()
