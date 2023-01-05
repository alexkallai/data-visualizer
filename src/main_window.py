from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from vispy.scene import SceneCanvas, visuals
from vispy.app import use_app
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
        self.canvas_wrapper = CanvasWrapper()

        self.controls = ControlWidgets()
        main_layout.addWidget(self.controls)

        # Add canvas.native as a widget, which is a low level widget
        main_layout.addWidget(self.canvas_wrapper.canvas.native)

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

class CanvasWrapper:
    def __init__(self):
        self.canvas = SceneCanvas(size=CANVAS_SIZE)
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

        #self.view_bot = self.grid.add_view(1, 0, bgcolor='#c0c0c0')
        ##line_data = _generate_random_line_positions(NUM_LINE_POINTS)
        #line_data = None
        #self.line = visuals.Line(line_data, parent=self.view_bot.scene, color=LINE_COLOR_CHOICES[0])
        #self.view_bot.camera = "panzoom"
        #self.view_bot.camera.set_range(x=(0, NUM_LINE_POINTS), y=(0, 1))

    def set_image_colormap(self, cmap_name: str):
        print(f"Changing image colormap to {cmap_name}")
        self.image.cmap = cmap_name

    def set_line_color(self, color):
        print(f"Changing line color to {color}")
        self.line.set_data(color=color)

def window():
    application = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(application.exec_())

if __name__ == "__main__":
    window()
