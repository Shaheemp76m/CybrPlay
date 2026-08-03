import raylib
import menu
import ui_render
import visualiser_render
import player
from config import *
import cava
from raylib import ffi

def update_layout(font, font2, title, info):
    bar_width = (screen_width - total_spacing) // no_of_bars
    song_width = raylib.MeasureTextEx(font2, title, 50, 1)
    info_width = raylib.MeasureTextEx(font, info, 20, 1)
    song_x = (screen_width - song_width.x) / 2
    info_x = (screen_width - info_width.x) / 2
    return bar_width, song_x, info_x

def update_screen():
    global screen_width, screen_height

    screen_width = raylib.GetScreenWidth()
    screen_height = raylib.GetScreenHeight()

def renderer():
    # raylib.SetConfigFlags(raylib.FLAG_VSYNC_HINT)
    raylib.SetConfigFlags(raylib.FLAG_WINDOW_RESIZABLE)
    raylib.SetConfigFlags(raylib.FLAG_WINDOW_TRANSPARENT)
    raylib.InitWindow(700, 480,  b"cybrplay")
    # raylib.MaximizeWindow()
    raylib.SetAudioStreamBufferSizeDefault(4096)
    raylib.InitAudioDevice()
    font = raylib.LoadFontEx(b"/usr/share/fonts/TTF/JetBrainsMono-Regular.ttf", 20, ffi.NULL, 0)
    font2 = raylib.LoadFontEx(b"/usr/share/fonts/TTF/JetBrainsMono-Bold.ttf", 50, ffi.NULL, 0)
    font3 = raylib.LoadFontEx(b"/usr/share/fonts/TTF/JetBrainsMono-Regular.ttf", 40, ffi.NULL, 0)
    raylib.SetTargetFPS(render_fps)

    visualiser = cava.start()
    waiting_for_next = False
    gap_frames = 0

    update_screen()
    fading_in, fading_in_frames, title, info, song_x, info_x = player.start_playing(font, font2, screen_width)
    bar_width, song_x, info_x = update_layout(font, font2, title, info)
    paused = False
    ismenu = False
    cursor = player.selected_genre
    go_to: str = ""

    while not raylib.WindowShouldClose():
        update_screen()
        # print("init:", raylib.GetScreenWidth(), raylib.GetScreenHeight())

        if waiting_for_next == False:
            raylib.UpdateMusicStream(player.music)
            go_to = "next"
        else:
            if gap_frames >= gap_btw_tracks:
                if ismenu:
                    menu.render_menu(font3, cursor, screen_width)
                else:
                    fading_in, fading_in_frames, title, info, song_x, info_x, cursor = player.song_change(go_to, font, font2, cursor, screen_width)
                    waiting_for_next = False
                    gap_frames = 0
            else:
                gap_frames += 1

        if ismenu:
            if raylib.IsKeyPressed(raylib.KEY_DOWN):
                if cursor != (len(player.genre_names) - 1):
                    cursor += 1
                    # print(cursor)
            if raylib.IsKeyPressed(raylib.KEY_UP):
                if cursor != 0:
                    cursor -= 1
                    # print(cursor) 
            if raylib.IsKeyPressed(raylib.KEY_ENTER):
                player.change_genre(cursor, 0)
                player.load_state()
                ismenu = False
                # print(cursor)
        else:
            if raylib.IsKeyPressed(raylib.KEY_DOWN):
                raylib.PauseMusicStream(player.music)
                ismenu = True
                waiting_for_next = True

            if raylib.IsKeyPressed(raylib.KEY_RIGHT):
                if player.current_song == len(player.songs) - 1:
                    # print("next album", player.current_song, len(player.songs))
                    go_to ="nextalbum"
                else:
                    # print("next song", player.current_song, len(player.songs))
                    go_to = "next"
                waiting_for_next, fading_in = player.next_song()

            if raylib.IsKeyPressed(raylib.KEY_SPACE):
                # print("song pause toggle")
                paused = player.pause(paused)

            if raylib.IsKeyPressed(raylib.KEY_LEFT):
                if player.current_song != 0:
                    # print("prev", player.current_song, len(player.songs))
                    go_to ="prev"
                else:
                    # print("prevalbum", player.current_song, len(player.songs))
                    go_to = "prevalbum"
                waiting_for_next, fading_in = player.next_song()


        bars: list[int] = cava.read_frame(visualiser)

        raylib.BeginDrawing()
        raylib.ClearBackground(raylib.BLANK)

        progress, waiting_for_next, go_to = player.song_progress(waiting_for_next, go_to)

        if raylib.IsWindowResized():
            bar_width, song_x, info_x = update_layout(font, font2, title, info)

        visualiser_render.render_visualiser(bars, screen_height, bar_width)
        fading_in, fading_in_frames = ui_render.song_and_metadata(
            waiting_for_next, fading_in_frames, fading_in, progress, font, font2, info, title, info_x, song_x, gap_frames, screen_width)
        raylib.EndDrawing()
    raylib.CloseAudioDevice()
    raylib.UnloadFont(font)
    raylib.UnloadFont(font2)
    raylib.UnloadFont(font3)
    raylib.CloseWindow()
    player.save_state()
renderer()
