import os
import subprocess
import shutil

print("Have you updated the version in 'VERSION' AND 'updater.py' -> 'self.current_version'? (y/n)")
if input(">").strip().lower() != "y":
    exit()


# Make Latest_Version old
def find_highest_version(folder_path):
    files = [file for file in os.listdir(folder_path) if file.startswith("BetterDiscord_v")]

    if not files:
        return f"{folder_path}/BetterDiscord_v0.zip"

    latest_version = max(files)
    latest_value = int(latest_version.split("BetterDiscord_v")[1].split(".")[0])
    next_value = latest_value + 1
    next_version = f"{folder_path}/BetterDiscord_v{next_value}.zip"

    return next_version


if os.path.exists("./Server/Latest_Version/BetterDiscord.zip"):
    os.rename("./Server/Latest_Version/BetterDiscord.zip", find_highest_version("./Server/Latest_Version"))

# Create Latest_Version folder
os.makedirs("./Server/Latest_Version/BetterDiscord")

# Build BetterDiscord.exe
print("Building BetterDiscord.exe")
cmd = [
    "pyinstaller",
    "--noconfirm",
    "--onefile",
    "--windowed",
    "--icon", "./Client/Icons/window_icon.ico",
    "./Client/BetterDiscord.py"
]

subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
shutil.copy2("./dist/BetterDiscord.exe", "./Server/Latest_Version/BetterDiscord")

# Build GUI.exe
print("Building GUI.exe")
cmd = [
    "pyinstaller",
    "--noconfirm",
    "--onefile",
    "--windowed",
    "--icon", "./Client/Icons/window_icon.ico",
    "./Client/GUI.py"
]

subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
shutil.copy2("./dist/GUI.exe", "./Server/Latest_Version/BetterDiscord")

# Build updater.exe
print("Building updater.exe")
cmd = [
    "pyinstaller",
    "--noconfirm",
    "--onefile",
    "--windowed",
    "--icon", "./Client/Icons/window_icon.ico",
    "./Client/updater.py"
]

subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
shutil.copy2("./dist/updater.exe", "./Server/Latest_Version/BetterDiscord")

# Copy files
print("Copying files")
shutil.copytree("./Client/Fonts", "./Server/Latest_Version/BetterDiscord/Fonts")
shutil.copytree("./Client/Icons", "./Server/Latest_Version/BetterDiscord/Icons")
shutil.copy2("./Client/SERVER_DETAILS.cfg", "./Server/Latest_Version/BetterDiscord")

# Create .zip
print("Creating .zip")
shutil.make_archive("./Server/Latest_Version/BetterDiscord", "zip", "./Server/Latest_Version/BetterDiscord")
shutil.rmtree("./Server/Latest_Version/BetterDiscord")

# Clean up
print("Cleaning up files")
shutil.rmtree("./dist")
shutil.rmtree("./build")
os.remove("./BetterDiscord.spec")
os.remove("./GUI.spec")
os.remove("./updater.spec")
