import raylib
from config import *

def draw_song_ui(alpha: int, color: tuple[int, int, int, int], ball_color: tuple[int, int, int, int], progress_x: int, font: raylib.Font, font2: raylib.Font, info: bytes, title: bytes, info_x: int, song_x: int, ball_x: float, ball_y: float):
    raylib.DrawRectangleRounded((progress_x, progress_y, progress_width, progress_height), 1, 20, color)
    raylib.DrawCircle(int(ball_x), int(ball_y), 6, ball_color)
    raylib.DrawTextEx(font, info, (info_x, 37), 20, 1, color)
    raylib.DrawTextEx(font2, title, (song_x, 60), 50, 1, color)

def song_and_metadata(waiting_for_next: bool, fading_in_frames: int, fading_in: bool, progress: float, font: raylib.Font, font2: raylib.Font, info: bytes, title: bytes, info_x: int, song_x: int, gap_frames: int):
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
    ball_color = (
        top_color[0],
        top_color[1],
        top_color[2],
        alpha
    )
    # print(waiting_for_next, fading_in, alpha)
    draw_song_ui(alpha, color, ball_color, progress_x, font, font2, info, title, info_x, song_x, ball_x, ball_y)
    return fading_in, fading_in_frames
