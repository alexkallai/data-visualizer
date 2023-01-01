from settings import *
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors

class File:
    """
    8 bit = 1 byte -> 2^4 * 2^4 = 16 * 16 = 256
    """

    def __init__(self, raw_binary_file: bytes) -> None:
        self.raw_binary_file = raw_binary_file
        self.size_in_bytes: int = len(raw_binary_file)
        self.hexa_pair_array = self.generate_hexa_pair_array()
        self.hexa_pair_unique_array, self.hexa_pair_unique_array_counts = self.get_unique_array_and_counts(self.hexa_pair_array)
    
    def generate_hexa_pair_array(self, slice=None):
        if not slice:
            slice = self.raw_binary_file
        # the first and last element will only be drawn once
        # and the +1 is for the odd length
        array_length = int((len(slice) + 1 ) / 2) - 2
        hexa_pair_array = np.zeros(shape=(array_length, 3), dtype=np.uint16)
        for index, byte in enumerate(slice):
            if index == array_length - 1:
                break
            hexa_pair_array[index][0] = byte # byte plus next byte
            hexa_pair_array[index][1] = slice[index+1] # byte plus next byte
            hexa_pair_array[index][2] = index
        return hexa_pair_array
    
    def get_unique_array_and_counts(self, array):
        return np.unique(array, return_counts=True, axis=0)

    def get_bin_file_slice(self, begin_percent=0, end_percent=100):
        # 0-100
        array_length = len(self.raw_binary_file)
        begin_percent_index = int((array_length * begin_percent) / 100)
        end_percent_index = int((array_length * end_percent) / 100)

        return self.raw_binary_file[begin_percent_index:end_percent_index]
    
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

    def get_slices_by_amount(self, number_of_slices, unique_array, unique_array_counts):
        list_of_arrays = []
        array_length = len(unique_array)
        slice_length = int(array_length = number_of_slices)
        for i in range(number_of_slices):
            list_of_arrays.append((unique_array[i*slice_length : (i+1)*slice_length], 
                                   unique_array_counts[i*slice_length : (i+1)*slice_length]))
        return list_of_arrays


    def plot_3D_digraph(self, unique_array_of_file_slice: bytes = None):
        NUMBER_OF_SLICES = 10
        if not unique_array_of_file_slice:
            unique_array_of_file_slice = self.hexa_pair_unique_array
            color_info = self.hexa_pair_unique_array_counts
        else:
            unique_array_of_file_slice , color_info = self.get_unique_array_and_counts(unique_array_of_file_slice)
        #list_of_slices = np.ndarray( NUMBER_OF_SLICES, dtype= )
        list_of_slices = []
        increment = int(100 / NUMBER_OF_SLICES)
        for i in range(NUMBER_OF_SLICES):
            if i == NUMBER_OF_SLICES-1:
                break
            list_of_slices.append(
                self.get_unique_array_and_counts(
                    self.generate_hexa_pair_array(
                        self.get_bin_file_slice(i*increment, (i+1)*increment))))

        normalize = colors.LogNorm(vmin=color_info.min(), vmax=color_info.max())
        plt.axes(projection="3d")

        for index, slice in enumerate(list_of_slices):
            plt.axes(projection="3d")
            plt.scatter(slice[0][:, 0],
                        slice[0][:, 1],
                        #index,
                        s=1,
                        c=slice[1],
                        cmap="magma",
                        norm=normalize)
            plt.show()



        #ax.set_facecolor("black")
        plt.scatter(unique_array_of_file_slice[:, 0],
                    unique_array_of_file_slice[:, 1],
                    s=1,
                    c=color_info,
                    cmap="magma",
                    norm=normalize)
        plt.show()
