from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import *


class ImageWidget(QWidget):

    def __init__(self, parent = None):
        self.width = 300
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.label = QLabel(self)
        self.picture = QPixmap(None)
        self.label.setPixmap(self.picture)
        self.label.setScaledContents(True)
        self.label.setMinimumWidth(self.width)
        self.label.setMaximumHeight(900)
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)


    def set_image(self, image: QPixmap) -> None:
        im = image.scaledToHeight(600, Qt.FastTransformation)
        self.label.setPixmap(im)