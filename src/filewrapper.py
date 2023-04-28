"""
This file is a wrapper file for the same functions as in file.py
It wraps the FileAnalyzer.dll C# library
"""

# Set up the usage of the DLL
import clr
clr.AddReference("FileAnalyzer")
# Import the necessary objects / functions from the DLL
from FileAnalyzer import AnalyzedFile

# Python imports
import numpy as np
import os
from tkinter import filedialog as fd

filename = fd.askopenfile()
#file = AnalyzedFile("d:/a.txt")
file = AnalyzedFile(filename.name)

file.generate_2D_digraph_image()

numpy_array = np.fromiter(file.digraph_image, int)

pass