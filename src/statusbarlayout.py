from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QFileDialog, QHBoxLayout, QFormLayout
from PyQt5 import QtCore
from PyQt5.QtGui import *

class StatusBarLayout(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QFormLayout()

        # Labels
        self.filename_label = QLabel("File name:")
        self.path_label = QLabel("Path:")
        self.SHA256_label = QLabel("SHA256:")
        self.MD5_label = QLabel("MD5:")

        # Set font
        for label in (self.filename_label,
                      self.path_label,
                      self.SHA256_label,
                      self.MD5_label):
            label.setFont(QFont("MonoSpace", pointSize=9, weight=500))
            label.setAlignment(QtCore.Qt.AlignLeft)

        # Lines
        self.filename_edit =  QLabel("-")
        self.path_edit =      QLabel("-")
        self.SHA256_edit =    QLabel("-")
        self.MD5_edit =       QLabel("-")

        # Set selectable property and font
        for label in (self.filename_edit,
                      self.path_edit,
                      self.SHA256_edit,
                      self.MD5_edit):
            label.setFont(QFont("MonoSpace", pointSize=9, weight=5))
            label.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
            label.setAlignment(QtCore.Qt.AlignLeft)

        self.row_layout_1 = QHBoxLayout()
        self.row_layout_2 = QHBoxLayout()
        self.row_layout_1.addWidget(self.filename_label)
        self.row_layout_1.addWidget(self.filename_edit)
        self.row_layout_1.addWidget(self.path_label)
        self.row_layout_1.addWidget(self.path_edit)
        self.row_layout_2.addWidget(self.SHA256_label)
        self.row_layout_2.addWidget(self.SHA256_edit)
        self.row_layout_2.addWidget(self.MD5_label)
        self.row_layout_2.addWidget(self.MD5_edit)

        layout.addRow(self.row_layout_1)
        layout.addRow(self.row_layout_2)

        self.setLayout(layout)
        #self.setFixedWidth(250)

    def set_filename(self, arg: str) -> None:
        self.filename_edit.setText(arg)

    def set_path(self, arg: str) -> None:
        self.path_edit.setText(arg)

    def set_sha256(self, arg: str) -> None:
        self.SHA256_edit.setText(arg)

    def set_md5(self, arg: str) -> None:
        self.MD5_edit.setText(arg)