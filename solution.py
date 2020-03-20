# -*- coding: utf-8 -*-
"""
MazeChallenge - by MircoT
Solvers: Luca Moroni, Antonio Strippoli

PSEUDOCODICE ITERATIVO:
- Scegli un vicino NON visitato:
    - Vai dal vicino
- Altrimenti (nessun vicino ok):
    - Controlla se puoi andare back
        - Vai back
    - Altrimenti (sono tornato all'origine):
        - Termina
"""
import mazeClient
import json
from time import sleep
import numpy as np
import matplotlib.pyplot as plt


# ---------------- UTILITIES ----------------
def update_counter(color: int):
    """
    Update counters of tiles' colors
    """
    if color == 82:
        nodes_count["red"] += 1
    elif color == 71:
        nodes_count["green"] += 1
    elif color == 66:
        nodes_count["blue"] += 1
    elif color == 32:
        nodes_count["white"] += 1


def get_dict(data: bytes):
    """
    Parse data and returns a dictionary (more usable)
    """
    return json.loads(data.decode('ascii'))


def inverse_command(com: "mazeClient.Commands"):
    """
    Get the command to go back given a command
    """
    if com == command.MOVE_LEFT:
        return command.MOVE_RIGHT
    elif com == command.MOVE_RIGHT:
        return command.MOVE_LEFT
    elif com == command.MOVE_UP:
        return command.MOVE_DOWN
    elif com == command.MOVE_DOWN:
        return command.MOVE_UP
    return command.GET_STATE # Bad usage


def get_neighbors(v: dict):
    """
    Returns valid neighbors
    """
    tmp = []
    for el in v["Neighbors"]:
        if (el["x"] - v["userX"] == 0) or (el["y"] - v["userY"] == 0):
            tmp.append(el)
    return tmp


def get_command(org: dict, dest: dict) -> "mazeClient.Commands":
    """
    Return command to let you move from org to dest
    """

    diff_x = org['userX'] - dest['x']
    diff_y = org['userY'] - dest['y']

    if diff_x == 1:
        return command.MOVE_DOWN
    elif diff_x == -1:
        return command.MOVE_UP
    elif diff_y == 1:
        return command.MOVE_RIGHT
    elif diff_y == -1:
        return command.MOVE_LEFT
    return command.GET_STATE # Bad usage


# --------------- MAIN PROGRAM --------------
def dfs(v: dict, last_cmd: str):
    # Remove unreachable neighbors
    neighbors_dict = get_neighbors(v)

    for u in neighbors_dict:
        if u not in visited:
            # Visit the neighbor
            visited.append(u)
            update_counter(u['val'])

            # Move to neighbor
            cmd = get_command(v, u)
            u = get_dict(mazeClient.send_command(cmd))
            #sleep(1)

            # Visit from that neighbor
            dfs(u, cmd)

    # Move back
    mazeClient.send_command(inverse_command(last_cmd))
    #sleep(1)


# -------------- Quests -----------------------

def print_map():

    x_s = []
    y_s = []

    for el in visited:
        x_s.append(el["x"])
        y_s.append(el["y"])

    matrix_plt = np.zeros((max(x_s), max(y_s)))

    for i in range(len(x_s)):
        matrix_plt[x_s[i]-1,y_s[i]-1] = 1


    plt.matshow(matrix_plt)
    plt.show()


def plot_statistic():

    x_s = []
    y_s = []
    c_s = []

    for el in visited:
        x_s.append(el["x"])
        y_s.append(el["y"])
        if el["val"] == 82:
            c_s.append("red")
        elif el["val"] == 71:
            c_s.append("green")
        elif el["val"] == 66:
            c_s.append("blue")
        elif el["val"] == 32:
            c_s.append("white")


    fig, ax = plt.subplots()
    ax.scatter(x_s, y_s, c = c_s)

    fig.savefig("stats.png")
    plt.show()


# ---------------- Main --------------------

if __name__ == '__main__':
    # Initialize variables
    command = mazeClient.Commands
    visited = [] # Grey nodes
    nodes_count = {
        'white': 0,
        'red': 0,
        'green': 0,
        'blue': 0
    }

    # Visit the root (starting position)
    curr_node = get_dict(mazeClient.send_command(command.GET_STATE))
    visited.append({
        'x': curr_node['userX'],
        'y': curr_node['userY'],
        'val': curr_node['userVal']
    })

    # Start exploration
    dfs(curr_node, command.GET_STATE)

    print_map()

    plot_statistic()

    # Print statistics
    print(nodes_count)
