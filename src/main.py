from board import Board
from render import Renderer

import keyboard as kb

import tkinter as tk
import time

def main():
    gameboard = Board()

    window = tk.Tk()
    window.title("Tetris")

    renderer = Renderer(window, gameboard)

    starttime = time.perf_counter()
    while True:
        if window.focus_displayof() and kb.is_pressed("esc"):
            break
        renderer.draw()

        frametime = time.perf_counter() - starttime
        while frametime < 1/19:
            frametime = time.perf_counter() - starttime
        starttime = time.perf_counter()
    

if __name__ == "__main__":
    main()