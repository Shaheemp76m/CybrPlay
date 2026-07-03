from pathlib import Path
from config import folder
from mutagen.flac import FLAC

def scan_music():
    songs = []
    genres = {}
    suported = ".flac"
    music_dir = Path(folder)

    for file in music_dir.rglob("*"):
        if file.is_file() and file.suffix.lower() in suported:
            genres = metadata(file, genres)
            songs.append(str(file))
    return songs, genres

def metadata(file, genres):
    audio = FLAC(file)
    genres_of_song = audio.get("genre", ["Unknown"])
    for current_genre in genres_of_song:
        current_genre = current_genre.strip()
        if current_genre in genres:
           genres[current_genre].append(str(file))
        else:
           genres[current_genre] = []
           genres[current_genre].append(str(file))
    return genres

