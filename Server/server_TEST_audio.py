import socket
import pyaudio

p = pyaudio.PyAudio()

chunk_size = 1024
sample_format = pyaudio.paInt16
channels = 1
sample_rate = 44100

# Open stream for playback
stream_out = p.open(format=sample_format,
                    channels=channels,
                    rate=sample_rate,
                    output=True,
                    frames_per_buffer=chunk_size)


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
    data = client_socket.recv(1024)
    client_socket.send(data)
