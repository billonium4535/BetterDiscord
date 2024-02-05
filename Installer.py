import requests
import os
import zipfile


def download_latest_version():
    response = requests.get("http://127.0.0.1:8459")
    if response.status_code == 200:
        with open("BetterDiscord.zip", "wb") as file:
            file.write(response.content)
        print("Downloaded")
    else:
        print("Failed")


def extract_zip(zip_file_path, extract_to):
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)


download_latest_version()
if os.path.exists("./BetterDiscord.zip"):
    extract_zip("./BetterDiscord.zip", "./BetterDiscord")
    os.remove("./BetterDiscord.zip")
