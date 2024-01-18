import socket

# Server configuration
server_ip = "0.0.0.0"
server_port = 8446

# Socket setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(10)

print(f"Server listening on {server_ip}:{server_port}")

# Accept connection from client
client_socket, client_address = server_socket.accept()
print(f"Connection established with {client_address}")

while True:
    screen_values_bytes = client_socket.recv(1024)
    if not screen_values_bytes:
        print("Client disconnected")
        break
    data_size_bytes = client_socket.recv(4)
    if not data_size_bytes:
        print("Error receiving data size")
        break
    data_size = int.from_bytes(data_size_bytes, 'big')
    received_data = b""
    while len(received_data) < data_size:
        chunk = client_socket.recv(4096)
        if not chunk:
            print("Error receiving data chunk")
            break
        received_data += chunk
    print(f"Received {len(received_data)} bytes from the client")

    client_socket.send(screen_values_bytes)
    client_socket.send(len(received_data).to_bytes(4, 'big'))
    client_socket.send(received_data)
