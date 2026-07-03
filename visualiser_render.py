import raylib
from config import *

def render_visualiser(bars, bar_width):
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
    return 0
