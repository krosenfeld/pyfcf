from typing import Union
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

__ALL__ = ["FigConfig",  "setup_matplotlib", "axes_setup"]

def setup_matplotlib(font_size:Union[int, float] =14, **kwargs) -> None:
    plt.rcParams["font.size"] = font_size
    plt.rcParams["axes.formatter.use_mathtext"] = True
    plt.rcParams["mathtext.fontset"] = "cm"
    plt.rcParams["figure.dpi"] = 200
    for key, value in kwargs.items():
        plt.rcParams[key] = value

def axes_setup(axes):
    axes.spines["left"].set_position(("axes",-0.025))
    axes.spines["top"].set_visible(False)
    axes.spines["right"].set_visible(False)
    return


class FigConfig():
    '''
    Class for generating pretty and customized matplotlib figures.
    '''

    def __init__(self, nx: int, ny: int,
                 idx: Union[float, None] = None, idy: Union[float, None] = None,
                 xs: Union[float, None] = None, ys: Union[float, None] = None,
                 xm: list = [], ym: list = [],
                 cbx: float =0, cby: float=0, cpos: Union[str, None] = None):
        '''
        :param nx: (int) number of sub figures in x dimension
        :param ny: (int) number of sub figure sin y dimension
        :param idx: (float) size of each x sub figure
        :param idy: (float) size of each y sub figure
        :param xs: (float) size of figure in x dimension
        :param ys: (float) size of figure in y dimension
        :param xm: (list) size of the x margins
        :param ym: (list) size of the y margins
        :param cbx: (float) size of the colorbar in the x dimension
        :param cby: (float) size of the colorbar in the y dimension
        :param cpos: (string) position of the colorbar
        '''

        self.nx = nx
        self.ny = ny
        if len(xm) > 0:
            self.xcm = np.cumsum(xm)
        if len(ym) > 0:
            self.ycm = np.cumsum(ym)

        # colorbar
        if isinstance(cpos, str):
            self.cpos = cpos.lower()
        else:
            self.cpos = None
        self.cbx = cbx
        self.cby = cby

        if idx is not None:
            if isinstance(idx, (float, int)):
                self.idx = [idx]
            else:     
                self.idx = idx
            self.xs = np.sum(idx) + self.xcm[-1]
            if self.cpos in ['left', 'right']:
                self.xs += self.cbx

        if idy is not None:
            if isinstance(idy, (float, int)):
                self.idy = [idy]
            else:     
                self.idy = idy            
            self.ys = np.sum(idy) + self.ycm[-1]
            if self.cpos in ['bottom', 'top']:
                self.ys += self.cby

        if xs is not None:
            self.xs = xs
            if self.cpos in ['left', 'right']:
                self.idx = self.nx*[(self.xs - self.xcm[-1] - self.cbx) / self.nx]
            else:
                self.idx = self.nx*[(self.xs - self.xcm[-1]) / self.nx]

        if ys is not None:
            self.ys = ys
            if self.cpos in ['bottom', 'top']:
                self.idy = self.ny*[(self.ys - self.ycm[-1] - self.cby)/self.ny]
            else:
                self.idy = self.ny*[(self.ys - self.ycm[-1])/self.ny]

        # set normalizing factor
        self.set_nrm()

        # check for self consistency
        self._check()

    def _check(self):
        for ix in range(self.nx):
            for iy in range(self.ny):
                assert(np.all(self.get_rect(ix, iy) <= 1))

        if self.cpos is not None:
            assert(self.cpos in ['bottom', 'top', 'left', 'right'])

        if self.cbx != 0 or self.cby != 0:
            assert(self.cpos is not None)


    def set_nrm(self):
        self.nrm =  np.array([self.xs, self.ys, self.xs, self.ys])

    def get_rect(self, ix, iy):
        '''Assumes colorbar is on top or on left'''

        if self.cpos == 'bottom':
            rect = np.array([self.xcm[ix]+ix*self.idx,
                             self.ycm[iy+1]+iy*self.idy+self.cby, self.idx, self.idy])
        elif self.cpos == 'left':
            rect = np.array([self.xcm[ix+1]+ix*self.idx+self.cbx,
                             self.ycm[iy]+iy*self.idy, self.idx, self.idy])
        else:
            idx = [self.idx] if not isinstance(self.idx, list) else self.idx
            idy = [self.idy] if not isinstance(self.idy, list) else self.idy
            rect = np.array([self.xcm[ix]+np.cumsum(np.concatenate(([0],idx)))[ix],
                             self.ycm[iy]+np.cumsum(np.concatenate(([0],idy)))[iy], 
                             self.idx[ix], self.idy[iy]])

        return rect / self.nrm

    def get_cax_rect(self):
        '''Colorbar axis position'''

        if self.cpos is None:
            return
        elif self.cpos == 'bottom':
            fig_block =  (self.xcm[-2] - self.xcm[0] + self.nx*self.idx)
            rect = np.array([self.xcm[0] + fig_block/2 - self.cbx/2, self.ycm[0], self.cbx, self.cby])
        elif self.cpos == 'top':
            fig_block =  (self.xcm[-2] - self.xcm[0] + self.nx*self.idx)
            rect = np.array([self.xcm[0] + fig_block/2 - self.cbx/2, self.ycm[-2] + self.idy*self.ny, 
            self.cbx, self.cby])
        elif self.cpos == 'left':
            fig_block =  (self.ycm[-2] - self.ycm[0] + self.ny*self.idy)
            rect = np.array([self.xcm[0], self.ycm[0] + fig_block/2 - self.cby/2, 
                self.cbx, self.cby])
        elif self.cpos == 'right':
            fig_block =  (self.ycm[-2] - self.ycm[0] + self.ny*self.idy)
            rect = np.array([self.xcm[-2] + self.idx*self.nx, self.ycm[0] + fig_block/2 - self.cby/2,
                self.cbx, self.cby])
        else:
            raise ValueError('Do not understand cpos:', self.cpos)

        return rect / self.nrm

    @staticmethod
    def setup_axes(ax,
                   left_position=-0.025, top_visible=False, right_visible=False,
                   ticklabelsize=10):
        ax.spines["left"].set_position(("axes",left_position))
        ax.spines["top"].set_visible(top_visible)
        ax.spines["right"].set_visible(right_visible)
        ax.tick_params(labelsize=ticklabelsize)

    @staticmethod
    def setup_matplotlib(font_size: Union[int, float] = 12, dpi=200, **kwargs) -> None:
        plt.rcParams["font.size"] = font_size
        # plt.rcParams["font.family"] = fontfamily
        plt.rcParams["axes.formatter.use_mathtext"] = True
        plt.rcParams["mathtext.fontset"] = "cm"
        plt.rcParams["figure.dpi"] = dpi
        for key, value in kwargs.items():
            plt.rcParams[key] = value

    @staticmethod
    def set_fontsize(fontsize: float):
        plt.rcParams["font.size"] = fontsize

    @staticmethod
    def legend(ax, fontsize=10, **kwargs):
        ax.legend(frameon=False, fontsize=fontsize, **kwargs)

    @staticmethod
    def get_script_name(p):
        '''
        Returns the name of the path without extension. Useful for attributing figures to the scripts that generate them.
        Example: FigConfig.get_script_name(__file))
        :param p: path of the script
        :return: string without path and extension
        '''
        return Path(p).stem
