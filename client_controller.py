# -*- coding: utf-8 -*-
from mazeClient import Commands as command
from mazeClient import send_command
from pynput import keyboard

def on_press(key):
    """
    Listen for input and move if a directional key or any of 'WASD' is pressed
    Exit if any other key is pressed
    """


    _key_ = keyboard.Key

    if key == _key_.up or key.char == 'w':
        action = command.MOVE_UP
    elif key == _key_.down or key.char == 's':
        action = command.MOVE_DOWN
    elif key == _key_.left or key.char == 'a':
        action = command.MOVE_LEFT
    elif key == _key_.right or key.char == 'd':
        action = command.MOVE_RIGHT
    elif key.char == 'e':
        action = command.GET_STATE
    else:
        return False

    res = send_command(action)
    if action == command.GET_STATE:
        print(res)
    else:
        print(action)


if __name__ == "__main__":
    print("INSTRUCTIONS:\n\tWASD -> Move around the maze;\n\tE -> GET STATE;\n\tAny other Key: QUIT")
    # Collect events until released
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()