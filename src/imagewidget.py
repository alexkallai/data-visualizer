from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap


class ImageWidget(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.label = QLabel(self)
        self.picture = QPixmap(None)
        self.label.setPixmap(self.picture)
        self.layout.addWidget(self.label)

        self.setLayout(self.layout)


    def set_image(self, image):
        raise NotImplementedError