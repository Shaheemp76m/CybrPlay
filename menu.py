from config import *
import raylib
from player import genre_names

genre_names: list[str]
offset_y = 0.0

def render_menu(font3: raylib.Font, cursor: int, screen_width: int):
    global offset_y
    target_offset = -(cursor * 35)
    offset_y += (target_offset - offset_y) * 0.15
    genre_y = 220 + offset_y
    for i, genre in enumerate(genre_names):
        if i == cursor:
            text = "> " + genre + " <"
        else:
            text = "" + genre
        genre_width = raylib.MeasureTextEx(font3, text.encode(), 40, 1)
        genre_x = (screen_width - genre_width.x) / 2
        if i == cursor:
            raylib.DrawTextEx(font3, text.encode(), (genre_x, genre_y), 40, 1, ui_color)  # pyright: ignore[reportUnknownMemberType]
        else:
            raylib.DrawTextEx(font3, text.encode(), (genre_x, genre_y), 40, 1, top_color)  # pyright: ignore[reportUnknownMemberType]
        genre_y += 35

