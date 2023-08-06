# Fix paths for imports to work in unit tests ----------------

if __name__ == "__main__":
    
    from _fix_paths import fix_paths
    fix_paths()

# ------------------------------------------------------------

# Load libraries ---------------------------------------------

import numpy as np
from scipy.stats import norm
import math

# ------------------------------------------------------------


def get_discrete_kernel(kernel_type="gaussian", kernel_width=1, length=31):
    """
    Generates a discrete kernel of a given type, width and length.

    :param str kernel_type: Type of the kernel: "gaussian".
    :param float kernel_width: Standard deviation for gaussian.
    :param int length: Length of the kernel.
    :return: Kernel in a form of a numpy array of length given by argument length.
        The density center of the kernel is on the central index if length is odd,
        and on the first index preceding length / 2 if length is even.
    :rtype: np.ndarray
    """
    
    kernel = np.array([0.0]*length)
    avg_index = int(math.floor(float(length - 0.9) / 2))
    
    for index in range(0, length):
        if kernel_type == "gaussian":
            kernel[index] = norm.pdf(index, avg_index, kernel_width)
    
    kernel = kernel / sum(kernel)
    
    return kernel


def get_gaussian_kernel(std=1, length=31):
    """
    Generates a gaussian kernel of a given width and length.

    :param float std: Standard deviation for gaussian.
    :param int length: Length of the kernel.
    :return: Kernel in a form of a numpy array of length given by argument length.
        The density center of the kernel is on the central index if length is odd,
        and on the first index preceding length / 2 if length is even.
    :rtype: np.ndarray
    """

    avg_index = int(math.floor(float(length - 0.9) / 2))

    kernel = norm.pdf(np.arange(0, length, 1), avg_index, std)

    kernel = kernel / sum(kernel)

    return kernel


def get_uniform_kernel(width=1, length=31):
    """
    Generates a uniform kernel of a given width and length. A convolution
    with this kernel gives a moving average.

    :param float width: Number of non-zero elements.
    :param int length: Length of the kernel.
    :return: Kernel in a form of a numpy array of length given by argument length.
        The center of the kernel is on the central index if length is odd,
        and on the first index preceding length / 2 if length is even.
    :rtype: np.ndarray
    """

    kernel = np.array([0.0]*length)
    idx_from = max(int(math.floor(float(length - 0.5) / 2)) - int(math.floor(float(width - 0.5) / 2)), 0)
    idx_to = min(idx_from + width, length - 1)  # idx_to doesn't have -1 because it is used in numpy array slice

    kernel[idx_from:idx_to] = 1.0

    kernel = kernel / sum(kernel)

    return kernel
