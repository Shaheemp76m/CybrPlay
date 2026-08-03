import json
from hextotuple import hextotuple

with open("/home/ross/.config/hypr/colors.json") as f: colors = json.load(f)
# colors
bottom_color = hextotuple(colors["accent2"], 255)
middle_color = hextotuple(colors["accent1"], 255)
top_color = hextotuple(colors["accent3"], 255)
ui_color = hextotuple(colors["accent1"], 255)

# 
block_height = 10
no_of_bars = 64
progress_y = 10
progress_width = 400
progress_height = 17
spacing = 5
gap_btw_tracks = 30 # fps
render_fps = 60
folder = "/home/ross/Music"

total_spacing = no_of_bars * spacing

