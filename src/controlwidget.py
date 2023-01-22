from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QFileDialog, QFormLayout
import os

class ControlWidgets(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        #layout = QVBoxLayout()
        layout = QFormLayout()

        self.open_button = QPushButton("Open file")
        layout.addWidget(self.open_button)

        self.setLayout(layout)
        self.setFixedWidth(100)

    # Return the file name
    def get_file_name(self):
        return QFileDialog.getOpenFileName(
            parent=self,
            caption="Open a file",
            directory=os.getcwd()
        )