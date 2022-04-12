import tkinter as tk
import time
import keyboard as kb # type: ignore
from board import Board
from ui.render import Renderer
import input_handling



def main():
    gameboard = Board()

    window = tk.Tk()
    window.title("Tetris")

    renderer = Renderer(window, gameboard)

    starttime = time.perf_counter()
    while True:
        if window.focus_displayof():
            if kb.is_pressed("esc"):
                break
            input_handling.process_inputs(gameboard)
        renderer.draw()

        frametime = time.perf_counter() - starttime
        while frametime < 1 / 60:
            frametime = time.perf_counter() - starttime
        starttime = time.perf_counter()


if __name__ == "__main__":
    main()
