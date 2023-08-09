from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QFileDialog, QFormLayout
import os

class ControlWidgets(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        #layout = QVBoxLayout()
        layout = QFormLayout()

        self.open_button = QPushButton("Open file")
        self.range_selector_1_label = QLabel("Range selector 1")
        self.range_selector_1_status_start_step = QLineEdit()
        self.range_selector_1_status_start_hex_offset = QLineEdit()
        self.range_selector_1_status_end_step = QLineEdit()
        self.range_selector_1_status_end_hex_offset = QLineEdit()

        self.range_selector_2_label = QLabel("Range selector 2")
        self.range_selector_2_status_start_step = QLineEdit()
        self.range_selector_2_status_start_hex_offset = QLineEdit()
        self.range_selector_2_status_end_step = QLineEdit()
        self.range_selector_2_status_end_hex_offset = QLineEdit()

        layout.addWidget(self.open_button)
        layout.addWidget(self.range_selector_1_label)
        layout.addWidget(self.range_selector_1_status_start_step)
        layout.addWidget(self.range_selector_1_status_start_hex_offset)
        layout.addWidget(self.range_selector_1_status_end_step)
        layout.addWidget(self.range_selector_1_status_end_hex_offset)

        layout.addWidget(self.range_selector_2_label)
        layout.addWidget(self.range_selector_2_status_start_step)
        layout.addWidget(self.range_selector_2_status_start_hex_offset)
        layout.addWidget(self.range_selector_2_status_end_step)
        layout.addWidget(self.range_selector_2_status_end_hex_offset)


        self.setLayout(layout)
        self.setFixedWidth(120)

    # Return the file name
    def get_file_name(self):
        return QFileDialog.getOpenFileName(
            parent=self,
            caption="Open a file",
            directory=os.getcwd()
        )