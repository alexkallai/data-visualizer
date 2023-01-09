from PyQt5.QtWidgets import QFileDialog
import os


# Return the file name
def get_file_name():
    return QFileDialog.getOpenFileName(
        parent=None,
        caption="Open a file",
        directory=os.getcwd()
    )