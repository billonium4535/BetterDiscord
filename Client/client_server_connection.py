import socket


def connect_to_server(server_ip, server_port, address_family, socket_kind):
    client_socket = socket.socket(address_family, socket_kind)
    client_socket.connect((server_ip, server_port))
    return client_socket


def send_data(client_socket, data):
    if isinstance(data, str):
        data = data.encode('windows-1252')
    client_socket.send(data)


def receive_files(client_socket, file_paths):
    for file_path in file_paths:
        file_content = client_socket.recv(1024)
        with open(file_path, 'wb') as file:
            file.write(file_content)
