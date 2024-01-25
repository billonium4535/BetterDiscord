import pygame

from GUI import MainWindowGUI
from updater import UpdaterWindowGUI


if __name__ == "__main__":
    pygame.init()
    UpdaterWindowGUI()
    MainWindowGUI()
