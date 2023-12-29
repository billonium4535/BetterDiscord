import socket

SERVER_HOST = '82.20.26.36'
SERVER_PORT = 8446


def start_client():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print(f"Attempting to connect to {SERVER_HOST}:{SERVER_PORT}")

    # Connect to the server
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    while True:
        # Get user input and send it to the server
        message = input("Enter a message (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break

        # Send the message to the server
        client_socket.send(message.encode('utf-8'))

    # Close the client socket when done
    client_socket.close()


if __name__ == "__main__":
    start_client()
