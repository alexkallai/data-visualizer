import file
from tkinter import filedialog as fd


if __name__ == "__main__":
    filenames = fd.askopenfilenames()
    for filename in filenames:
        with open(filename, "rb") as f:
            opened_file = file.File(f.read())
            opened_file.plot_2D_digraph()
            opened_file.plot_3D_digraph()
