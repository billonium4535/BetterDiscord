import socket
import os


# Server configuration 82.20.26.36/127.0.0.1
server_ip = "127.0.0.1"
server_port = 8446


def receive_files(client_socket):
    file_paths = [
        "./client_class.py",
        "./colors.py",
        "./constants.py"
    ]

    for file_path in file_paths:
        file_content = client_socket.recv(1024)
        with open(file_path, 'wb') as file:
            file.write(file_content)


def main():
    # Socket setup
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print(f"Attempting to connect to {server_ip}:{server_port}")

    client_socket.connect((server_ip, server_port))

    print("Connected")

    # Receive current version from the server
    current_version = client_socket.recv(1024).decode()
    print(f"Current client version: {current_version}")

    # Send client version to the server
    client_socket.sendall(current_version.encode())

    # Check for update
    update_signal = client_socket.recv(1024)

    if update_signal == b'UPDATE':
        print("Updating client files...")
        receive_files(client_socket)
        print("Update complete.")
    elif update_signal == b'NO_UPDATE':
        print("Client is up to date.")
    else:
        print("Unexpected update signal.")


main()
