import tkinter as tk
import time
import keyboard as kb # type: ignore
from board import Board
from ui.render import Renderer
from inputhandler import InputHandler



def main():
    gameboard = Board()

    window = tk.Tk()
    window.title("Tetris")

    renderer = Renderer(window, gameboard)

    inputhandler = InputHandler(gameboard)

    start_time = time.perf_counter()
    input_time = time.perf_counter()
    while True:
        if window.focus_displayof():
            if kb.is_pressed("esc"):
                break
            inputhandler.process_inputs(gameboard, time.perf_counter() - input_time)
            input_time = time.perf_counter()
        renderer.draw()

        frametime = time.perf_counter() - start_time
        # Wait to keep 60fps
        while frametime < 1 / 60:
            frametime = time.perf_counter() - start_time
        start_time = time.perf_counter()


if __name__ == "__main__":
    main()
