import subprocess
import threading
import time

title = "No Music"
artist = ""
album = ""
position = 0.0
duration = 0.0

def get_metadata():
    try:
        title = subprocess.check_output(
            ["playerctl","metadata","title"],
            text=True
        ).strip()

        artist = subprocess.check_output(
            ["playerctl","metadata","artist"],
            text=True
        ).strip()

        album= subprocess.check_output(
            ["playerctl","metadata","album"],
            text=True
        ).strip()

        return title, artist, album

    except:
        return "No Music","",""

def get_progress():
    try:
        position = float(subprocess.check_output(
            ["playerctl","position"],
            text=True
        ).strip())
        duration = float(subprocess.check_output(
            ["playerctl","metadata","mpris:length"],
            text=True
        ).strip()) / 1_000_000
        return position, duration
    except:
        return 0.0, 0.0

def music_thread():
    global title, album, artist, position, duration

    while True:
        title, artist, album = get_metadata()
        position, duration = get_progress()
        time.sleep(0.1)
threading.Thread(target=music_thread, daemon=True).start()
