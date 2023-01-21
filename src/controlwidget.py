from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QFileDialog, QFormLayout
import os

class ControlWidgets(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        #layout = QVBoxLayout()
        layout = QFormLayout()

        self.open_button = QPushButton("Open file")
        #self.open_button.clicked.connect(self.get_file_name)
        # Labels
        self.filename_label = QLabel("File name:")
        self.path_label = QLabel("Path:")
        self.SHA256_label = QLabel("SHA256:")
        self.MD5_label = QLabel("MD5:")

        # Lines
        self.filename_edit = QLineEdit("-")
        self.path_edit = QTextEdit("-")
        self.SHA256_edit = QTextEdit("-")
        self.MD5_edit = QTextEdit("-")

        self.path_edit.height

        layout.addWidget(self.open_button)
        layout.addWidget(self.filename_label)
        layout.addWidget(self.filename_edit)
        layout.addWidget(self.path_label)
        layout.addWidget(self.path_edit)
        layout.addWidget(self.SHA256_label)
        layout.addWidget(self.SHA256_edit)
        layout.addWidget(self.MD5_label)
        layout.addWidget(self.MD5_edit)

        self.setLayout(layout)
        self.setFixedWidth(250)

    # Return the file name
    def get_file_name(self):
        return QFileDialog.getOpenFileName(
            parent=self,
            caption="Open a file",
            directory=os.getcwd()
        )

    def set_filename(self, arg: str) -> None:
        self.filename_edit.setText(arg)

    def set_path(self, arg: str) -> None:
        self.path_edit.setText(arg)

    def set_sha256(self, arg: str) -> None:
        self.SHA256_edit.setText(arg)

    def set_md5(self, arg: str) -> None:
        self.MD5_edit.setText(arg)