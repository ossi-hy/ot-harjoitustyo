import keyboard as kb # type: ignore
from board import Board

inputs = {
    "left": "left",
    "right": "right",
    "drop": "space",
    "cw": "d",
    "ccw": "a",
    "180": "s",
}

pressed = {
    "left": False,
    "right": False,
    "drop": False,
    "cw": False,
    "ccw": False,
    "180": False,
}


def process_inputs(board: Board) -> None:
    for action, key in inputs.items():
        if kb.is_pressed(key):
            if pressed[action]:
                continue
            if action == "left":
                board.move(0)
            elif action == "right":
                board.move(1)
            elif action == "cw":
                board.rotate(0)
            elif action == "ccw":
                board.rotate(1)
            elif action == "180":
                board.rotate(2)
            elif action == "drop":
                board.drop()
            pressed[action] = True
        else:
            pressed[action] = False
