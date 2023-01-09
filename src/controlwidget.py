from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton ,QFileDialog
import os

class ControlWidgets(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout()

        open_button = QPushButton("Open file")
        open_button.clicked.connect(self.get_file_name)
        layout.addWidget(open_button)

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