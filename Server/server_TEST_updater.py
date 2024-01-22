import socket

# Server configuration
server_ip = "0.0.0.0"
server_port = 8446

CURRENT_CLIENT_VERSION = "1.0"


def send_files(client_socket):
    file_paths = [
        "../Client/client_class.py",
        "../Client/colors.py",
        "../Client/constants.py"
    ]

    for file_path in file_paths:
        with open(file_path, "rb") as file:
            file_content = file.read()
            client_socket.sendall(file_content)


def main():
    # Socket setup
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(10)

    print(f"Server listening on {server_ip}:{server_port}")

    # Accept connection from client
    client_socket, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    while True:
        # Send current version to the client
        client_socket.sendall(CURRENT_CLIENT_VERSION.encode())

        # Receive client version
        client_version = client_socket.recv(1024).decode()

        if client_version != CURRENT_CLIENT_VERSION:
            print(f"Client version mismatch: {client_version} (client) != {CURRENT_CLIENT_VERSION} (server)")
            client_socket.sendall(b'UPDATE')

            # Send updated files to the client
            send_files(client_socket)
        else:
            print("Client is up to date.")
            client_socket.sendall(b'NO_UPDATE')


main()
