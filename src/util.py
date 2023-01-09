from PyQt5.QtWidgets import QFileDialog
import os


# Return the file name
def get_file_name(self):
    return QFileDialog.getOpenFileName(
        parent=self,
        caption="Open a file",
        directory=os.getcwd()
    )