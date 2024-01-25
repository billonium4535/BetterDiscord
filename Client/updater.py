import math
import pygame.draw

from constants import init_font
from colors import *


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

        self.downloaded_data_size = 0

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
            if not self.handle_server_connection_check():
                self.draw_connecting_screen()
            elif not self.check_current_version():
                self.update_client()
                self.draw_updating_screen()
            else:
                self.running = False

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()

    def handle_server_connection_check(self):
        # Simulate waiting for a server connection
        if pygame.time.get_ticks() >= 5000:
            self.connected_to_server = True
        return self.connected_to_server

    def check_current_version(self):
        # if self.current_version = server_version:
        return self.up_to_date

    def update_client(self):
        # Simulate updating client
        if pygame.time.get_ticks() >= 10000:
            self.up_to_date = True

    def handle_mouse_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
