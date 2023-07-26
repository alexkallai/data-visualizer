from vispy.scene import SceneCanvas, visuals
from PyQt5.QtCore import QSize
from PyQt5.QtGui import *
import numpy as np


class CanvasWrapper3D:

    def __init__(self):
        self.canvas = SceneCanvas()
        self.view = self.canvas.central_widget.add_view()
        self.scatter = visuals.Markers()
        self.scatter.set_data(
            pos = np.empty((100, 3),  dtype= np.uint8),
            size = 5,
            #edge_width: float = 1,
            #edge_width_rel: Any | None = None,
            edge_color = 'black',
            face_color = 'white',
            symbol = 'o')
        #self.view.add(scatter)
        self.view.camera = "arcball"
        # axis for navigation
        self.axis = visuals.XYZAxis(parent=self.view.scene)
    
    def set_data(self, data: np.ndarray, colors: np.ndarray):
        #del self.view
        #self.view = self.canvas.central_widget.add_view()
        #scatter = visuals.Markers(alpha=0.3)
        self.scatter.set_data(
            pos = data,
            size = 3,
            edge_width = 0,
            edge_color = 'white',
            face_color = colors,
            symbol = 'o')
        self.view.add(self.scatter)
        self.view.update()