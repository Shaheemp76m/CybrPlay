import raylib
import json
import library
from config import *
from mutagen.flac import FLAC

def start_playing(font: raylib.Font, font2: raylib.Font, screen_width: int):
    global music, audio, current_song
    audio = FLAC(songs[current_song])
    music = raylib.LoadMusicStream(songs[current_song].encode())
    raylib.PlayMusicStream(music)  # pyright: ignore[reportUnknownMemberType]
    fading_in = True
    fading_in_frames = 0
    title: bytes = audio["title"][0].encode()
    info = audio["album"][0] + " - " + audio["artist"][0]
    info: bytes = info.encode()
    song_width = raylib.MeasureTextEx(font2, title, 50, 1)  # pyright: ignore[reportUnknownMemberType]
    info_width = raylib.MeasureTextEx(font, info, 20, 1)  # pyright: ignore[reportUnknownMemberType]
    song_x = (screen_width - song_width.x) / 2
    info_x = (screen_width - info_width.x) / 2
    return fading_in, fading_in_frames, title, info, song_x, info_x

def song_change(go_to: str, font: raylib.Font, font2: raylib.Font, cursor: int, screen_width: int):

    global music, audio, current_song, selected_genre

    if go_to == "next":
        if current_song < len(songs) - 1:
            current_song += 1
        else:
            current_song = 0
            # print(selected_genre)
            # print(cursor)
            change_genre(cursor, 0)
            load_state()

    elif go_to == "prev":
        if current_song != 0:
            current_song -= 1

    elif go_to == "nextalbum":
        current_song = 0
        # print(selected_genre)
        # print(cursor)
        selected_genre = (selected_genre + 1) % len(genre_names)
        cursor = selected_genre
        change_genre(cursor, 0)
        load_state()

    elif go_to == "prevalbum":
        selected_genre = (selected_genre - 1) % len(genre_names)
        cursor = selected_genre
        change_genre(cursor, 0)
        load_state()
        current_song = len(songs) - 1

    audio = FLAC(songs[current_song])
    music = raylib.LoadMusicStream(songs[current_song].encode())
    raylib.PlayMusicStream(music)  # pyright: ignore[reportUnknownMemberType]
    fading_in = True
    fading_in_frames = 0
    title = audio["title"][0].encode()
    info = audio["album"][0] + " - " + audio["artist"][0]
    info = info.encode()
    song_width = raylib.MeasureTextEx(font2, title, 50, 1)  # pyright: ignore[reportUnknownMemberType]
    info_width = raylib.MeasureTextEx(font, info, 20, 1)  # pyright: ignore[reportUnknownMemberType]
    song_x = (screen_width - song_width.x) / 2
    info_x = (screen_width - info_width.x) / 2
    return fading_in, fading_in_frames, title, info, song_x, info_x, cursor

def pause(paused: bool):
    if paused:
        raylib.ResumeMusicStream(music)  # pyright: ignore[reportUnknownMemberType]
        paused = False
    else:
        raylib.PauseMusicStream(music)  # pyright: ignore[reportUnknownMemberType]
        paused = True
    return paused

def next_song():
    raylib.PauseMusicStream(music)  # pyright: ignore[reportUnknownMemberType]
    waiting_for_next = True
    fading_in = True
    return waiting_for_next, fading_in

def song_progress(waiting_for_next: bool, go_to: str):
    global current_song
    if int(raylib.GetMusicTimeLength(music)) <= int(raylib.GetMusicTimePlayed(music)):  # pyright: ignore[reportUnknownMemberType]
        progress = 1.0
        raylib.PauseMusicStream(music)  # pyright: ignore[reportUnknownMemberType]
        waiting_for_next = True
        if current_song == len(songs) - 1:
            # print("next album", current_song, len(songs))
            go_to = "nextalbum"
        else:
            # print("next song", current_song, len(songs))
            go_to = "next"
    elif raylib.GetMusicTimeLength(music) > 0:  # pyright: ignore[reportUnknownMemberType]
        progress = raylib.GetMusicTimePlayed(music) / raylib.GetMusicTimeLength(music)  # pyright: ignore[reportUnknownMemberType]
    else:
        progress = 0.0
    return progress, waiting_for_next, go_to

def change_genre(selected_genre: int, current_song: int):
    state = {
        "current_song": current_song,
        "selected_genre": selected_genre,
    }
    with open("state.json","w") as f:
        json.dump(state, f, indent=4)

def load_state():
    global current_song, selected_genre, songs, genre_names, genres
    with open("state.json","r") as f:
        state: dict[str, int] = json.load(f)
    current_song = state["current_song"]
    genre_names = list(genres.keys())
    selected_genre = state["selected_genre"]
    songs = genres[genre_names[selected_genre]]
    return songs, current_song, selected_genre, genre_names

def save_state():
    state = {
        "current_song": current_song,
        "selected_genre": selected_genre
    }
    with open("state.json","w") as f:
        json.dump(state, f, indent=4)

current_song: int
songs: list[str]
selected_genre: int
genre_names: list[str]
genres = library.scan_music()
songs, current_song, selected_genre, genre_names = load_state()
