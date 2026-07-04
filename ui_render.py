import raylib
from config import *


def draw_song_ui(alpha, color, progress_x, progress, font, font2, info, title, info_x, song_x, ball_x, ball_y):
    raylib.DrawRectangleRounded((progress_x, progress_y, progress_width, progress_height), 1, 20, color)
    raylib.DrawCircle(int(ball_x), int(ball_y), 6, (120, 20, 20, alpha))
    raylib.DrawTextEx(font, info, (info_x, 37), 20, 1, color)
    raylib.DrawTextEx(font2, title, (song_x, 60), 50, 1, color)

def song_and_metadata(waiting_for_next, fading_in_frames, fading_in, progress, font, font2, info, title, info_x, song_x, gap_frames):
    progress_x = (screen_width - 400) // 2
    ball_x = progress_x + 8 + (progress * (progress_width - 8 * 2))
    ball_y = progress_y + (progress_height / 2)

    if waiting_for_next:
        alpha = 255 - (gap_frames * 255 // gap_btw_tracks) 
    elif fading_in:
        alpha = fading_in_frames * 255 // 30
        fading_in_frames += 1
        if alpha == 255:
            fading_in = False
            fading_in_frames = 0
    else:
        alpha = 255

    color = (
        ui_color[0],
        ui_color[1],
        ui_color[2],
        alpha
    )
    # print(waiting_for_next, fading_in, alpha)
    draw_song_ui(alpha, color, progress_x, progress, font, font2, info, title, info_x, song_x, ball_x, ball_y)
    return fading_in, fading_in_frames
