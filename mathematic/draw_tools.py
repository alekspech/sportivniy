import matplotlib.pyplot as plt
import numpy as np

def make_axes(
        xlim=(-10, 10), 
        ylim=(-10, 10), 
        major=1.0, 
        minor=0.5, 
        figsize=(7, 5), 
        equal=False
    ):
    """
    Create a Matplotlib figure/axes with:
    - Major grid every `major`
    - Minor grid every `minor`
    - OX (x-axis) in green, OY (y-axis) in blue
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    if equal:
        ax.set_aspect('equal', adjustable='box')

    # OX and OY
    ax.axhline(0, color='green', linewidth=4)
    ax.axvline(0, color='blue', linewidth=4)

    # Ticks
    x0, x1 = xlim
    y0, y1 = ylim
    ax.set_xticks(np.arange(np.floor(x0), np.ceil(x1) + major, major))
    ax.set_yticks(np.arange(np.floor(y0), np.ceil(y1) + major, major))
    ax.set_xticks(np.arange(np.floor(x0), np.ceil(x1) + minor, minor), minor=True)
    ax.set_yticks(np.arange(np.floor(y0), np.ceil(y1) + minor, minor), minor=True)

    # Grid
    ax.grid(which='major', linestyle='-', alpha=0.6)
    ax.grid(which='minor', linestyle=':', alpha=0.4)

    # Softer spines
    for spine in ax.spines.values():
        spine.set_alpha(0.3)

    return fig, ax
