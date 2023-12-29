import socket
import threading

SERVER_HOST = '82.20.26.36'
SERVER_PORT = 8446


def receive_messages(client_socket):
    try:
        while True:
            # Receive and print messages from the server
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Received message from {client_socket.getpeername()[0]}: {data.decode('utf-8')}")
    except ConnectionResetError:
        print("Connection with the server closed.")


def start_client():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print(f"Attempting to connect to {SERVER_HOST}:{SERVER_PORT}")

    # Connect to the server
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # Start a separate thread for receiving messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    print("Enter a message (or 'exit' to quit):")

    try:
        while True:
            # Get user input and send it to the server
            message = input(">")
            if message.lower() == 'exit':
                break

            # Send the message to the server
            client_socket.send(message.encode('utf-8'))

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the client socket when done
        client_socket.close()


if __name__ == "__main__":
    start_client()
