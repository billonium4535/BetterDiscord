import socket
import threading

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8446

# List to store connected client sockets
connected_clients = []


def handle_client(client_socket):
    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break

            # Print the received message
            print(f"Received message from {client_socket.getpeername()}: {data.decode('utf-8')}")

            # Broadcast the message to all connected clients except the sender
            broadcast_message(data, client_socket)

    except ConnectionResetError:
        print(f"Connection with {client_socket.getpeername()} closed by client.")
    except OSError:
        print(f"Connection with {client_socket.getpeername()} closed by client.")
    finally:
        # Remove the client socket from the list when the connection is terminated
        connected_clients.remove(client_socket)
        client_socket.close()


def broadcast_message(message, sender_socket):
    # Iterate through the list of connected clients and send the message to each client
    for client in connected_clients:
        # Check if the client is not the sender
        if client != sender_socket:
            try:
                # Send the message to the client
                client.send(message)
            except socket.error:
                # Remove the client socket from the list if there is an error sending the message
                connected_clients.remove(client)


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

        # Add the client socket to the list of connected clients
        connected_clients.append(client_socket)

        # Start a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    start_server()
