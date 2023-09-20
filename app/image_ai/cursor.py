##this py when executed, show the exactly coordinate from the cursor
##so it gets easy to check the configuration

import curses
import pyautogui

def update_cursor_coordinates(stdscr, x, y):
    stdscr.clear()
    stdscr.addstr(0, 0, f"Cursor Coordinates: (x={x}, y={y})")
    stdscr.refresh()

def main(stdscr):
    # Initialize curses
    curses.curs_set(0)  # Hide the cursor

    while True:
        # Get the current cursor position
        x, y = pyautogui.position()

        # Update and display cursor coordinates
        update_cursor_coordinates(stdscr, x, y)

if __name__ == "__main__":
    curses.wrapper(main)
