import raylib
import cava
import music
from raylib import ffi

def renderer():
    raylib.SetConfigFlags(raylib.FLAG_WINDOW_TRANSPARENT)
    raylib.InitWindow(1350,720,b"Cybrplay")
    font = raylib.LoadFontEx(b"/usr/share/fonts/TTF/JetBrainsMono-Regular.ttf", 20, ffi.NULL, 0)
    font2 = raylib.LoadFontEx(b"/usr/share/fonts/TTF/JetBrainsMono-Bold.ttf", 50, ffi.NULL, 0)
    raylib.SetTextureFilter(font.texture,1)
    raylib.SetTargetFPS(60)

    visualiser = cava.start()
    bottom_color = (99, 31, 33, 255)
    middle_color = (242, 72, 72, 255)
    top_color = (242, 97, 24, 200)
    song_color = (242, 72, 72, 255)
    glow = (99, 31, 33, 40)

    while not raylib.WindowShouldClose():
        bars = cava.read_frame(visualiser)
        raylib.BeginDrawing()
        raylib.ClearBackground(raylib.BLANK)
        screen_height = raylib.GetScreenHeight()
        screen_width = raylib.GetScreenWidth()
        spacing = 8
        total_spacing = 32 * spacing
        bar_width = (screen_width - total_spacing) // 32
        x = spacing

        # get latest metadata from the thread
        title = music.title.encode()
        info = music.artist + " - " + music.album
        info = info.encode()
        if music.duration > 0:
            progress = music.position / music.duration
        else:
            progress = 0.0

        for bar in bars:
            block_height = 10
            bar_height = int((bar / 1000) * screen_height)
            blocks = bar_height // block_height
            reminder = bar_height % block_height
            x_increment = screen_width // 32
            y = screen_height - bar_height

            song_width = raylib.MeasureTextEx(font2, title, 50, 1)
            info_width = raylib.MeasureTextEx(font, info, 20, 1)
            song_x = (screen_width - song_width.x) / 2
            info_x = (screen_width - info_width.x) / 2

            progress_x = (screen_width - 400) // 2
            progress_y = 10
            progress_width = 400
            progress_height = 17

            ball_x = progress_x + 8 + (progress * (progress_width - 8 * 2))
            ball_y = progress_y + (progress_height / 2)

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
        raylib.DrawTextEx(font2, title, (song_x, 60), 50, 1, song_color)
        raylib.DrawTextEx(font, info, (info_x, 37), 20, 1, song_color)
        raylib.DrawRectangleRounded((progress_x, progress_y, progress_width, progress_height), 1, 20, song_color)
        raylib.DrawCircle(int(ball_x), int(ball_y), 6, (120, 20, 20, 255))
        raylib.EndDrawing()
    raylib.UnloadFont(font)
    raylib.CloseWindow()
renderer()

