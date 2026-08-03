from pathlib import Path
from config import folder
from mutagen.flac import FLAC

def scan_music():
    songs: list[str] = []
    genres: dict[str, list[str]] = {}
    suported = ".flac"
    music_dir = Path(folder)

    for file in music_dir.rglob("*"):
        if file.is_file() and file.suffix.lower() in suported:
            genres = metadata(file, genres)
            songs.append(str(file))

    # genres = {
    #    genres: songs
    #    for genres, songs in genres.items()
    #    if len(songs) >= 3
    #}
    return songs, genres

def metadata(file: Path, genres: dict[str, list[str]]):
    audio = FLAC(file)
    if "album" not in audio:
        return genres
    genres_of_song: list[str] = str(audio["album"][0]).split(",")

    for current_genre in genres_of_song:
        current_genre = current_genre.strip()
        if current_genre in genres:
           genres[current_genre].append(str(file))
        else:
           genres[current_genre] = []
           genres[current_genre].append(str(file))
    genres = dict(
        sorted(
            genres.items(),
            key=lambda item: len(item[1]),
            reverse = True
        )
    )
    return genres

if __name__ == '__main__':
    songs, genres = scan_music()
    genres = {
        genres: songs
        for genres, songs in genres.items()
        if len(songs) >= 2
    }
    no = 0
    for genre, songs in genres.items():
        print(no, genre)
        no += 1
        for song in songs:
            print("     ", song)

