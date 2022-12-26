from settings import *
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors

class File:
    """
    8 bit = 1 byte -> 2^4 * 2^4 = 16 * 16 = 256
    """

    def __init__(self, raw_binary_file: bytes) -> None:
        size_in_bytes: int = len(raw_binary_file)
        CHUNK_SIZE = 1 # byte
        # the first and last element will only be drawn once
        # and the +1 is for the odd length
        array_length = int((size_in_bytes + 1 ) / 2) - 2
        self.hexa_pair_array = np.zeros(shape=(array_length, 2), dtype=np.uint16)
        for index, byte in enumerate(raw_binary_file):
            if index == array_length - 1:
                break
            self.hexa_pair_array[index] = (byte, raw_binary_file[index+1])
        
        self.hexa_pair_unique_array, self.hexa_pair_unique_array_counts = self.get_unique_array_and_counts(self.hexa_pair_array)
    
    def get_unique_array_and_counts(self, array):
        return np.unique(array, return_counts=True, axis=0)
    
    def plot_2D_digraph(self, raw_binary_file_slice: bytes = None):
        if not raw_binary_file_slice:
            raw_binary_file_slice = self.hexa_pair_unique_array
            color_info = self.hexa_pair_unique_array_counts
        else:
            raw_binary_file_slice, color_info = self.get_unique_array_and_counts(raw_binary_file_slice)

        normalize = colors.LogNorm(vmin=color_info.min(), vmax=color_info.max())
        plt.axes().set_facecolor("black")
        plt.scatter(x=raw_binary_file_slice[:, 0], 
                    y=raw_binary_file_slice[:, 1],
                    c=color_info,
                    s=2,
                    cmap="magma",
                    norm=normalize)
        plt.show()