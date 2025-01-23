import os
import unittest
import pyfcf
import matplotlib.pyplot as plt
from pathlib import Path

def example(filename):
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

    print(filename)
    plt.savefig(filename)


class TestSingleFigureExample(unittest.TestCase):
    def setUp(self):
        self.filename = Path(__file__).resolve().parent / f"{Path(__file__).stem}.png"

    def tearDown(self):
        if self.filename.exists():
            os.remove(self.filename)

    def test_runs_without_errors(self):
        try:
            example(self.filename)
        except Exception as e:
            self.fail(f"single_figure_example raised an exception: {e}")

    def test_creates_file(self):
        example(self.filename)
        self.assertTrue(self.filename.exists(), "File does not exist")

if __name__ == "__main__":
    example(Path(__file__).resolve().parent / f"{Path(__file__).stem}.png")