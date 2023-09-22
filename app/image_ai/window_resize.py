import ctypes
import tkinter as tk
from tkinter import ttk

# Function to get a list of all open windows.
def get_windows_list():
    windows = []

    def enum_windows_callback(hwnd, lParam):
        if ctypes.windll.user32.IsWindowVisible(hwnd):
            title_length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
            title_buffer = ctypes.create_unicode_buffer(title_length + 1)
            ctypes.windll.user32.GetWindowTextW(hwnd, title_buffer, title_length + 1)
            windows.append((hwnd, title_buffer.value))
        return True  # Return True to continue enumerating windows

    # Create a callback function pointer.
    enum_windows_proc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)(enum_windows_callback)

    # Call EnumWindows with the callback function.
    ctypes.windll.user32.EnumWindows(enum_windows_proc, 0)
    
    return windows

# Create a list of available windows.
available_windows = get_windows_list()

# Create a simple tkinter GUI for window selection.
root = tk.Tk()
root.title("Select a Window")
root.geometry("400x300")

label = tk.Label(root, text="Select a window to resize:")
label.pack(pady=10)

window_combobox = ttk.Combobox(root, values=[title for _, title in available_windows])
window_combobox.pack()

def resize_selected_window():
    selected_title = window_combobox.get()
    for hwnd, title in available_windows:
        if selected_title == title:
            window_width = 800
            window_height = 600
            x = 0
            y = 0
            ctypes.windll.user32.SetWindowPos(hwnd, None, x, y, window_width, window_height, 0)
            ctypes.windll.user32.ShowWindow(hwnd, 1)
            ctypes.windll.user32.SetForegroundWindow(hwnd)
            break

resize_button = tk.Button(root, text="Resize Selected Window", command=resize_selected_window)
resize_button.pack(pady=10)

root.mainloop()
