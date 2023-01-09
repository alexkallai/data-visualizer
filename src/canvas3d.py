from vispy.scene import SceneCanvas, visuals
from PyQt5.QtCore import QSize
from PyQt5.QtGui import *
import numpy as np


class CanvasWrapper3D:

    def __init__(self):
        self.canvas = SceneCanvas()
        self.view = self.canvas.central_widget.add_view()
        scatter = visuals.Markers()
        scatter.set_data(
            pos = np.full((20, 2), 10, dtype= np.uint32),
            size = 5,
            #edge_width: float = 1,
            #edge_width_rel: Any | None = None,
            edge_color = 'black',
            face_color = 'white',
            symbol = 'o')
        self.view.add(scatter)
        self.view.camera = "arcball"
        # axis for navigation
        self.axis = visuals.XYZAxis(parent=self.view.scene)