import pygame

from GUI import MainWindowGUI
from updater import UpdaterWindowGUI
from constants import check_client_exit, client_init


if __name__ == "__main__":
    pygame.init()
    client_init()
    UpdaterWindowGUI()
    if not check_client_exit():
        MainWindowGUI()
