from pygame.locals import *
import socket
import threading
from constants import *


class ClientApp:
    def __init__(self):
        # Create a socket object
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Create threads
        self.receive_thread = threading.Thread(target=self.receive_messages)

        self.init_display()
        self.init_socket()

        self.chat_text = []
        self.input_active = False
        self.input_text = ""

        self.run()

    def init_display(self):
        # Set up the Pygame window
        screen.fill(colors["discord-dark"])

    def init_socket(self):
        # Socket settings
        # 82.20.26.36/127.0.0.1
        SERVER_HOST = "82.20.26.36"
        SERVER_PORT = 8446

        # Connect to the server
        self.client_socket.connect((SERVER_HOST, SERVER_PORT))

        # Start a separate thread for receiving messages
        self.receive_thread.start()

    def receive_messages(self):
        try:
            while True:
                # Receive and print messages from the server
                data = self.client_socket.recv(1024)
                if not data:
                    break

                chat_int = 0
                received_message = data.decode('windows-1252')
                while chat_int < len(received_message.split("\r\n")):
                    self.chat_text.append(received_message.split("\r\n")[chat_int])
                    chat_int += 1

        except ConnectionResetError:
            print("Connection with the server closed.")
        except OSError:
            print("Connection with the server closed.")

    def draw_input_box(self):
        # Draw the input box
        input_box.y = screen.get_height() - input_height - input_bottom_margin
        pygame.draw.rect(screen, input_color_active if self.input_active else input_color_inactive, input_box, 20, 7)

        # Draw the flashing cursor
        if self.input_active:
            flash_timer = pygame.time.get_ticks() // 500
            if flash_timer % 2 == 0:  # Flash the cursor on/off
                cursor_color = colors["discord-text"]
                cursor_surface = font.render("|", True, cursor_color)
                cursor_pos = (input_box.x + 10 + font.size(self.input_text)[0], input_box.y + 12)
                screen.blit(cursor_surface, cursor_pos)

        # Render the input text
        input_surface = font.render(self.input_text, True, colors["discord-text"])
        screen.blit(input_surface, (input_box.x + 10, input_box.y + 13))

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.client_socket.close()
                    running = False
                elif event.type == VIDEORESIZE:
                    self.handle_resize(event)
                elif event.type == MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event)
                elif event.type == KEYDOWN:
                    self.handle_keypress(event)

            self.init_display()

            # Draw the chat box
            chat_box.y = screen.get_height() - chat_height - chat_bottom_margin
            pygame.draw.rect(screen, chat_color, chat_box)
            message_y_pos = 10
            for message in self.chat_text:
                chat_surface = font.render(message, True, colors["discord-text"])
                screen.blit(chat_surface, (chat_margin, ((chat_box.y + (channel_name_height + channel_name_top_margin)) + message_y_pos)))
                message_y_pos += 15

            # Draw the input box
            self.draw_input_box()

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

    def handle_resize(self, event):
        # screen = pygame.display.set_mode(event.dict['size'], HWSURFACE | DOUBLEBUF | RESIZABLE)
        input_box.width = event.dict['w'] - 2 * input_margin
        chat_box.width = event.dict['w'] - 2 * chat_margin

    def handle_mouse_click(self, event):
        if input_box.collidepoint(event.pos):
            self.input_active = True
        else:
            self.input_active = False

    def handle_keypress(self, event):
        if self.input_active:
            if event.key == K_RETURN:
                if self.input_text:
                    self.client_socket.send(self.input_text.encode('windows-1252'))
                    self.input_text = ''
            elif event.key == K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                self.input_text += event.unicode


if __name__ == "__main__":
    app = ClientApp()
