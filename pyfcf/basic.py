import matplotlib
import numpy as np

__ALL__ = ["FigConfig",  "setup_matplotlib", "axes_setup"]

def setup_matplotlib(font_size:(int, float) =14) -> None:
    plt.rcParams["font.size"] = font_size
    # font_family = ['DejaVu Sans', 'Garamond', 'Proxima Nova'][1]
    # plt.rcParams["font.family"] = font_family
    plt.rcParams["axes.formatter.use_mathtext"] = True
    plt.rcParams["mathtext.fontset"] = "cm"
    plt.rcParams["figure.dpi"] = 200


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
                 idx: (float, None) = None, idy: (float, None) = None,
                 xm: list = [], ym: list = [],
                 cbx: float =0, cby: float=0, cpos: (str, None) = None):
        '''
        :param nx: (int) number of sub figures in x dimension
        :param ny: (int) number of sub figure sin y dimension
        :param idx: (float) size of each x sub figure
        :param idy: (float) size of each y sub figure
        :param xm:
        :param ym:
        :param cbx:
        :param cby:
        :param cpos:
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
            self.idx = idx
            self.xs = idx*nx + self.xcm[-1]
            if self.cpos in ['left', 'right']:
                self.xs += self.cbx

        if idy is not None:
            self.idy = idy
            self.ys = idy*ny + self.ycm[-1]
            if self.cpos in ['bottomr', 'top']:
                self.ys += self.cby

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
            rect = np.array([self.xcm[ix]+ix*self.idx,
                             self.ycm[iy]+iy*self.idy, self.idx, self.idy])

        return rect / self.nrm

    def get_cax_rect(self):
        '''Colorbar axes position'''
        if self.cpos is None:
            return
        elif self.cpos == 'bottom':
            rect = np.array([self.xs/2 - self.cbx/2, self.ycm[0], self.cbx, self.cby])
        elif self.cpos == 'top':
            rect = np.array([self.xs/2 - self.cbx/ 2, self.ycm[-2]+self.idy*self.ny, self.cbx, self.cby])
        elif self.cpos == 'left':
            rect = np.array([self.xcm[0], self.ys/2 - self.cby/2, self.cbx, self.cby])
        elif self.cpos == 'right':
            rect = np.array([self.xcm[-2]+self.idx*self.nx, self.ys/2 - self.cby/2, self.cbx, self.cby])
        else:
            raise ValueError('Do not understand cpos:', self.cpos)

        return rect / self.nrm

    @staticmethod
    def axes_setup(ax,
                   left_position=-0.025, top_visible=False, right_visible=False,
                   ticklabelsize=10):
        ax.spines["left"].set_position(("axes",left_position))
        ax.spines["top"].set_visible(top_visible)
        ax.spines["right"].set_visible(right_visible)
        ax.tick_params(labelsize=ticklabelsize)

    @staticmethod
    def matplotlib_setup(fontsize: (int, float) = 12, fontfamily=None) -> None:
        if fontfamily is None:
            fontfamily = ['DejaVu Sans', 'Garamond', 'Proxima Nova'][1]
        plt.rcParams["font.size"] = fontsize
        plt.rcParams["font.family"] = fontfamily
        plt.rcParams["axes.formatter.use_mathtext"] = True
        plt.rcParams["mathtext.fontset"] = "cm"
        plt.rcParams["figure.dpi"] = 200

        print(os.path.basename(__file__).split('.')[0])

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
        return os.path.splitext(os.path.basename(p))[0]