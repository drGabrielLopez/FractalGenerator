from enum import Enum

import numpy as np
import plotly.express as px


class FractalType(Enum):
    Julia = 1
    Mandelbrot = 2


class FractalGenerator:
    """Creates a single fractal object and either returns it as as a numpy array, plot it or persists it as an pgn
    image. The output of this class is used by FractalTrainingValidationSet to generate training/val sets
    Args:
        complex_function -- complex function to make a Julia fractal
        n -- fractal size will ne n*n
        xlim,ylim -- tuples with the plotting region on the complex plane
        thr -- once a function grows larger that this number is considered to be divergent to infinity
        max_iter -- number of compositions of the complex function with itself
        type_ -- fractal type
        fractal -- numpy array with the fractal
    """

    def __init__(self, n=256, xlim=(-2, 2), ylim=(-2, 2), thr=2, max_iter=10):
        self.type_ = None
        self.fractal = None
        self.n = n
        self.xlim = xlim
        self.ylim = ylim
        self.thr = thr
        self.max_iter = max_iter

    def create_julia(self, complex_function=lambda z: np.sin(z ** 4 + 1.41)):
        """Creates a fractal of the Julia family, the fractal is stored inside self.fractal"""
        fractal = np.zeros((self.n, self.n), dtype="complex")
        x_space = np.linspace(self.xlim[0], self.xlim[1], self.n)
        y_space = np.linspace(self.ylim[0], self.ylim[1], self.n)
        for ix, x in enumerate(x_space):
            for iy, y in enumerate(y_space):
                for i in range(self.max_iter):
                    if i == 0:
                        z = complex(x, y)
                    z = complex_function(z)
                    if np.abs(z) >= self.thr:
                        z = self.thr
                        break
                fractal[ix, iy] = z
        self.fractal = np.abs(fractal)
        self.type_ = FractalType.Julia
        return self

    def create_mandelbrot(self):
        """Creates a fractal of the Mandelbrot family, the fractal is stored inside self.fractal"""
        fractal = np.zeros((self.n, self.n), dtype="complex")
        x_space = np.linspace(self.xlim[0], self.xlim[1], self.n)
        y_space = np.linspace(self.ylim[0], self.ylim[1], self.n)
        for ix, x in enumerate(x_space):
            for iy, y in enumerate(y_space):
                for i in range(self.max_iter):
                    if i == 0:
                        z = 0
                    z = z ** 2 + complex(x, y)
                    if np.abs(z) >= self.thr:
                        z = self.thr
                        break
                fractal[ix, iy] = z
        self.fractal = np.abs(fractal.transpose())
        self.type_ = FractalType.Mandelbrot
        return self

    def plot(self, **kwargs):
        if self.fractal is None:
            print("Nothing to plot. Generate a fractal first.")
            return None
        random_colormap = np.random.choice(
            ["orrd", "inferno_r", "hot_r", "jet_r", "purples", "agsunset_r"]
        )
        fig = px.imshow(
            img=self.fractal, color_continuous_scale=random_colormap, **kwargs
        )
        return fig
