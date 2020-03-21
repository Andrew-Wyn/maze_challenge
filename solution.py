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
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

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

    cmap = ListedColormap(['k', 'r', 'g', 'b', 'w']) # codified in colormap module from matplotlib

    # liste che possono tornare utili per la generazione dell'istogramma nel caso le tengo, senno cambio c_s, che cosi non performa
    x_s = []
    y_s = []
    c_s = []

    for el in visited:
        x_s.append(el["x"])
        y_s.append(el["y"])
        if el["val"] == 82:
            c_s.append(1) # red
        elif el["val"] == 71:
            c_s.append(2) # green
        elif el["val"] == 66:
            c_s.append(3) # blue
        elif el["val"] == 32:
            c_s.append(4) # white

    x_max = max(x_s)
    y_max = max(y_s)

    matrix_plt = np.zeros((x_max + 1, y_max + 1))

    for i in range(len(x_s)):
        matrix_plt[x_max - x_s[i] + 1,y_max - y_s[i] + 1] = c_s[i]


    _ = plt.matshow(matrix_plt, cmap=cmap)

    plt.xlim((0,y_max - min(y_s)+2))
    plt.ylim((x_max - min(x_s)+2, 0))
    
    plt.show()


def plot_statistic():    
    names = list(nodes_count.keys())
    values = list(nodes_count.values())

    fig, axs = plt.subplots(1, 3, figsize=(9, 3), sharey=True)
    axs[0].bar(names, values)
    axs[1].scatter(names, values)
    axs[2].plot(names, values)
    fig.suptitle('Categorical Plotting')

    plt.show()



def preprocess_data_hist():

    x_colors = {}
    y_colors = {}

    # molteplici riscritture
    for el in visited:

        x_colors[el["x"]] = {
            'red':0,
            'green':0,
            'blue':0,
            'white':0
        }

        y_colors[el["y"]] = {
            'red':0,
            'green':0,
            'blue':0,
            'white':0
        }

    for el in visited:

        x = el["x"]
        y = el["y"]

        if el["val"] == 82:
            x_colors[x]['red'] += 1
            y_colors[y]['red'] += 1 # red
        elif el["val"] == 71:
            x_colors[x]['green'] += 1
            y_colors[y]['green'] += 1 # green
        elif el["val"] == 66:
            x_colors[x]['blue'] += 1
            y_colors[y]['blue'] += 1 # blue
        elif el["val"] == 32:
            x_colors[x]['white'] += 1
            y_colors[y]['white'] += 1 # white

    x_s = []
    x_red = []
    x_green = []
    x_blue = []
    x_white = []

    for key in sorted(x_colors):
        x_s.append(key)
        x_red.append(x_colors[key]["red"])
        x_green.append(x_colors[key]["green"])
        x_blue.append(x_colors[key]["blue"])
        x_white.append(x_colors[key]["white"])

    y_s = []
    y_red = []
    y_green = []
    y_blue = []
    y_white = []

    for key in sorted(y_colors):
        y_s.append(key)
        y_red.append(y_colors[key]["red"])
        y_green.append(y_colors[key]["green"])
        y_blue.append(y_colors[key]["blue"])
        y_white.append(y_colors[key]["white"])


    return x_s, x_red, x_green, x_blue, x_white, y_s, y_red, y_green, y_blue, y_white
    


def color_histogram():

    # nested function used only for this purpose
    def autolabel(ax, rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    x_s, x_red, x_green, x_blue, x_white, y_s, y_red, y_green, y_blue, y_white = preprocess_data_hist()

    fig, (ax1, ax2) = plt.subplots(1,2)

    print(y_s)

    width = 0.2  # the width of the bars

    # ---------------------- X

    x = np.arange(len(x_s))  # the label locations

    rect_red = ax1.bar(x - 3*width/2, x_red, width, label='Red', color="red")
    rect_green = ax1.bar(x - width/2, x_green, width, label='Green', color="green")
    rect_blue = ax1.bar(x + width/2, x_blue, width, label='Blue', color="blue")
    rect_white = ax1.bar(x + 3*width/2, x_white, width, label='White', color="grey")

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax1.set_ylabel('Frequency')
    ax1.set_title('Frequencies for X variable')
    ax1.set_xticks(x)
    ax1.set_xticklabels(x_s)
    ax1.legend()

    autolabel(ax1, rect_red)
    autolabel(ax1, rect_blue)
    autolabel(ax1, rect_green)
    autolabel(ax1, rect_white)

    leg = ax1.get_legend()
    leg.legendHandles[0].set_color('red')
    leg.legendHandles[1].set_color('green')
    leg.legendHandles[2].set_color('blue')
    leg.legendHandles[3].set_color('grey')


    # ---------------------------Y

    y = np.arange(len(y_s))  # the label locations

    rect_red1 = ax2.bar(y - 3*width/2, y_red, width, label='Red', color="red")
    rect_green1 = ax2.bar(y - width/2, y_green, width, label='Green', color="green")
    rect_blue1 = ax2.bar(y + width/2, y_blue, width, label='Blue', color="blue")
    rect_white1 = ax2.bar(y + 3*width/2, y_white, width, label='White', color="grey")

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax2.set_ylabel('Frequency')
    ax2.set_title('Frequencies for Y variable')
    ax2.set_xticks(y)
    ax2.set_xticklabels(y_s)
    ax2.legend()

    autolabel(ax2, rect_red1)
    autolabel(ax2, rect_blue1)
    autolabel(ax2, rect_green1)
    autolabel(ax2, rect_white1)

    leg = ax2.get_legend()
    leg.legendHandles[0].set_color('red')
    leg.legendHandles[1].set_color('green')
    leg.legendHandles[2].set_color('blue')
    leg.legendHandles[3].set_color('grey')


    # fig.tight_layout()
    fig.set_size_inches(18.5, 10.5)

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

    # quests
    print_map()
    color_histogram()

    # Print statistics
    print(nodes_count)
