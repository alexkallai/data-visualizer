import file
from tkinter import filedialog as fd


if __name__ == "__main__":
    filename = fd.askopenfilename()
    with open(filename, "rb") as f:
        opened_file = file.File(f.read())
    opened_file.plot_2D_digraph()