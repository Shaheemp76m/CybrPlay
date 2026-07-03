import raylib
import ui_render
import visualiser_render
import player
from config import *
import library
import cava
from raylib import ffi

def renderer():
    raylib.SetConfigFlags(raylib.FLAG_WINDOW_TRANSPARENT)
    raylib.InitWindow(screen_width,screen_height,b"Cybrplay")
    raylib.InitAudioDevice()
    font = raylib.LoadFontEx(b"/usr/share/fonts/TTF/JetBrainsMono-Regular.ttf", 20, ffi.NULL, 0)
    font2 = raylib.LoadFontEx(b"/usr/share/fonts/TTF/JetBrainsMono-Bold.ttf", 50, ffi.NULL, 0)
    font3 = raylib.LoadFontEx(b"/usr/share/fonts/TTF/JetBrainsMono-Regular.ttf", 30, ffi.NULL, 0)
    raylib.SetTextureFilter(font.texture,1)
    raylib.SetTargetFPS(render_fps)

    visualiser = cava.start()
    waiting_for_next = False
    fading_in = True
    gap_frames = 0

    songs, current_song, genre_names, selected_genre = player.load_state()
    music, audio, fading_in, fading_in_frames, title, info, song_width, info_width, song_x, info_x = player.song_change(
        songs, current_song, screen_height, screen_width, font2, font)
    paused = False

    total_spacing = no_of_bars * spacing
    bar_width = (screen_width - total_spacing) // no_of_bars
    while not raylib.WindowShouldClose():

        if waiting_for_next == False:
            raylib.UpdateMusicStream(music)
        else:
            if gap_frames >= gap_btw_tracks:
                music, audio, fading_in, fading_in_frames, title, info, song_width, info_width, song_x, info_x = player.song_change(
                    songs, current_song, screen_height, screen_width, font, font2)
                waiting_for_next = False
                gap_frames = 0 
            else:
                gap_frames += 1

        if raylib.IsKeyPressed(raylib.KEY_RIGHT):
            current_song = (current_song + 1 ) % len(songs)
            waiting_for_next, fading_in = player.next_song(current_song, music)

        if raylib.IsKeyPressed(raylib.KEY_SPACE):
            paused = player.pause(music, paused)

        if raylib.IsKeyPressed(raylib.KEY_LEFT):
            current_song -= 1
            waiting_for_next, fading_in = player.next_song(current_song, music)

        bars = cava.read_frame(visualiser)
        raylib.BeginDrawing()
        raylib.ClearBackground(raylib.BLANK)

        if int(raylib.GetMusicTimeLength(music)) <= int(raylib.GetMusicTimePlayed(music)):
            current_song = (current_song + 1 ) % len(songs)
            progress = 1.0
            raylib.PauseMusicStream(music)
            waiting_for_next = True
        elif raylib.GetMusicTimeLength(music) > 0:
            progress = raylib.GetMusicTimePlayed(music) / raylib.GetMusicTimeLength(music)
        else:
            progress = 0.0

        visualiser_render.render_visualiser(bars, bar_width)
        fading_in, fading_in_frames = ui_render.song_and_metadata(waiting_for_next, fading_in, fading_in_frames, progress, font, font2, info, title, info_x, song_x, gap_frames)
        raylib.EndDrawing()
    raylib.CloseAudioDevice()
    raylib.UnloadFont(font)
    raylib.CloseWindow()
    player.save_state(current_song, selected_genre)
renderer()

