import os
import unittest
import pyfcf
import matplotlib.pyplot as plt
from pathlib import Path

def example(filename):

    x = [1, 2, 3, 4]
    y = [1, 1, 2, 5]    
    nx = 3
    fc = pyfcf.FigConfig(nx=3, ny=1, xs=8.5, ys=4.5, 
                        xm=[0.3]+(nx-2)*[0.1]+[0.3], ym=[0.3, 0.1])
    
    fig = plt.figure(figsize=(fc.xs, fc.ys))
    for i in range(nx):
        ax = plt.axes(fc.get_rect(i,0))
        ax.plot(x,y,'-o')
        
    plt.savefig(filename)

class TestMultiFigureExample(unittest.TestCase):
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
    TestMultiFigureExample().test_builds_without_errors()
    # unittest.main()