import raylib
import time
import menu
import ui_render
import visualiser_render
import player
from config import *
import library
import cava
from raylib import ffi

def renderer():
    raylib.SetConfigFlags(raylib.FLAG_WINDOW_TRANSPARENT)
    raylib.InitWindow(screen_width,screen_height,b"cybrplay")
    raylib.InitAudioDevice()
    font = raylib.LoadFontEx(b"/usr/share/fonts/TTF/JetBrainsMono-Regular.ttf", 20, ffi.NULL, 0)
    font2 = raylib.LoadFontEx(b"/usr/share/fonts/TTF/JetBrainsMono-Bold.ttf", 50, ffi.NULL, 0)
    font3 = raylib.LoadFontEx(b"/usr/share/fonts/TTF/JetBrainsMono-Regular.ttf", 40, ffi.NULL, 0)
    raylib.SetTextureFilter(font.texture,1)
    raylib.SetTargetFPS(render_fps)

    visualiser = cava.start()
    waiting_for_next = False
    gap_frames = 0

    fading_in, fading_in_frames, title, info, song_width, info_width, song_x, info_x = player.start_playing(font, font2)
    paused = False
    ismenu = False
    cursor = player.selected_genre

    while not raylib.WindowShouldClose():

        if waiting_for_next == False:
            raylib.UpdateMusicStream(player.music)
            go_to = "next"
        else:
            if gap_frames >= gap_btw_tracks:
                if ismenu:
                    menu.render_menu(font3, cursor)
                else:
                    fading_in, fading_in_frames, title, info, song_width, info_width, song_x, info_x = player.song_change(go_to, font, font2)
                    waiting_for_next = False
                    gap_frames = 0 
            else:
                gap_frames += 1

        if raylib.IsKeyPressed(raylib.KEY_RIGHT):
            go_to = "next"
            waiting_for_next, fading_in = player.next_song()

        if raylib.IsKeyPressed(raylib.KEY_SPACE):
            paused = player.pause(paused)

        if raylib.IsKeyPressed(raylib.KEY_LEFT):
            go_to = "prev"
            waiting_for_next, fading_in = player.next_song()

        if raylib.IsKeyPressed(raylib.KEY_M):
            if ismenu:
                raylib.ResumeMusicStream(player.music)
                ismenu = False
                waiting_for_next = False
            else:
                raylib.PauseMusicStream(player.music)
                ismenu = True
                waiting_for_next = True

        if ismenu:
            if raylib.IsKeyPressed(raylib.KEY_DOWN):
                if cursor != (len(player.genre_names) - 1):
                    cursor += 1
            if raylib.IsKeyPressed(raylib.KEY_UP):
                if cursor != 0:
                    cursor -= 1
            if raylib.IsKeyPressed(raylib.KEY_ENTER):
                player.change_genre(cursor, 0)
                player.load_state()
                ismenu = False

        bars = cava.read_frame(visualiser)
        
        raylib.BeginDrawing()
        raylib.ClearBackground(raylib.BLANK)

        progress, waiting_for_next = player.song_progress(waiting_for_next)

        visualiser_render.render_visualiser(bars, bar_width)
        fading_in, fading_in_frames = ui_render.song_and_metadata(
            waiting_for_next, fading_in_frames, fading_in, progress, font, font2, info, title, info_x, song_x, gap_frames)
        raylib.EndDrawing()
    raylib.CloseAudioDevice()
    raylib.UnloadFont(font)
    raylib.UnloadFont(font2)
    raylib.UnloadFont(font3)
    raylib.CloseWindow()
    player.save_state()
renderer()

