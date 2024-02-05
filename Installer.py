import requests
import os
import zipfile
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading
import time
import base64
from io import BytesIO


# Convert png to gif with (https://convertio.co/png-gif/)
# Convert gif to base64 with (https://base64.guru/converter/encode/image/gif)
icon_base64 = """
R0lGODlhAAIAAvQAAAAAAAAAAAEBAQICAgQEBAUFBQYGBgcHBwgICAkJCQoKCgsLCwwMDA0NDQ4ODg8PDxAQEBERERMTEwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAAAAIf8LWE1QIERhdGFYTVA8P3hwYWNrZXQgYmVnaW49J++7vycgaWQ9J1c1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCc/Pgo8eDp4bXBtZXRhIHhtbG5zOng9J2Fkb2JlOm5zOm1ldGEvJyB4OnhtcHRrPSdJbWFnZTo6RXhpZlRvb2wgMTIuNDAnPgo8cmRmOlJERiB4bWxuczpyZGY9J2h0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMnPgoKIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PScnCiAgeG1sbnM6dGlmZj0naHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8nPgogIDx0aWZmOk9yaWVudGF0aW9uPjE8L3RpZmY6T3JpZW50YXRpb24+CiA8L3JkZjpEZXNjcmlwdGlvbj4KPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg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
"""

icon_data = base64.b64decode(icon_base64)
icon_stream = BytesIO(icon_data)


def set_window_icon(window):
    try:
        icon_image = Image.open(icon_stream)
        icon_photo = ImageTk.PhotoImage(icon_image)
        window.iconphoto(True, icon_photo)
    except tk.TclError as e:
        print(f"Error setting window icon: {e}")
        exit()


def download_latest_version(window, progress_bar, install_button, speed_label):
    try:
        response = requests.get("http://127.0.0.1:8459", stream=True)
        total_size = int(response.headers.get('content-length', 0))
        block_size = 65536
        progress_bar["maximum"] = total_size
        downloaded_size = 0
        start_time = time.time()

        if response.status_code == 200:
            with open("BetterDiscord.zip", "wb") as file:
                for data in response.iter_content(block_size):
                    progress_bar["value"] += len(data)
                    downloaded_size += len(data)
                    file.write(data)
                    if progress_bar["value"] % (block_size * 10) == 0:
                        window.update_idletasks()
                        time.sleep(0.01)

                    elapsed_time = time.time() - start_time
                    download_speed = downloaded_size / (1048576 * elapsed_time)
                    speed_label.config(text=f"Download Speed: {download_speed:.2f} MB/s | {downloaded_size / 1048576:.2f} MB/{total_size / 1048576:.2f} MB")

            if os.path.exists("./BetterDiscord.zip"):
                extract_zip("./BetterDiscord.zip", "./BetterDiscord")
                os.remove("./BetterDiscord.zip")
                messagebox.showinfo("Success", "Installation successful")
                install_button["text"] = "Close"
                install_button["command"] = lambda: close_button_click(window)
                install_button["state"] = tk.NORMAL
                speed_label.config(text="Download Complete")
        else:
            print("Failed")
    except requests.exceptions.ConnectionError:
        print("Server not available")
    except FileNotFoundError:
        print("BetterDiscord.zip does not exist")


def extract_zip(zip_file_path, extract_to):
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)


def check_server_connection():
    try:
        response = requests.get("http://127.0.0.1:8459", timeout=1)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False


def install_button_click(window, progress_bar, install_button, speed_label):
    if check_server_connection():
        install_button["state"] = tk.DISABLED
        download_thread = threading.Thread(target=download_latest_version, args=(window, progress_bar, install_button, speed_label))
        download_thread.start()
    else:
        messagebox.showerror("Error", "Server not available")


def close_button_click(window):
    window.destroy()


def main_window_loop():
    window = tk.Tk()
    window.title("BetterDiscord Installer")
    window.resizable(False, False)
    set_window_icon(window)

    speed_label = tk.Label(window, text="Download Speed: 0 MB/s | 0.00 MB/0.00 MB")
    speed_label.pack(pady=5)

    progress_bar = ttk.Progressbar(window, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=10)

    install_button = tk.Button(window, text="Install", command=lambda: install_button_click(window, progress_bar, install_button, speed_label))
    install_button.pack(pady=10)

    window.mainloop()


main_window_loop()
