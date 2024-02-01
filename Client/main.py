import pygame
import subprocess
import os

from GUI import MainWindowGUI
from updater import UpdaterWindowGUI

running = True


def client_init():
    if os.path.exists("./CLIENT_QUIT"):
        os.remove("./CLIENT_QUIT")


def check_client_exit():
    if os.path.exists("./CLIENT_QUIT"):
        client_quit = True
        os.remove("./CLIENT_QUIT")
    else:
        client_quit = False

    return client_quit


if __name__ == "__main__":
    pygame.init()
    client_init()
    if os.path.exists("./updater.exe"):
        subprocess.run("./updater.exe", check=True)
    else:
        UpdaterWindowGUI()
        if not check_client_exit():
            MainWindowGUI()
