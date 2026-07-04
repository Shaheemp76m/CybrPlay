import raylib
import json
import library
from config import *
from mutagen.flac import FLAC

def start_playing(font, font2):
    global music, audio, current_song
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
    return fading_in, fading_in_frames, title, info, song_width, info_width, song_x, info_x

def song_change(go_to, font, font2):
    global music, audio, current_song
    # raylib.StopMusicStream(music)
    # raylib.UnloadMusicStream(music)
    if go_to == "next":
        current_song = (current_song + 1 ) % len(songs)
    elif go_to == "prev":
        current_song -= 1
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
    return fading_in, fading_in_frames, title, info, song_width, info_width, song_x, info_x

def pause(paused):
    if paused:
        raylib.ResumeMusicStream(music)
        paused = False
    else:
        raylib.PauseMusicStream(music)
        paused = True
    return paused

def next_song():
    raylib.PauseMusicStream(music)
    waiting_for_next = True
    fading_in = True
    return waiting_for_next, fading_in

def song_progress(waiting_for_next):
    global current_song
    if int(raylib.GetMusicTimeLength(music)) <= int(raylib.GetMusicTimePlayed(music)):
        progress = 1.0
        raylib.PauseMusicStream(music)
        waiting_for_next = True
    elif raylib.GetMusicTimeLength(music) > 0:
        progress = raylib.GetMusicTimePlayed(music) / raylib.GetMusicTimeLength(music)
    else:
        progress = 0.0
    return progress, waiting_for_next

def load_state():
    with open("state.json","r") as f:
        state = json.load(f)
    current_song = state["current_song"]
    songs, genres = library.scan_music()
    genre_names = list(genres.keys())
    selected_genre = state["selected_genre"]
    songs = genres[genre_names[selected_genre]]
    return songs, current_song, selected_genre

def save_state():
    state = {
        "current_song": current_song,
        "selected_genre": selected_genre
    }
    with open("state.json","w") as f:
        json.dump(state, f, indent=4)

songs, current_song, selected_genre = load_state()
