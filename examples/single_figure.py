"""single_figure.py
Create a single figure with defined axis and margin size.
"""

import pyfcf
import matplotlib.pyplot as plt
from pathlib import Path
pyfcf.FigConfig.setup_matplotlib(font_size=14)

def single_figure_example():
    x = [1, 2, 3, 4]
    y = [1, 1, 2, 5]

    xm = [0.7, 0.05]  # x margin
    ym = [0.4, 0.3]  # y margin

    fc = pyfcf.FigConfig(1, 1, xm=xm, ym=ym, idx=5, idy=3)
    print(fc.xs, fc.ys)

    plt.figure(figsize=(fc.xs, fc.ys))
    rect = fc.get_rect(0, 0)
    print(rect)

    ax = plt.axes(rect)
    ax.plot(x, y, "-o")
    ax.set_ylabel("Y-axis")
    ax.set_title("Title")

    plt.savefig(Path(__file__).resolve().parent / f"{fc.get_script_name(__file__)}.png")


if __name__ == "__main__":
    single_figure_example()
