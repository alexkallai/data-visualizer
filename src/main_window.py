from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QFileDialog, QTabWidget, QLabel
from vispy.app import use_app
import configparser
from pathlib import Path
import util
import sys
import os

# Local imports
from canvas2d import CanvasWrapper2D
from canvas3d import CanvasWrapper3D
from previewcanvas import PreviewCanvas
from imagewidget import ImageWidget
from controlwidget import ControlWidgets
from file import File

# Config
filepath = Path(__file__).parent
config = configparser.ConfigParser()
config.read(f"{filepath}/settings.ini", encoding="utf-8")


class MainWindow(QMainWindow):
    """
    Docs
    """

    def __init__(self) -> None:
        super(MainWindow, self).__init__()

        # Set window geometry and location
        self.setGeometry(
            0,
            0,
            int( config["general"]["WINDOW_WIDTH"]   ),
            int( config["general"]["WINDOW_HEIGHT"]  )
                         )
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        # Set window title
        self.setWindowTitle("Data Visualizer")

        # TODO icon
        #from PyQt5.QtGui import QIcon
        #self.setWindowIcon()

        # Initialize the central widget
        central_widget = QtWidgets.QWidget()
        # Set main layout to horizontal box layout so widget sections are side-by-side
        main_layout = QtWidgets.QHBoxLayout()
        self.canvas_wrapper_2D = CanvasWrapper2D()
        self.canvas_wrapper_hilbert = CanvasWrapper2D()
        self.canvas_wrapper_3D = CanvasWrapper3D()

        #self.image_widget = ImageWidget()
        self.image_widget_canvas = PreviewCanvas()

        self.controls = ControlWidgets()

        # Initialize tabs
        self.tabs = QTabWidget()
        # Add canvas.native as a widget, which is a low level widget
        self.tabs.addTab(self.canvas_wrapper_2D.canvas.native, "2D view")
        self.tabs.addTab(self.canvas_wrapper_3D.canvas.native, "3D view")
        self.tabs.addTab(self.canvas_wrapper_hilbert.canvas.native, "Hilbert curve view")
        # Add widgets
        main_layout.addWidget(self.controls)
        #main_layout.addWidget(self.image_widget)
        main_layout.addWidget(self.image_widget_canvas.canvas.native)
        main_layout.addWidget(self.tabs)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self._connect_controls()

    def _connect_controls(self):
        self.controls.open_button.clicked.connect(self.set_file)
    
    def set_file(self):
        self.file = File()
        if hasattr(self.file, "raw_binary_file"):
            self.image_widget_canvas.set_image(self.file.get_byteplot_PIL_image())
            self.canvas_wrapper_2D.set_image(self.file.get_2D_digraph_image())
            self.canvas_wrapper_hilbert.set_image(self.file.get_2D_hilbert_image())