from vispy.scene import SceneCanvas, visuals
from vispy.plot import Fig
import numpy as np


class PlotCanvasWrapper:
    def __init__(self):
        self.plotcanvas = Fig(bgcolor="#F0F0F0")
        self.plotwidget = self.plotcanvas[0, 0]
        self.color = (0.3, 0.5, 0.8)

    def set_image_colormap(self, cmap_name: str):
        pass

    def set_plot(self, plot_data: np.ndarray) -> None:
        # plot_data: 1D array
        self.plotwidget.histogram(plot_data, bins=256, color=self.color, orientation='h')
        #self.plotwidget.update()

    def refit_image(self) -> None:
        pass