import pygame
import subprocess
import os
import time
import ipaddress

import GUI
import updater

running = True


def client_init():
    if os.path.exists("./CLIENT_QUIT"):
        os.remove("./CLIENT_QUIT")


def check_client_exit():
    if os.path.exists("./CLIENT_QUIT"):
        os.remove("./CLIENT_QUIT")
        exit()
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


def check_for_server_details(file_path):
    if os.path.exists(file_path):
        try:
            ipaddress.ip_address(next(open(file_path), "").strip())
            return True
        except ValueError:
            return False
    else:
        return False


if __name__ == "__main__":
    pygame.init()
    client_init()
    if check_for_server_details("./SERVER_DETAILS.cfg"):
        if os.path.exists("./updater.exe"):
            subprocess.run("./updater.exe", check=True)
            while not check_client_exit() and not check_natural_client_exit():
                time.sleep(3)
            if os.path.exists("./GUI.exe"):
                subprocess.run("./GUI.exe", check=True)
            else:
                GUI.MainWindowGUI()
        else:
            updater.UpdaterWindowGUI()
            while not check_client_exit() and not check_natural_client_exit():
                time.sleep(3)
            if os.path.exists("./GUI.exe"):
                subprocess.run("./GUI.exe", check=True)
            else:
                GUI.MainWindowGUI()
