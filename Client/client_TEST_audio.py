import socket
import pyaudio
import numpy as np
import threading


chunk_size = 1024
sample_format = pyaudio.paInt16
channels = 1
sample_rate = 44100
threshold = 500
RawAudio = True

p = pyaudio.PyAudio()

# Open stream for recording
stream_in = p.open(format=sample_format,
                   channels=channels,
                   rate=sample_rate,
                   input=True,
                   frames_per_buffer=chunk_size)

# Open stream for playback
stream_out = p.open(format=sample_format,
                    channels=channels,
                    rate=sample_rate,
                    output=True,
                    frames_per_buffer=chunk_size)

# Server configuration 82.20.26.36/127.0.0.1
server_ip = "127.0.0.1"
server_port = 8446

# Socket setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(f"Attempting to connect to {server_ip}:{server_port}")

client_socket.connect((server_ip, server_port))

print("Connected")


# Function to handle recording audio
def record_audio():
    while True:
        input_data = stream_in.read(chunk_size)
        input_array = np.frombuffer(input_data, dtype=np.int16)

        audio_level = np.abs(input_array).mean()

        # Check if the audio level exceeds the threshold
        if RawAudio or (not RawAudio and audio_level > threshold):
            # Send the audio
            client_socket.send(input_data)


# Function to handle playing audio
def play_audio():
    while True:
        output_data = client_socket.recv(1024)
        stream_out.write(output_data)


# Start recording and playing audio in separate threads
record_thread = threading.Thread(target=record_audio)
play_thread = threading.Thread(target=play_audio)

record_thread.start()
play_thread.start()

# Wait for both threads to finish
record_thread.join()
play_thread.join()

# except KeyboardInterrupt:
#     pass
#
# finally:
#     # Stop and close the streams
#     stream_in.stop_stream()
#     stream_in.close()
#     # stream_out.stop_stream()
#     # stream_out.close()
#
#     # Terminate PyAudio
#     p.terminate()
