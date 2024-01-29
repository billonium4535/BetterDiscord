import math
import pygame.draw
import socket
import threading

from constants import init_font, client_exit
from colors import *
from client_server_connection import connect_to_server


class UpdaterWindowGUI:
    def __init__(self):
        self.screen = pygame.display
        self.screen_width = 400
        self.screen_height = 400

        self.running = True
        self.connected_to_server = False
        self.up_to_date = False
        self.dots = 0
        self.rotation = 0

        # Server configuration 82.20.26.36/127.0.0.1
        self.server_address = "127.0.0.1"

        self.last_saved_tick = 0
        self.downloaded_data_size = 0
        self.updater_socket = connect_to_server(self.server_address, 8457, socket.AF_INET, socket.SOCK_STREAM)

        self.connect_to_server_thread = threading.Thread(target=self.connect_to_server_thread)

        self.current_version = "v1.0"

        self.init_display()
        self.font = init_font()
        self.run()

    def init_display(self):
        self.screen.set_mode((self.screen_width, self.screen_height))
        self.screen.set_caption("Better Discord Updater")
        self.screen.set_icon(pygame.image.load("./Icons/updater_icon.png"))

    def draw_connecting_screen(self):
        points = []
        for i in range(12):
            angle = math.radians(30 * i + self.rotation)
            if i % 2 == 0:
                x_coord = (self.screen_width // 2) + 25 * math.cos(angle)
                y_coord = (self.screen_height // 2) + 25 * math.sin(angle)
            else:
                x_coord = (self.screen_width // 2) + (25 / 2) * math.cos(angle)
                y_coord = (self.screen_height // 2) + (25 / 2) * math.sin(angle)
            points.append((int(x_coord), int(y_coord)))

        for i in range(101):
            angle = math.radians(180) + ((self.rotation * -1) / 20) + (math.radians(180) / 101) * i
            x_coord = (self.screen_width // 2) + 30 * math.cos(angle)
            y_coord = (self.screen_height // 2) + 30 * math.sin(angle)
            pygame.draw.circle(self.screen.get_surface(), colors["white"], (int(x_coord), int(y_coord)), 2)

        pygame.draw.polygon(self.screen.get_surface(), colors["white"], points, 2)

        self.screen.get_surface().blit(self.font.render("Connecting to server" + "." * int(self.dots), True, colors["white"]), ((self.screen_width // 2) - 75, 75))
        self.dots = (self.dots + 0.1) % 4
        self.rotation += 2

    def draw_updating_screen(self):
        for i in range(4):
            angle = math.radians(360 * i / 4 + self.rotation)
            x_coord = (self.screen_width // 2) + 30 * math.cos(angle)
            y_coord = (self.screen_height // 2) + 30 * math.sin(angle)
            pygame.draw.circle(self.screen.get_surface(), colors["white"], (int(x_coord), int(y_coord)), 5)

        self.screen.get_surface().blit(self.font.render("Updating client" + "." * int(self.dots), True, colors["white"]), ((self.screen_width // 2) - 50, 75))
        self.screen.get_surface().blit(self.font.render(f"Downloaded {self.downloaded_data_size}mb", True, colors["white"]), ((self.screen_width // 2) - 60, 100))
        self.dots = (self.dots + 0.1) % 4
        self.rotation += 2

    def run(self):
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            self.screen.get_surface().fill(colors["discord-dark"])
            self.handle_mouse_events()
            if not self.connected_to_server:
                self.handle_server_connection_check()
                self.draw_connecting_screen()
            elif not self.check_current_version():
                self.update_client()
                self.draw_updating_screen()
            else:
                self.running = False

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()

    def connect_to_server_thread(self):
        while self.updater_socket is None and self.running is True:
            self.updater_socket = connect_to_server(self.server_address, 8457, socket.AF_INET, socket.SOCK_STREAM)

    def handle_server_connection_check(self):
        # Simulate waiting for a server connection
        if pygame.time.get_ticks() >= 2500:
            if self.updater_socket is not None:
                self.updater_socket.send("CONNECTION_CHECK".encode('windows-1252'))
                if self.updater_socket.recv(1024).decode('windows-1252') == "200 OK":
                    self.connected_to_server = True
                    self.last_saved_tick = pygame.time.get_ticks()
                else:
                    self.connected_to_server = False
            else:
                if not self.connect_to_server_thread.is_alive():
                    self.connect_to_server_thread.start()

    def check_current_version(self):
        if pygame.time.get_ticks() >= self.last_saved_tick + 2500:
            self.updater_socket.send("GET_VERSION".encode('windows-1252'))
            if self.current_version == self.updater_socket.recv(1024).decode('windows-1252'):
                self.up_to_date = True
            else:
                self.up_to_date = False

            return self.up_to_date

    def update_client(self):
        if not self.up_to_date:
            pass

    def handle_mouse_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client_exit()
                self.running = False
