""" single_figure.py
Create a single figure with defined axis and margin size.
"""
import pyfcf
import matplotlib.pyplot as plt
from pathlib import Path

x = [1,2,3,4]
y = [1,1,2,5]

def example1():

    xm = [0.4, 0.05] # x margin
    ym = [0.4, 0.3] # y margin

    fc = pyfcf.FigConfig(1,1, xm=xm, ym=ym, idx=5, idy=3)
    print(fc.xs, fc.ys)

    plt.figure(figsize=(fc.xs, fc.ys))
    rect = fc.get_rect(0, 0)
    print(rect)
    
    ax = plt.axes(rect)
    ax.plot(x,y,'-o')
    ax.set_title('Title')

    plt.savefig(Path(__file__).resolve().parent / 'single_figure.png')

if __name__ == "__main__":

    example1()