from board import Board
from render import Renderer
import tkinter as tk

def main():
    gameboard = Board()

    window = tk.Tk()
    window.title("Tetris")

    renderer = Renderer(window, gameboard)
    renderer.draw()
    window.mainloop()

if __name__ == "__main__":
    main()