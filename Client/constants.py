import pygame
from colors import colors

# Initialize Pygame
pygame.init()

# Font settings
FONT_SIZE = 15
font = pygame.font.Font("./Fonts/arial.ttf", FONT_SIZE)
font.set_italic(True)


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
input_box = pygame.Rect(input_margin, (screen.get_height() - input_height - input_bottom_margin), (screen.get_width() - (input_margin * 2)), input_height)
input_color_inactive = pygame.Color(colors["discord-message-box"])
input_color_active = pygame.Color(colors["discord-message-box"])
input_text = ""

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
