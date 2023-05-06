from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QFileDialog
from hilbertcurve.hilbertcurve import HilbertCurve
from util import timer
from itertools import groupby
from matplotlib import colormaps
from matplotlib import colors, cm
from matplotlib import pyplot as plt
from pathlib import Path
import hashlib
import math
import numpy as np
import os
import sys

try:
    from itertools import pairwise
except:
    # about 40% slower than itertools.pairwise,
    # but that's available from python 3.10 only
    def pairwise(iterable):
        for x in zip(iterable, iterable[1:]):
            yield x


class File:
    """
    8 bit = 1 byte -> 2^4 * 2^4 = 16 * 16 = 256
    """

    def __init__(self, path=None) -> None:
        self.path = None

        if path == None:
            path, filter = self.get_file_name()
        if path:
            try:
                with open(path, "rb") as f:
                    self.raw_binary_file  = np.frombuffer(f.read(), dtype=np.uint8)
            except Exception as e:
                print(f"There was problem with reading in the file: \n{e}")
                return
        else:
            return
        self.path = path

        print(f"The size of the bytes file object is: {sys.getsizeof(self.raw_binary_file)}")
        self.size_in_bytes: int = len(self.raw_binary_file)
        self.folder_path = self.path
        self.file_name = str(os.path.split(self.path)[-1])
        #self.hexa_pair_array = self.generate_hexa_pair_array()
        #self.hexa_pair_unique_array, self.hexa_pair_unique_array_counts = self.get_unique_array_and_counts(self.hexa_pair_array)

    # Select the file and return the path
    def get_file_name(self) -> tuple[str, str]:
        return QFileDialog.getOpenFileName(
            parent=None,
            caption="Open a file",
            directory=os.getcwd()
        )

    @timer
    def get_2D_digraph_image(self, slice=None) -> np.ndarray:
        """
        This function returns the 256 x 256 (1 byte) pixels sized image where the
        values are the number of occurrences of the plotted (byte, byte+1) pair
        """
        
        if not slice:
            slice = self.raw_binary_file

        digraph_image = np.zeros(shape=(256, 256), dtype=np.uint16)

        # itertool pairwise solution
        for res in groupby(pairwise(slice)):
            digraph_image[ res[0][0] ][ res[0][1] ] = len(list( res[1] )) 

        return digraph_image

    @timer
    def get_2D_hilbert_iterations_number(self):
        """
        Iteration 1 - 4 members:  4^x -> x = 1
        Iteration 2 - 16 members: 4^x -> x = 2
        Iteration 3 - 64 members: 4^x -> x = 3
        x = log(length) / log(4)
        """

        return math.ceil( math.log10(self.size_in_bytes) / math.log10(4) )

    @timer
    def get_2D_hilbert_image(self, slice=None) -> np.ndarray:
        """
        This function returns the ? x ? sized image that is the 2D representation
        of the 1D byte series
        The hilbert curve's size _quadruples_ in 2D every iteration!
        """

        if not slice:
            slice = self.raw_binary_file

        NUMBER_OF_DIMENSIONS = 2
        number_of_iterations = self.get_2D_hilbert_iterations_number()
        print(f"Number of hilbert curve iterations: {number_of_iterations}")
        hilbert_curve = HilbertCurve(p=number_of_iterations, n=NUMBER_OF_DIMENSIONS, n_procs=-1)

        slice = np.frombuffer(slice, dtype=np.uint8)
        # Create a suitably sized array
        hilbert_array_side_length = int(math.pow(2, number_of_iterations))
        hilbert_array = np.zeros( ( hilbert_array_side_length, hilbert_array_side_length), dtype=np.uint8 )
        
        # Zip method
        for point in zip(slice,
                         hilbert_curve.points_from_distances(distances=range(self.size_in_bytes))):
            hilbert_array[ point[1][1] ][ point[1][0] ] = point[0]

        return hilbert_array

    @timer
    def get_3D_hilbert_iterations_number(self) -> int:
        """
        Iteration 1 - 8 members:   8^x -> x = 1
        Iteration 2 - 64 members:  8^x -> x = 2
        Iteration 3 - 512 members: 8^x -> x = 3
        x = log(length) / log(4)
        """

        return math.ceil( math.log10(self.size_in_bytes) / math.log10(8) )

    @timer
    def get_3D_hilbert_image(self, slice=None) -> np.ndarray:
        """
        This function returns the ? x ? x ? sized image that is the 3D representation
        of the 1D byte series
        The hilbert curve's size _x8_ in 3D every iteration!
        """
        
        # Set up colormap
        normalizer = colors.Normalize(vmin=0.0, vmax=1.0, clip=True)
        colormapper = cm.ScalarMappable(norm=normalizer, cmap=colormaps['viridis'])

        if not slice:
            slice = self.raw_binary_file

        NUMBER_OF_DIMENSIONS = 3
        number_of_iterations = self.get_3D_hilbert_iterations_number()
        print(f"Number of 3D hilbert curve iterations: {number_of_iterations}")
        hilbert_curve = HilbertCurve(p=number_of_iterations, n=NUMBER_OF_DIMENSIONS, n_procs=-1)

        slice_original = np.frombuffer(slice, dtype=np.uint8)
        slice = colormapper.to_rgba(np.frombuffer(slice, dtype=np.uint8), alpha=False, bytes=False, norm=True)[:,:3]
        slice = np.array(slice, dtype=np.float32)
        # Create a suitably sized array
        array_side_len = int(math.pow(2, number_of_iterations))
        list_of_coords = np.zeros( (self.size_in_bytes, 3), dtype=np.uint8 )
        list_of_colors = np.zeros( (self.size_in_bytes, 3), dtype=np.float32)

        def map_byte_to_color(byte):
            color_component = (byte/256)
            viridis = colormaps['viridis']
            return viridis(color_component)[:3]

        # Zip method
        for index, point in enumerate(zip(slice_original,
                                          hilbert_curve.points_from_distances(distances=range(self.size_in_bytes)))):
            #list_of_coords[index][0] = point[1][0]
            #list_of_coords[index][1] = point[1][1]
            #list_of_coords[index][2] = point[1][2]
            list_of_coords[index] = point[1]
            # TODO very slow:
            list_of_colors[index] = map_byte_to_color(point[0])

        print("Equals?")
        print(np.array_equal( slice, list_of_colors, equal_nan=False))
        return list_of_coords, list_of_colors

    @timer
    def get_unique_array_and_counts(self, array):
        return np.unique(array, return_counts=True, axis=0)

    @timer
    def get_bin_file_slice(self, begin_percent=0, end_percent=100) -> bytes:
        # 0-100
        begin_percent_index = int((self.size_in_bytes * begin_percent) / 100)
        end_percent_index = int((self.size_in_bytes * end_percent) / 100)

        return self.raw_binary_file[begin_percent_index:end_percent_index]

    @timer
    def get_slices_by_amount(self, number_of_slices, unique_array, unique_array_counts):
        list_of_arrays = []
        array_length = len(unique_array)
        slice_length = int(array_length = number_of_slices)
        for i in range(number_of_slices):
            list_of_arrays.append((unique_array[i*slice_length : (i+1)*slice_length], 
                                   unique_array_counts[i*slice_length : (i+1)*slice_length]))
        return list_of_arrays

    '''
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
    '''

    @timer
    def get_2D_array_sizes_with_aspect_ratio(self, length: int, aspect_ratio: int) -> tuple[int, int]:
        """
        Return the width, and height based on the length and aspect ratio
        """

        side_width = int(math.sqrt(length / aspect_ratio)) + 1
        side_height = int(length / side_width) + 1

        return side_width, side_height


    @timer
    def get_byteplot_PIL_image(self, slice=None, max_width=400, ratio=4, downsample=False) -> np.ndarray:
        """
        max_width: maximum number of pixels allowed in the output (NOTE: it's after downsampling)
        ratio: y / x (height / width)
        downsample: if downsampling should happen
        """

        if not slice:
            slice = self.raw_binary_file

        # Read in the file
        width, height = self.get_2D_array_sizes_with_aspect_ratio(self.size_in_bytes, ratio)

        print(f"Init width: { width}")
        print(f"Init height: { height}")
        print(f"Len: {self.size_in_bytes}")

        # Pad the remaining space with zeroes by appending an empty array so the
        # 1D array can be reshaped to 2D
        array2D = np.append(slice, np.zeros(((width*height)-self.size_in_bytes), np.uint8))
        array2D = array2D.reshape((height, width))

        # Downsample the array by keeping its ratio ???
        sampling_no = width / max_width
        if sampling_no > 1 and downsample:
            sampling_no = int(sampling_no) 
            return array2D[::sampling_no, ::sampling_no]

        return array2D

    @timer
    def apply_colormap_to_image(array: np.ndarray) -> np.ndarray:
        raise NotImplementedError

    @timer
    def get_qpixmap_from_PIL_image(self, image: np.ndarray) -> QPixmap:
        height, width = image.shape
        qt_image = QImage(image, width, height, width, QImage.Format_Grayscale8)
        return QPixmap(qt_image)

    @timer
    def sha256_hash(self) -> str:
        return hashlib.sha256(self.raw_binary_file).hexdigest()

    @timer
    def md5_hash(self) -> str:
        return hashlib.md5(self.raw_binary_file).hexdigest()


if __name__ == "__main__":
    testfile = File(str(__file__))
    image = testfile.get_byteplot_PIL_image()
    testfile.get_2D_hilbert_image()
    testfile.get_2D_digraph_image()