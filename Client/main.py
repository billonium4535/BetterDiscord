import pygame
import subprocess
import os
import time

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


def check_natural_client_exit():
    if os.path.exists("./CLIENT_NATURAL_QUIT"):
        client_quit = True
        os.remove("./CLIENT_NATURAL_QUIT")
    else:
        client_quit = False

    return client_quit


if __name__ == "__main__":
    pygame.init()
    client_init()
    if os.path.exists("./updater.exe"):
        subprocess.run("./updater.exe", check=True)
        while not check_client_exit() or not check_natural_client_exit():
            time.sleep(3)
        if os.path.exists("./GUI.exe"):
            subprocess.run("./GUI.exe", check=True)
        else:
            MainWindowGUI()
    else:
        UpdaterWindowGUI()
        if os.path.exists("./GUI.exe"):
            subprocess.run("./GUI.exe", check=True)
        else:
            MainWindowGUI()
