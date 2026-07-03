import raylib
import config
from config import *
import library
import cava
from raylib import ffi
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

def renderer():
    raylib.SetConfigFlags(raylib.FLAG_WINDOW_TRANSPARENT)
    raylib.InitWindow(screen_width,screen_height,b"Cybrplay")
    raylib.InitAudioDevice()
    font = raylib.LoadFontEx(b"/usr/share/fonts/TTF/JetBrainsMono-Regular.ttf", 20, ffi.NULL, 0)
    font2 = raylib.LoadFontEx(b"/usr/share/fonts/TTF/JetBrainsMono-Bold.ttf", 50, ffi.NULL, 0)
    raylib.SetTextureFilter(font.texture,1)
    raylib.SetTargetFPS(render_fps)

    visualiser = cava.start()
    waiting_for_next = False
    gap_frames = 0

    current_song = 0
    songs, genres = library.scan_music()
    genre_names = list(genres.keys())
    selected_genre = 9
    songs = genres[genre_names[selected_genre]]
    music, audio, fading_in, fading_in_frames, title, info, song_width, info_width, song_x, info_x = song_change(songs, current_song, screen_height, screen_width, font2, font)
    paused = False

    total_spacing = no_of_bars * spacing
    bar_width = (screen_width - total_spacing) // no_of_bars
    while not raylib.WindowShouldClose():

        if waiting_for_next == False:
            raylib.UpdateMusicStream(music)
        else:
            if gap_frames >= gap_btw_tracks:
                music, audio, fading_in, fading_in_frames, title, info, song_width, info_width, song_x, info_x = song_change(songs, current_song, screen_height, screen_width, font, font2)
                waiting_for_next = False
                gap_frames = 0 
            else:
                gap_frames += 1

        if raylib.IsKeyPressed(raylib.KEY_RIGHT):
            current_song = (current_song + 1 ) % len(songs)
            raylib.PauseMusicStream(music)
            waiting_for_next = True

        if raylib.IsKeyPressed(raylib.KEY_SPACE):
            if paused:
                raylib.PauseMusicStream(music)
                paused = False
            else:
                raylib.ResumeMusicStream(music)
                paused = True

        if raylib.IsKeyPressed(raylib.KEY_LEFT):
            current_song -= 1
            raylib.PauseMusicStream(music)
            waiting_for_next = True

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
        
        progress_x = (screen_width - 400) // 2

        ball_x = progress_x + 8 + (progress * (progress_width - 8 * 2))
        ball_y = progress_y + (progress_height / 2)
        x = spacing

        for bar in bars:
            bar_height = int((bar / 1000) * screen_height)
            blocks = bar_height // block_height
            reminder = bar_height % block_height
            x_increment = screen_width // no_of_bars
            y = screen_height - bar_height


            for i in range(blocks):# rendering the visualiser
                position = y / screen_height
                if position < 0.5:
                    amount = position / 0.5
                    color = raylib.ColorLerp(top_color, middle_color, amount)
                else:
                    amount = (position - 0.5) / 0.5
                    color = raylib.ColorLerp(middle_color, bottom_color, amount)
                raylib.DrawRectangle(x, y, bar_width, block_height, color)
                y += block_height
            if reminder > 0:
                raylib.DrawRectangle(x, y, bar_width, reminder, bottom_color)
            x += bar_width + spacing

        if waiting_for_next == True:
            alpha = 255 - (gap_frames * 255 // gap_btw_tracks) 
            raylib.DrawRectangleRounded((progress_x, progress_y, progress_width, progress_height), 1, 20, (242, 72, 72, alpha))
            raylib.DrawCircle(int(ball_x), int(ball_y), 6, (120, 20, 20, alpha))
            raylib.DrawTextEx(font, info, (info_x, 37), 20, 1, (242, 72, 72, alpha))
            raylib.DrawTextEx(font2, title, (song_x, 60), 50, 1, (242, 72, 72, alpha))
        elif fading_in == True:
            alpha = fading_in_frames * 255 // 30
            raylib.DrawRectangleRounded((progress_x, progress_y, progress_width, progress_height), 1, 20, (242, 72, 72, alpha))
            raylib.DrawCircle(int(ball_x), int(ball_y), 6, (120, 20, 20, alpha))
            raylib.DrawTextEx(font, info, (info_x, 37), 20, 1, (242, 72, 72, alpha))
            raylib.DrawTextEx(font2, title, (song_x, 60), 50, 1, (242, 72, 72, alpha))
            fading_in_frames += 1
            if alpha == 255:
                fading_in = False
                fading_in_frames = 0
        else:
            raylib.DrawRectangleRounded((progress_x, progress_y, progress_width, progress_height), 1, 20, song_color)
            raylib.DrawCircle(int(ball_x), int(ball_y), 6, (120, 20, 20, 255))
            raylib.DrawTextEx(font, info, (info_x, 37), 20, 1, song_color)
            raylib.DrawTextEx(font2, title, (song_x, 60), 50, 1, song_color)

        raylib.EndDrawing()
    raylib.CloseAudioDevice()
    raylib.UnloadFont(font)
    raylib.CloseWindow()
renderer()

