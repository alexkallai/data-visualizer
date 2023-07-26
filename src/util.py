from PyQt5.QtWidgets import QFileDialog
import os
from time import time


# Return the file name
def get_file_name():
    return QFileDialog.getOpenFileName(
        parent=None,
        caption="Open a file",
        directory=os.getcwd()
    )

def timer(func):
    # This function shows the execution time of 
    # the function object passed
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2-t1):.4f}s')
        return result
    return wrap_func