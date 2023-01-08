from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTabWidget, QLabel
from PyQt5.QtGui import QImage, QPixmap
from vispy.scene import SceneCanvas, visuals
from vispy.app import use_app
import numpy as np
import sys
import os

# Define window location and size settings
CANVAS_SIZE = (600, 600)  # (width, height)
IMAGE_SHAPE = (600, 800)  # (height, width)
WINDOW_X_COORD = 100
WINDOW_Y_COORD = 200
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
COLORMAP_CHOICES = ["viridis", "reds", "blues"]
LINE_COLOR_CHOICES = ["black", "red", "blue"]

class MainWindow(QMainWindow):
    """
    Docs
    """

    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        # Set window geometry and location
        self.setGeometry(
            WINDOW_X_COORD,
            WINDOW_Y_COORD,
            WINDOW_WIDTH,
            WINDOW_HEIGHT
                         )
        # Set window title
        self.setWindowTitle("Data Visualizer")

        # TODO icon
        #from PyQt5.QtGui import QIcon
        #self.setWindowIcon()

        # Initialize the window's widgets
        central_widget = QtWidgets.QWidget()
        # Set main layout to horizontal box layout
        main_layout = QtWidgets.QHBoxLayout()
        self.canvas_wrapper_2D = CanvasWrapper2D()
        self.canvas_wrapper_3D = CanvasWrapper3D()

        self.image_widget = ImageWidget()

        # Initialize tabs
        self.tabs = QTabWidget()

        self.tabs.addTab(self.canvas_wrapper_2D.canvas.native, "2D view")
        self.tabs.addTab(self.canvas_wrapper_3D.canvas.native, "3D view")

        self.controls = ControlWidgets()
        main_layout.addWidget(self.controls)
        main_layout.addWidget(self.image_widget)

        # Add canvas.native as a widget, which is a low level widget
        main_layout.addWidget(self.tabs)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    # Return the file name
    def get_file_name(self):
        return QFileDialog.getOpenFileName(
            parent=self,
            caption="Open a file",
            directory=os.getcwd()
        )

class ControlWidgets(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QtWidgets.QVBoxLayout()

        open_button = QtWidgets.QPushButton("Open file")
        open_button.clicked.connect(self.get_file_name)
        layout.addWidget(open_button)

        self.colormap_label = QtWidgets.QLabel("Image Colormap:")
        layout.addWidget(self.colormap_label)

        self.colormap_chooser = QtWidgets.QComboBox()
        self.colormap_chooser.addItems(COLORMAP_CHOICES)
        layout.addWidget(self.colormap_chooser)

        self.line_color_label = QtWidgets.QLabel("Line color:")
        layout.addWidget(self.line_color_label)

        self.line_color_chooser = QtWidgets.QComboBox()
        self.line_color_chooser.addItems(LINE_COLOR_CHOICES)
        layout.addWidget(self.line_color_chooser)

        layout.addStretch(1)
        self.setLayout(layout)
        self.setFixedWidth(200)

    # Return the file name
    def get_file_name(self):
        return QFileDialog.getOpenFileName(
            parent=self,
            caption="Open a file",
            directory=os.getcwd()
        )

class CanvasWrapper2D:
    def __init__(self):
        self.canvas = SceneCanvas()
        self.grid = self.canvas.central_widget.add_grid()

        self.view_top = self.grid.add_view(0, 0, bgcolor='cyan')
        #image_data = _generate_random_image_data(IMAGE_SHAPE)
        image_data = None
        self.image = visuals.Image(
            image_data,
            texture_format="auto",
            cmap="viridis",
            parent=self.view_top.scene,
        )
        #self.view_top.camera = "panzoom"
        self.view_top.camera.set_range(x=(0, IMAGE_SHAPE[1]), y=(0, IMAGE_SHAPE[0]), margin=0)

    def set_image_colormap(self, cmap_name: str):
        print(f"Changing image colormap to {cmap_name}")
        self.image.cmap = cmap_name

    def set_line_color(self, color):
        print(f"Changing line color to {color}")
        self.line.set_data(color=color)

class CanvasWrapper3D:

    def __init__(self) -> None:
        self.canvas = SceneCanvas(keys="interactive", show=True)
        #self.grid = self.canvas.central_widget.add_grid()
        self.view = self.canvas.central_widget.add_view()
        scatter = visuals.Markers()
        scatter.set_data(np.full((2, 2), fill_value=10, dtype=np.uint8), edge_width=0, face_color=(1, 1, 1, .5), size=5, symbol="arrow")
        #scatter.set_data(pos, edge_width=0, face_color=(1, 1, 1, .5), size=5, symbol=symbols)
        self.view.add(scatter)
        self.view.camera = 'arcball'
        self.axis = visuals.XYZAxis(parent=self.view.scene)

class ImageWidget(QtWidgets.QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.layout = QtWidgets.QVBoxLayout
        self.label = QLabel(self)
        self.picture = QImage("sphx_glr_point_cloud_001.png")
        self.picture = QPixmap("sphx_glr_point_cloud_001.png")
        self.label.setPixmap(self.picture)
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)

def window():
    application = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(application.exec_())

if __name__ == "__main__":
    window()
