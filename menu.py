from config import *
import raylib
from player import genre_names

def render_menu(font3, cursor):
    offset_y = -(cursor * 35)
    genre_y = 220 + offset_y
    for i, genre in enumerate(genre_names):
        if i == cursor:
            text = "> " + genre + " <"
        else:
            text = "" + genre
        genre_width = raylib.MeasureTextEx(font3, text.encode(), 40, 1)
        genre_x = (screen_width - genre_width.x) / 2
        if i == cursor:
            raylib.DrawTextEx(font3, text.encode(), (genre_x, genre_y), 40, 1, ui_color)
        else:
            raylib.DrawTextEx(font3, text.encode(), (genre_x, genre_y), 40, 1, (242, 72, 72, 159))
        genre_y += 35

