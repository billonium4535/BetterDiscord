import pygame
import socket
import zlib
import mss
import pygetwindow
import threading


# Server configuration 82.20.26.36/127.0.0.1
server_ip = "127.0.0.1"
server_port = 8446
window_title = "Netflix - Opera"
screen_top = 100
screen_left = 100

# Socket setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.settimeout(0.1)

print(f"Attempting to connect to {server_ip}:{server_port}")

client_socket.connect((server_ip, server_port))

print("Connected")


def get_window_position_and_size(title):
    try:
        # print("a")
        window = pygetwindow.getWindowsWithTitle(title)  # FAILS HERE
        # print("b")
        if window:
            # print("c")
            window = window[0]
            # print("d")
            return {'top': window.top, 'left': window.left, 'width': window.width, 'height': window.height}
        else:
            print(f"Window with title '{title}' not found.")
            return None
    except IndexError:
        print(f"Window with title '{title}' not found.")
        return None


def record_screen():
    while True:
        # print("1")
        rect = get_window_position_and_size(window_title)
        # print("2")
        screenshot = mss.mss().grab(rect)
        # print("3")
        pixels = zlib.compress(screenshot.rgb, 5)
        data_size = len(pixels).to_bytes(4, 'big')
        screen_values = f"{rect['width']},{rect['height']}"
        client_socket.send(screen_values.encode('windows-1252'))
        client_socket.send(data_size)
        client_socket.send(pixels)
        print(f"Sent {len(pixels)} bytes to the server")


def receive_screen():
    print("a")
    screen_values_bytes = client_socket.recv(1024)  # FAILS HERE
    print("b")
    if not screen_values_bytes:
        return None
    received_values = screen_values_bytes.decode().split(",")
    received_width = int(received_values[0])
    received_height = int(received_values[1])
    data_size_bytes = client_socket.recv(4)
    if not data_size_bytes:
        return None
    data_size = int.from_bytes(data_size_bytes, 'big')
    received_data = b""
    while len(received_data) < data_size:
        chunk = client_socket.recv(4096)
        if not chunk:
            return None
        received_data += chunk
    return received_data, received_width, received_height


def display_screen():
    default_screen_width = 100
    default_screen_height = 100
    fps = 30
    pygame.init()
    clock = pygame.time.Clock()
    watching = True

    screen = pygame.display.set_mode((default_screen_width, default_screen_height))

    while watching:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                watching = False
                break

        # record_screen()

        print("1")

        try:

            pixels, screen_width, screen_height = receive_screen()

            print("1.1")

            if pixels is None:
                print("Error receiving screen data.")
                break

            pixels = zlib.decompress(pixels)

            print("1.2")

            # Ensure that the length of pixels matches the expected size for (100, 100) resolution and 'RGB' format
            expected_size = screen_width * screen_height * 3
            if len(pixels) != expected_size:
                raise ValueError(f"Expected {expected_size} bytes, but got {len(pixels)} bytes")

            print("2")

            # Create the Surface from raw pixels
            img = pygame.image.fromstring(pixels, (screen_width, screen_height), 'RGB')

            if screen.get_width() != screen_width or screen.get_height() != screen_height:
                screen = pygame.display.set_mode((screen_width, screen_height))

            print("3")

            # Display the picture
            screen.blit(img, (0, 0))
        except:
            pass
        print("4")
        pygame.display.flip()
        print("5")
        clock.tick(fps)
        print("6")

    pygame.quit()


def main():
    # display_screen()

    capture_send_thread = threading.Thread(target=record_screen)
    receive_display_thread = threading.Thread(target=display_screen)

    capture_send_thread.start()
    receive_display_thread.start()

    # Wait for the threads to finish
    capture_send_thread.join()
    receive_display_thread.join()

    # Close the socket
    client_socket.close()


main()
