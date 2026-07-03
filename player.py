import raylib
import json
import library
from mutagen.flac import FLAC

def song_change(songs, current_song, screen_height, screen_width, font, font2):
    audio = FLAC(songs[current_song])
    music = raylib.LoadMusicStream(songs[current_song].encode())
    raylib.PlayMusicStream(music)
    fading_in = True
    fading_in_frames = 0
    title = audio["title"][0].encode()
    info = audio["album"][0] + " - " + audio["artist"][0]
    info = info.encode()    
    song_width = raylib.MeasureTextEx(font2, title, 50, 1)
    info_width = raylib.MeasureTextEx(font, info, 20, 1)
    song_x = (screen_width - song_width.x) / 2
    info_x = (screen_width - info_width.x) / 2
    return music, audio, fading_in, fading_in_frames, title, info, song_width, info_width, song_x, info_x

def pause(music, paused):
    if paused:
        raylib.PauseMusicStream(music)
        paused = False
    else:
        raylib.ResumeMusicStream(music)
        paused = True
    return paused

def next_song(current_song, music):
    raylib.PauseMusicStream(music)
    waiting_for_next = True
    fading_in = True
    return waiting_for_next, fading_in

def load_state():

    with open("state.json","r") as f:
        state = json.load(f)
    current_song = state["current_song"]
    songs, genres = library.scan_music()
    genre_names = list(genres.keys())
    selected_genre = state["selected_genre"]
    songs = genres[genre_names[selected_genre]]
    return songs, current_song, genre_names, selected_genre

def save_state(current_song, selected_genre):
    state = {
        "current_song": current_song,
        "selected_genre": selected_genre
    }
    with open("state.json","w") as f:
        json.dump(state, f, indent=4)
