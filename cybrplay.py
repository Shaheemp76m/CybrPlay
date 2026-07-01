import raylib

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
 
    while True:
        stdscr.clear()

        h, w = stdscr.getmaxyx()

        song_name = "Song Name"
        album_name = "Album"
        auther = "Auther"
        song_info = album_name + " - " + auther

        song_y = h // 4
        song_x = (w - len(song_name)) // 2

        song_info_y = song_y + 1
        song_info_x = (w - len(song_info)) // 2

        stdscr.addstr(song_y, song_x, song_name, curses.A_BOLD | curses.color_pair(1))
        stdscr.addstr(song_info_y, song_info_x, song_info, curses.color_pair(1))
        stdscr.refresh()

        if stdscr.getch() == ord("q"):
            break
curses.wrapper(main)
