from constants import *
from colors import *
from audio import get_audio_input_devices, get_audio_output_devices


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

        self.slider_width = 150
        self.slider_circle_x = (self.threshold / self.max_threshold) * 138  # max 138
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

        self.input_devices = get_audio_input_devices()
        self.output_devices = get_audio_output_devices()
        self.input_device_dropdown = pygame.Rect(175, 5, 200, 25)
        self.output_device_dropdown = pygame.Rect(175, 45, 200, 25)
        self.input_selected_device = None
        self.output_selected_device = None
        self.input_open = False
        self.output_open = False
        self.scroll_offset_input = 0
        self.scroll_offset_output = 0

        self.init_display()
        self.run()

    def init_display(self):
        self.screen.set_mode((min_width, min_height))
        self.screen.set_caption("Better Discord")
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
        pygame.draw.rect(self.screen.get_surface(), colors["white"], (5, 375, self.slider_width, 12), border_radius=10)
        pygame.draw.circle(self.screen.get_surface(), colors["red"], (11 + self.slider_circle_x, 381), 6)

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

    def draw_devices_dropdown(self):
        pygame.draw.rect(self.screen.get_surface(), colors["white"], self.input_device_dropdown, border_radius=10)
        pygame.draw.rect(self.screen.get_surface(), colors["white"], self.output_device_dropdown, border_radius=10)

        if self.input_open:
            pygame.draw.rect(self.screen.get_surface(), colors["white"], (175, 5, 200, 25 * min(len(self.input_devices) + 1, 6)), border_radius=10)
            for i, (name, index) in enumerate(self.input_devices[self.scroll_offset_input:self.scroll_offset_input + 5]):
                self.screen.get_surface().blit(font.render(name, True, colors["discord-dark"]), (180, 35 + (25 * i)))
            pygame.draw.rect(self.screen.get_surface(), colors["grey"], (175, 10, 5, 140), border_radius=10)
            scroll_indicator_height = 140 / len(self.input_devices) * 5
            scroll_indicator_pos = (140 - scroll_indicator_height) * (self.scroll_offset_input / (len(self.input_devices) - 5))
            pygame.draw.rect(self.screen.get_surface(), colors["black"], pygame.Rect(175, 10 + scroll_indicator_pos, 5, scroll_indicator_height), border_radius=10)

        if self.output_open:
            pygame.draw.rect(self.screen.get_surface(), colors["white"], (175, 45, 200, 25 * min(len(self.output_devices) + 1, 6)), border_radius=10)
            for i, (name, index) in enumerate(self.output_devices[self.scroll_offset_output:self.scroll_offset_output + 5]):
                self.screen.get_surface().blit(font.render(name, True, colors["discord-dark"]), (180, 75 + (25 * i)))
            pygame.draw.rect(self.screen.get_surface(), colors["grey"], (175, 50, 5, 140), border_radius=10)
            scroll_indicator_height = 140 / len(self.input_devices) * 5
            scroll_indicator_pos = (140 - scroll_indicator_height) * (self.scroll_offset_output / (len(self.output_devices) - 5))
            pygame.draw.rect(self.screen.get_surface(), colors["black"], pygame.Rect(175, 50 + scroll_indicator_pos, 5, scroll_indicator_height), border_radius=10)

        if self.input_selected_device:
            self.screen.get_surface().blit(font.render(self.input_selected_device[0], True, colors["discord-dark"]), (180, 7))

        if self.output_selected_device and not self.input_open:
            self.screen.get_surface().blit(font.render(self.output_selected_device[0], True, colors["discord-dark"]), (180, 47))

    def run(self):
        self.running = True
        clock = pygame.time.Clock()

        while self.running:
            self.screen.get_surface().fill(colors["discord-dark"])
            self.handle_mouse_events()

            # if self.mouse_down:
            self.handle_mouse_click()
            self.handle_mouse_position()

            self.draw_voice_channels()
            self.draw_input_sensitivity_slider()
            self.draw_call_buttons()
            self.draw_devices_dropdown()

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()

    def handle_mouse_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_down = True
                elif event.button == 4:
                    self.handle_scroll(-1)
                elif event.button == 5:
                    self.handle_scroll(1)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_down = False
                self.debouncer = False

    def handle_mouse_click(self):
        if self.mouse_down:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Threshold slider
            circle_center = (11 + self.slider_circle_x, 381)
            if circle_center[0] - self.circle_radius <= mouse_x <= circle_center[0] + self.circle_radius:
                self.dragging = True
            if self.dragging:
                self.slider_circle_x = max(0, min(138, mouse_x - 11))

            # Call buttons
            if not self.debouncer:
                if self.mute_button.collidepoint(mouse_x, mouse_y):
                    if not self.deafaned:
                        self.muted = not self.muted
                    self.debouncer = True
                if self.deafan_button.collidepoint(mouse_x, mouse_y):
                    if self.deafaned:
                        self.deafaned = False
                        self.muted = False
                    else:
                        self.deafaned = True
                        self.muted = True
                    self.debouncer = True
                if self.leave_call_button.collidepoint(mouse_x, mouse_y):
                    self.debouncer = True

                # Dropdowns
                if self.input_device_dropdown.collidepoint(mouse_x, mouse_y) and not self.output_open:
                    self.input_open = not self.input_open
                    self.debouncer = True
                if self.output_device_dropdown.collidepoint(mouse_x, mouse_y) and not self.input_open:
                    self.output_open = not self.output_open
                    self.debouncer = True
                if pygame.Rect(175, 5, 200, 25 * (len(self.input_devices) + 1)).collidepoint(mouse_x, mouse_y) and self.input_open:
                    for i, (name, index) in enumerate(self.input_devices[self.scroll_offset_input:self.scroll_offset_input + 5]):
                        if pygame.Rect(175, 35 + (25 * i), 200, 25).collidepoint(mouse_x, mouse_y):
                            self.input_selected_device = (name, index)
                            self.input_open = False
                            self.debouncer = True
                if pygame.Rect(175, 45, 200, 25 * (len(self.output_devices) + 1)).collidepoint(mouse_x, mouse_y) and self.output_open:
                    for i, (name, index) in enumerate(self.output_devices[self.scroll_offset_output:self.scroll_offset_output + 5]):
                        if pygame.Rect(175, 75 + (25 * i), 200, 25).collidepoint(mouse_x, mouse_y):
                            self.output_selected_device = (name, index)
                            self.output_open = False
                            self.debouncer = True
                if not self.input_device_dropdown.collidepoint(mouse_x, mouse_y) and self.input_open:
                    self.input_open = False
                    self.debouncer = True
                if not self.output_device_dropdown.collidepoint(mouse_x, mouse_y) and self.output_open:
                    self.output_open = False
                    self.debouncer = True
        else:
            self.dragging = False
        self.threshold = round(0 + (self.max_threshold - 0) * (((self.slider_circle_x / 138) * 100) / 100.0))

    def handle_mouse_position(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if self.voice_channel_1_box.collidepoint(mouse_x, mouse_y):
            self.voice_channel_1_box_hover = True
        else:
            self.voice_channel_1_box_hover = False

        if self.mute_button.collidepoint(mouse_x, mouse_y):
            self.mute_button_hover = True
        else:
            self.mute_button_hover = False

        if self.deafan_button.collidepoint(mouse_x, mouse_y):
            self.deafan_button_hover = True
        else:
            self.deafan_button_hover = False

        if self.leave_call_button.collidepoint(mouse_x, mouse_y):
            self.leave_call_button_hover = True
        else:
            self.leave_call_button_hover = False

    def handle_scroll(self, direction):
        if self.input_open:
            self.scroll_offset_input = max(0, min(len(self.input_devices) - 5, self.scroll_offset_input + direction))
        elif self.output_open:
            self.scroll_offset_output = max(0, min(len(self.output_devices) - 5, self.scroll_offset_output + direction))


MainWindowGUI()
