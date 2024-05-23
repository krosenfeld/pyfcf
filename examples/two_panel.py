""" two_panel.py
Two panel figure setting axis and margin size
"""

import pyfcf
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def two_panel_example():

    pyfcf.FigConfig.setup_matplotlib(font_size=14)

    x = np.linspace(0, 2*np.pi, 100)

    xm = [0.8, 0.7, 0.05] # x margin
    ym = [0.4, 0.3] # y margin

    fc = pyfcf.FigConfig(2, 1, xm=xm, ym=ym, idx=[5, 2], idy=[3])
    print(f"Figure size: ({fc.xs}), ({fc.ys})")

    plt.figure(figsize=(fc.xs, fc.ys))

    # panel 1
    rect = fc.get_rect(0, 0)
    print(f"rect 1: {rect}")
    ax = plt.axes(rect)
    fc.setup_axes(ax)
    ax.plot(x, np.cos(x),'-o')
    ax.set_title('Panel 1')

    # panel 2
    rect = fc.get_rect(1, 0)
    print(f"rect 2: {rect}")
    ax = plt.axes(rect)
    fc.setup_axes(ax)
    ax.plot(x, np.sin(x), '-o')
    ax.set_title('Panel 2')

    plt.savefig(Path(__file__).resolve().parent / f"{fc.get_script_name(__file__)}.png")

if __name__ == "__main__":

    two_panel_example()