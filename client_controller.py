# -*- coding: utf-8 -*-
from mazeClient import Commands as command
from mazeClient import send_command
from pynput import keyboard

def on_press(key):
    """
    Listen for input and move if a directional key or any of 'WASD' is pressed
    Exit if any other key is pressed
    """
    key_repr = repr(key)[1:-1]
    if key == keyboard.Key.up or key_repr == 'w':
        action = command.MOVE_UP
    elif key == keyboard.Key.down or key_repr == 's':
        action = command.MOVE_DOWN
    elif key == keyboard.Key.left or key_repr == 'a':
        action = command.MOVE_LEFT
    elif key == keyboard.Key.right or key_repr == 'd':
        action = command.MOVE_RIGHT
    elif key_repr == 'e':
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