import pygame
from constants import *
from colors import *


class MainWindowGUI:
    def __init__(self):
        self.screen = pygame.display

        self.voice_channel_1_box = pygame.Rect(5, 5, 150, 25)
        self.voice_channel_1_box_hover = False

        self.init_display()
        self.run()

    def init_display(self):
        self.screen.set_mode((min_width, min_height))
        self.screen.set_caption("Better Discord")
        self.screen.get_surface().fill(colors["discord-dark"])
        self.screen.set_icon(pygame.image.load("./Icons/window_icon.png"))

    def draw_voice_channels(self):
        # vc box
        if not self.voice_channel_1_box_hover:
            pygame.draw.rect(self.screen.get_surface(), colors["discord-dark"], self.voice_channel_1_box, border_radius=10)
        else:
            pygame.draw.rect(self.screen.get_surface(), colors["discord-divider"], self.voice_channel_1_box, border_radius=10)

        # Outline box
        pygame.draw.rect(self.screen.get_surface(), colors["white"], (5, 5, 150, 250), 2, border_radius=10)

        # vc text
        voice_channel_1_surface = font.render("Voice Channel 1", True, colors["discord-text"])
        voice_channel_1_rect = voice_channel_1_surface.get_rect().center = (35, 10)
        self.screen.get_surface().blit(voice_channel_1_surface, voice_channel_1_rect)

        # vc icon
        self.screen.get_surface().blit(pygame.transform.scale(pygame.image.load("./Icons/voice_channel.png"), (17, 17)), (15, 10))

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event)

            self.draw_voice_channels()
            self.handle_mouse_position()

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()

    def handle_mouse_click(self, event):
        pass

    def handle_mouse_position(self):
        if self.voice_channel_1_box.collidepoint(pygame.mouse.get_pos()):
            self.voice_channel_1_box_hover = True
        else:
            self.voice_channel_1_box_hover = False


MainWindowGUI()
