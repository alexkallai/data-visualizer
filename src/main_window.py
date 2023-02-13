#from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDesktopWidget, QTabWidget, QMainWindow, QWidget, QHBoxLayout, QFormLayout, QLabel
from PyQt5 import QtGui
from superqt import QRangeSlider, QLabeledRangeSlider
from qtpy.QtCore import Qt
from vispy.app import use_app
import configparser
from pathlib import Path
import time

# Local imports
from canvas2d import CanvasWrapper2D
from canvas3d import CanvasWrapper3D
from previewcanvas import PreviewCanvas
from controlwidget import ControlWidgets
from statusbarlayout import StatusBarLayout
from file import File
from plotwidget import PlotCanvasWrapper

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
        # Set window icon
        self.setWindowIcon(QtGui.QIcon("src/window_icon.ico"))
        # Initialize statusbar
        self.statusbar = self.statusBar()
        self.statusbar_layout = StatusBarLayout()
        self.statusbar.addWidget(self.statusbar_layout)

        # Initialize the central widget
        central_widget = QWidget()
        # Set main layout to horizontal box layout so widget sections are side-by-side
        main_layout = QHBoxLayout()
        self.canvas_wrapper_2D = CanvasWrapper2D()
        #self.canvas_wrapper_2D = PreviewCanvas()
        self.canvas_wrapper_hilbert = CanvasWrapper2D()
        self.canvas_wrapper_byte_histogram = PlotCanvasWrapper()
        self.canvas_wrapper_3D = CanvasWrapper3D()

        self.image_preview_widget_canvas_1 = PreviewCanvas()
        self.image_preview_widget_canvas_2 = PreviewCanvas()
        # Range slider 1
        self.range_slider_1 = QLabeledRangeSlider(Qt.Orientation.Vertical)
        self.range_slider_1.setBarMovesAllHandles(True)
        self.range_slider_1.setRange(0, 1000)
        self.range_slider_1.setValue((0, 1000))
        # Range slider 2
        self.range_slider_2 = QLabeledRangeSlider(Qt.Orientation.Vertical)
        self.range_slider_2.setBarMovesAllHandles(True)
        self.range_slider_2.setRange(0, 1000)
        self.range_slider_2.setValue((0, 1000))

        self.controls = ControlWidgets()

        # Initialize tabs
        self.tabs = QTabWidget()
        # Add canvas.native as a widget, which is a low level widget
        self.tabs.addTab(self.canvas_wrapper_2D.canvas.native, "2D view")
        self.tabs.addTab(self.canvas_wrapper_3D.canvas.native, "3D view")
        self.tabs.addTab(self.canvas_wrapper_hilbert.canvas.native, "Hilbert curve view")
        #self.tabs.addTab(self.canvas_wrapper_byte_histogram.canvas.native, "Byte histogram")
        self.tabs.addTab(self.canvas_wrapper_byte_histogram.plotcanvas.native, "Byte histogram")
        # Add widgets
        main_layout.addWidget(self.controls)
        main_layout.addWidget(self.range_slider_1)
        main_layout.addWidget(self.image_preview_widget_canvas_1.canvas.native)
        main_layout.addWidget(self.range_slider_2)
        main_layout.addWidget(self.image_preview_widget_canvas_2.canvas.native)
        main_layout.addWidget(self.tabs)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self._connect_controls()

    def _connect_controls(self):
        self.controls.open_button.clicked.connect(self.set_new_file)
        self.range_slider_1.sliderReleased.connect(self.slider_1_release_handler)
        self.range_slider_2.sliderReleased.connect(self.slider_2_release_handler)
        self.range_slider_1.sliderMoved.connect(self.slider_1_move_handler)
        self.range_slider_2.sliderMoved.connect(self.slider_2_move_handler)
    
    def set_new_file(self):
        self.file = File()
        self.set_file_pipeline()
    
    def set_statusbar(self):
            # Set the fields
            self.statusbar_layout.set_filename(self.file.file_name)
            self.statusbar_layout.set_path(self.file.folder_path)
            self.statusbar_layout.set_sha256(self.file.sha256_hash())
            self.statusbar_layout.set_md5(self.file.md5_hash())
    
    def set_file_pipeline(self):
        if hasattr(self.file, "raw_binary_file"):
            self.set_statusbar()

            # Set the images
            self.image_preview_widget_canvas_1.set_image(self.file.get_byteplot_PIL_image())
            self.image_preview_widget_canvas_2.set_image(self.file.get_byteplot_PIL_image())
            self.canvas_wrapper_2D.set_image(self.file.get_2D_digraph_image())
            self.canvas_wrapper_hilbert.set_image(self.file.get_2D_hilbert_image())
            self.canvas_wrapper_byte_histogram.set_plot(self.file.raw_binary_file)
            self.canvas_wrapper_3D.set_data(*self.file.get_3D_hilbert_image() )

    def slider_1_release_handler(self):
        print("Slider 1 released")
        print(self.range_slider_1.value())

    def slider_2_release_handler(self):
        print("Slider 2 released")

    def slider_1_move_handler(self):
        print("Slider 1 moved")

    def slider_2_move_handler(self):
        print("Slider 2 moved")