import pygame
from pygame.locals import *
import socket
import threading
from colors import colors

# Initialize Pygame
pygame.init()

colors = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "discord-dark": (49, 51, 56),
    "discord-panel": (43, 45, 49),
    "discord-message-box": (56, 58, 64),
    "discord-divider": (38, 40, 44),
    "discord-text": (242, 243, 245)
}

# Font settings
FONT_SIZE = 20
font = pygame.font.Font(None, FONT_SIZE)

screen_info = pygame.display.Info()
min_width, min_height = 400, 400

# Set up the Pygame window
screen = pygame.display.set_mode((screen_info.current_w, (screen_info.current_h - 71)), pygame.RESIZABLE)
pygame.display.set_caption("Better Discord")

# Chat box settings
chat_margin = 300
chat_bottom_margin = 100
chat_height = screen.get_height() - chat_bottom_margin
chat_box = pygame.Rect(chat_margin, (screen.get_height() - chat_height - chat_bottom_margin), (screen.get_width() - (chat_margin * 2)), chat_height)
chat_color = colors["discord-dark"]
chat_text = []

# Text input box settings
input_margin = 300
input_bottom_margin = 20
input_height = 40
input_box = pygame.Rect(input_margin, (screen.get_height() - input_height - input_bottom_margin),
                        (screen.get_width() - (input_margin * 2)), input_height)
input_color_inactive = pygame.Color(colors["discord-message-box"])
input_active = False
input_text = ''
input_surface = font.render(input_text, True, input_color_inactive)

# Channels settings
channel_right_margin = 0
channel_height = screen.get_height()
channel_box = pygame.Rect(0, 0, 250, channel_height)
channel_color = colors["discord-panel"]

# Members settings
member_right_margin = 0
member_height = screen.get_height()
member_box = pygame.Rect((screen.get_width() - 250), 50, 250, channel_height)
member_color = colors["discord-panel"]

# Channel name settings
channel_name_left_margin = 250
channel_name_right_margin = 0
channel_name_top_margin = 0
channel_name_height = 50
channel_name_box = pygame.Rect(channel_name_left_margin, channel_name_top_margin, (screen.get_width() - (channel_name_left_margin + channel_name_right_margin)), channel_name_height)
channel_name_color = colors["discord-dark"]
channel_name_divider_color = colors["discord-divider"]
channel_name_divider_box = pygame.Rect(0, (channel_name_top_margin + channel_name_height), screen.get_width(), 1)
channel_name_text = "# PLACEHOLDER"
channel_name_surface = font.render(channel_name_text, True, colors["discord-text"])
channel_name_rect = channel_name_surface.get_rect()
channel_name_rect.center = ((channel_name_left_margin + 20), (channel_name_height // 2.5))

server_name_surface = font.render("Penguin Mopping", True, colors["discord-text"])
server_name_rect = server_name_surface.get_rect()
server_name_rect.center = (65, 20)

# Socket settings
SERVER_HOST = '82.20.26.36'
SERVER_PORT = 8446

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((SERVER_HOST, SERVER_PORT))


# Start a separate thread for receiving messages
def receive_messages():
    global chat_text
    try:
        while True:
            # Receive and print messages from the server
            data = client_socket.recv(1024)
            if not data:
                break

            chat_int = 0
            received_message = data.decode('windows-1252')
            while chat_int < len(received_message.split("\r\n")):
                chat_text.append(received_message.split("\r\n")[chat_int])
                chat_int += 1

    except ConnectionResetError:
        print("Connection with the server closed.")
    except OSError:
        print("Connection with the server closed.")


receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()


running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            client_socket.close()
            running = False

        # Resize the window
        elif event.type == VIDEORESIZE:
            screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
            input_box.width = event.dict['w'] - 2 * input_margin
            chat_box.width = event.dict['w'] - 2 * chat_margin

        # Check if the mouse click is within the input box
        elif event.type == MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                input_active = True
            else:
                input_active = False

        # Check for key presses
        elif event.type == KEYDOWN:
            if input_active:

                # Check for Enter key press
                if event.key == K_RETURN:
                    # Check if there is text
                    if input_text:
                        # Send text and reset input
                        client_socket.send(input_text.encode('windows-1252'))
                        input_text = ''
                elif event.key == K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

    screen.fill(colors["discord-dark"])

    # Draw the chat box
    chat_box.y = screen.get_height() - chat_height - chat_bottom_margin
    pygame.draw.rect(screen, chat_color, chat_box)
    message_y_pos = 10
    for message in chat_text:
        chat_surface = font.render(message, True, colors["discord-text"])
        screen.blit(chat_surface, (chat_margin, ((chat_box.y + (channel_name_height + channel_name_top_margin)) + message_y_pos)))
        message_y_pos += 15

    # Draw the input box
    input_box.y = screen.get_height() - input_height - input_bottom_margin
    pygame.draw.rect(screen, input_color_inactive, input_box, 20, 7)
    input_surface = font.render(input_text, True, colors["discord-text"])
    screen.blit(input_surface, (input_box.x + 10, input_box.y + 13))

    # Draw the channel box
    pygame.draw.rect(screen, channel_color, channel_box)

    # Draw the members box
    pygame.draw.rect(screen, member_color, member_box)

    # Draw the channel name box
    pygame.draw.rect(screen, channel_name_color, channel_name_box)
    pygame.draw.rect(screen, channel_name_divider_color, channel_name_divider_box)

    # Draw server name text
    screen.blit(server_name_surface, server_name_rect.center)

    # Draw channel name text
    screen.blit(channel_name_surface, channel_name_rect.center)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

pygame.quit()
