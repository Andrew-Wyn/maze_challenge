# -*- coding: utf-8 -*-
from mazeClient import Commands as command
from mazeClient import send_command
from pynput import keyboard

def on_press(key):
    """
    Listen for input and move if a directional key or any of 'WASD' is pressed
    Exit if any other key is pressed
    """

    if key == keyboard.Key.up or key.char == 'w':
        action = command.MOVE_UP
    elif key == keyboard.Key.down or key.char == 's':
        action = command.MOVE_DOWN
    elif key == keyboard.Key.left or key.char == 'a':
        action = command.MOVE_LEFT
    elif key == keyboard.Key.right or key.char == 'd':
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