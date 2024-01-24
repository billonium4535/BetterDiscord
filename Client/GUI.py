from constants import *
from colors import *


class MainWindowGUI:
    def __init__(self):
        self.screen = pygame.display

        self.mouse_down = False
        self.running = True
        self.debouncer = False

        self.voice_channel_1_box = pygame.Rect(5, 5, 150, 25)
        self.voice_channel_1_box_hover = False

        self.threshold = 500
        self.max_threshold = 1000

        self.slider_width = 200
        self.slider_circle_x = (self.threshold / self.max_threshold) * 188  # max 188
        self.circle_radius = 6
        self.dragging = False

        self.muted = False
        self.mute_button = pygame.Rect(5, 325, 45, 25)
        self.mute_button_hover = False

        self.deafaned = False
        self.deafan_button = pygame.Rect(57.5, 325, 45, 25)
        self.deafan_button_hover = False

        self.in_call = False
        self.leave_call_button = pygame.Rect(110, 325, 45, 25)
        self.leave_call_button_hover = False

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
        pygame.draw.rect(self.screen.get_surface(), colors["white"], (5, 5, 150, 300), 2, border_radius=10)

        # vc text
        voice_channel_1_surface = font.render("Voice Channel 1", True, colors["discord-text"])
        voice_channel_1_rect = voice_channel_1_surface.get_rect().center = (35, 10)
        self.screen.get_surface().blit(voice_channel_1_surface, voice_channel_1_rect)

        # vc icon
        self.screen.get_surface().blit(pygame.transform.scale(pygame.image.load("./Icons/voice_channel.png"), (17, 17)), (15, 10))

    def draw_input_sensitivity_slider(self):
        pygame.draw.rect(self.screen.get_surface(), colors["white"], (100, 375, self.slider_width, 12), border_radius=10)
        pygame.draw.circle(self.screen.get_surface(), colors["red"], (106 + self.slider_circle_x, 381), 6)

    def draw_call_buttons(self):

        if not self.mute_button_hover:
            pygame.draw.rect(self.screen.get_surface(), colors["discord-message-box"], self.mute_button, border_radius=10)
        else:
            pygame.draw.rect(self.screen.get_surface(), colors["discord-divider"], self.mute_button, border_radius=10)

        if self.muted:
            self.screen.get_surface().blit(pygame.transform.scale(pygame.image.load("./Icons/mic_mute.png"), (17, 17)), (18, 328))
        else:
            self.screen.get_surface().blit(pygame.transform.scale(pygame.image.load("./Icons/mic_unmute.png"), (17, 17)), (18, 328))

        if not self.deafan_button_hover:
            pygame.draw.rect(self.screen.get_surface(), colors["discord-message-box"], self.deafan_button, border_radius=10)
        else:
            pygame.draw.rect(self.screen.get_surface(), colors["discord-divider"], self.deafan_button, border_radius=10)

        if self.deafaned:
            self.screen.get_surface().blit(pygame.transform.scale(pygame.image.load("./Icons/deafen.png"), (17, 17)), (70, 328))
        else:
            self.screen.get_surface().blit(pygame.transform.scale(pygame.image.load("./Icons/undeafen.png"), (17, 17)), (70, 328))

        if not self.leave_call_button_hover:
            pygame.draw.rect(self.screen.get_surface(), colors["discord-message-box"], self.leave_call_button, border_radius=10)
        else:
            pygame.draw.rect(self.screen.get_surface(), colors["discord-divider"], self.leave_call_button, border_radius=10)

        self.screen.get_surface().blit(pygame.transform.scale(pygame.image.load("./Icons/leave_call.png"), (17, 17)), (126, 329))

    def run(self):
        self.running = True
        clock = pygame.time.Clock()

        while self.running:
            self.handle_mouse_events()
            self.handle_mouse_click()
            self.handle_mouse_position()

            self.draw_voice_channels()
            self.draw_input_sensitivity_slider()
            self.draw_call_buttons()

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()

    def handle_mouse_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_down = False
                self.debouncer = False

    def handle_mouse_click(self):
        if self.mouse_down:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Threshold slider
            circle_center = (106 + self.slider_circle_x, 381)
            if circle_center[0] - self.circle_radius <= mouse_x <= circle_center[0] + self.circle_radius:
                self.dragging = True
            if self.dragging:
                self.slider_circle_x = max(0, min(188, mouse_x - 106))

            # Call buttons
            if not self.debouncer:
                if self.mute_button.collidepoint(pygame.mouse.get_pos()):
                    if not self.deafaned:
                        self.muted = not self.muted
                    self.debouncer = True
                if self.deafan_button.collidepoint(pygame.mouse.get_pos()):
                    if self.deafaned:
                        self.deafaned = False
                        self.muted = False
                    else:
                        self.deafaned = True
                        self.muted = True
                    self.debouncer = True
                if self.leave_call_button.collidepoint(pygame.mouse.get_pos()):
                    self.debouncer = True
        else:
            self.dragging = False
        self.threshold = round(0 + (self.max_threshold - 0) * (((self.slider_circle_x / 188) * 100) / 100.0))

    def handle_mouse_position(self):
        if self.voice_channel_1_box.collidepoint(pygame.mouse.get_pos()):
            self.voice_channel_1_box_hover = True
        else:
            self.voice_channel_1_box_hover = False

        if self.mute_button.collidepoint(pygame.mouse.get_pos()):
            self.mute_button_hover = True
        else:
            self.mute_button_hover = False

        if self.deafan_button.collidepoint(pygame.mouse.get_pos()):
            self.deafan_button_hover = True
        else:
            self.deafan_button_hover = False

        if self.leave_call_button.collidepoint(pygame.mouse.get_pos()):
            self.leave_call_button_hover = True
        else:
            self.leave_call_button_hover = False


MainWindowGUI()
