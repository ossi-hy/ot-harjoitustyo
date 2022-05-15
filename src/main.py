from __future__ import annotations
import tkinter as tk
#import time
from time import perf_counter as time
from game.board import Board
from ui.render import Renderer
from ui.inputhandler import InputHandler


def main():
    gameboard = Board()

    # Create window
    window = tk.Tk()
    window.title("Tetris")

    inputhandler = InputHandler(window, gameboard)

    renderer = Renderer(window, gameboard, inputhandler)

    start_time = time()
    input_time = time()
    while True:
        inputhandler.process_inputs(renderer, time() - input_time)
        input_time = time()
        if not renderer.draw():
            break

        frametime = time() - start_time
        # Busyloop wait to keep 60fps
        while frametime < 1 / 60:
            frametime = time() - start_time
        start_time = time()
    window.quit()


if __name__ == "__main__":
    main()
