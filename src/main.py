from __future__ import annotations
import tkinter as tk
import time
from board import Board
from ui.render import Renderer
from inputhandler import InputHandler


def main():
    gameboard = Board()

    # Create window
    window = tk.Tk()
    window.title("Tetris")

    renderer = Renderer(window, gameboard)

    inputhandler = InputHandler(gameboard)

    start_time = time.perf_counter()
    input_time = time.perf_counter()
    while True:
        if window.focus_displayof():
            inputhandler.process_inputs(renderer, time.perf_counter() - input_time)
            input_time = time.perf_counter()
        if not renderer.draw():
            break

        frametime = time.perf_counter() - start_time
        # Busyloop wait to keep 60fps
        while frametime < 1 / 60:
            frametime = time.perf_counter() - start_time
        start_time = time.perf_counter()
    window.quit()


if __name__ == "__main__":
    main()
