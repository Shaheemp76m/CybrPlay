import raylib
from config import *

def render_visualiser(bars, screen_height: int, bar_width: int):
    x = spacing
    for bar in bars:
        bar_height = int((bar / 1000) * screen_height)
        blocks = bar_height // block_height
        reminder = bar_height % block_height
        y = screen_height - bar_height

        for _ in range(blocks):# rendering the visualiser
            position: float = y / screen_height
            if position < 0.5:
                amount = position / 0.5
                color = raylib.ColorLerp(top_color, middle_color, amount)  # pyright: ignore[reportUnknownMemberType]
            else:
                amount = (position - 0.5) / 0.5
                color = raylib.ColorLerp(middle_color, bottom_color, amount)  # pyright: ignore[reportUnknownMemberType]
            raylib.DrawRectangle(x, y, bar_width, block_height, color)  # pyright: ignore[reportUnknownMemberType]
            y += block_height
        if reminder > 0:
            raylib.DrawRectangle(x, y, bar_width, reminder, bottom_color)  # pyright: ignore[reportUnknownMemberType]
        x += bar_width + spacing
    return 0
