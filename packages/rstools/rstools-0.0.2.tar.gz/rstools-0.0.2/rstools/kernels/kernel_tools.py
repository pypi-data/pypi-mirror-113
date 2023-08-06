# Fix paths for imports to work in unit tests ----------------

if __name__ == "__main__":
    
    from _fix_paths import fix_paths
    fix_paths()

# ------------------------------------------------------------

# Load libraries ---------------------------------------------

import numpy as np
import math

# ------------------------------------------------------------


def convolve(x, y):
    """
    Calculates the convolution of an array x and a kernel array y. If the length
    of y is odd, then the zero point of the kernel is set to the center index.
    If the length is even, the zero point is set to the smaller index of the two
    in the center. The length of y must be at least 2*len(x)-1. Central 2*len(x)-1
    elements of y will be used in the calculation.

    :param np.ndarray x: An array to be convolved with a kernel.
    :param np.ndarray y: The kernel to convolve with.
    :return: action_set convolution of x and y with the length of x.
    :rtype: np.ndarray
    """

    # result = np.array([0.0]*len(x))
    avg_y_index = int(math.floor(float(len(y) - 0.9) / 2))
    len_x = len(x)

    y_matrix = np.array([y[range(avg_y_index + n, avg_y_index + n - len_x, -1)]
                         for n in range(len(x))])
    with np.errstate(divide="ignore", invalid="ignore"):
        y_matrix = np.divide(y_matrix, np.sum(y_matrix, axis=1).reshape(len_x, 1))
    result_temp = x * y_matrix
    result = np.array([np.sum(result_temp[row]) for row in range(len_x)])
    #
    # for n in range(0, len(x)):
    #     indices = [i for i in range(avg_y_index + n, avg_y_index + n - len(x), -1)]
    #     y_transformed = np.array([y[i] for i in indices])
    #     y_transformed = y_transformed / sum(y_transformed)
    #     result[n] = np.dot(x, y_transformed)

    return result


def convolve_nan(x, y):
    """
    Calculates the convolution of an array x and a kernel array y. If the length
    of y is odd, then the zero point of the kernel is set to the center index.
    If the length is even, the zero point is set to the smaller index of the two
    in the center. The length of y must be at least 2*len(x)-1. Central 2*len(x)-1
    elements of y will be used in the calculation.

    Handles NaNs in x. If a NaN is encountered, this position and its weight
    are treated as nonexistent.

    :param np.ndarray x: An array to be convolved with a kernel.
    :param np.ndarray y: The kernel to convolve with.
    :return: action_set convolution of x and y with the length of x.
    :rtype: np.ndarray
    """

    avg_y_index = int(math.floor(float(len(y) - 0.9) / 2))
    len_x = len(x)

    y_matrix = np.array([np.where(~np.isnan(x),
                                  y[range(avg_y_index + n, avg_y_index + n - len_x, -1)],
                                  np.nan)
                         for n in range(len(x))])
    with np.errstate(divide="ignore", invalid="ignore"):
        y_matrix = np.divide(y_matrix, np.nansum(y_matrix, axis=1).reshape(len_x, 1))
    result_temp = x * y_matrix
    result = np.array([np.nansum(result_temp[row])
                       if not np.isnan(result_temp[row]).all()
                       else np.nan for row in range(len_x)])

    return result


def convolve_nan_slow(x, y):
    """
    Calculates the convolution of an array x and a kernel array y. If the length
    of y is odd, then the zero point of the kernel is set to the center index.
    If the length is even, the zero point is set to the smaller index of the two
    in the center. The length of y must be at least 2*len(x)-1. Central 2*len(x)-1
    elements of y will be used in the calculation.

    Handles NaNs in x. If a NaN is encountered, this position and its weight
    are treated as nonexistent.

    :param np.ndarray x: An array to be convolved with a kernel.
    :param np.ndarray y: The kernel to convolve with.
    :return: action_set convolution of x and y with the length of x.
    :rtype: np.ndarray
    """

    result = np.array([0.0]*len(x))
    avg_y_index = int(math.floor(float(len(y) - 0.9) / 2))

    for n in range(0, len(x)):
        result[n] = 0
        i = 0
        y_transformed = []

        for j in range(avg_y_index + n, avg_y_index + n - len(x), -1):
            if not np.isnan(x[i]):
                y_transformed.append(y[j])
                result[n] += x[i] * y[j]
            i += 1

        if sum(y_transformed) != 0:
            result[n] = result[n] / sum(y_transformed)
        else:
            result[n] = np.NaN

    return result


# ==============================================================================
# Unit tests
# ==============================================================================

if __name__ == "__main__":

    import unittest


    class TestConvolve(unittest.TestCase):
        def test_convolve(self):
            print("Convolve test -------------")

            result = convolve(np.array([0.0, 1.0, 2.0, 1.0, 0.0]),
                              np.array([0.0, 0.0, 0.0, 0.0, 0.333, 0.333, 0.333,
                                        0.0, 0.0, 0.0, 0.0]))

            print(result)

            self.assertEquals(len(result), 5)
            self.assertAlmostEqual(result[0], 0.5)
            self.assertAlmostEqual(result[1], 1.0)
            self.assertAlmostEqual(result[2], 1.333333333333)
            self.assertAlmostEqual(result[3], 1.0)
            self.assertAlmostEqual(result[4], 0.5)

            print("")

        def test_convolve_nan(self):
            print("Convolve with NaNs test -------------")

            # First case

            result = convolve_nan(np.array([np.nan, 1.0, 2.0]),
                                  np.array([0.0, 0.0, 0.333, 0.333, 0.333, 0.0, 0.0]))

            print(result)

            self.assertEquals(len(result), 3)
            self.assertEquals(result[0], 1.0)
            self.assertAlmostEqual(result[1], 1.5)
            self.assertAlmostEqual(result[2], 1.5)

            # Second case

            result = convolve_nan(np.array([0.0, 1.0, 2.0, np.nan, np.nan, np.nan, 1.0, 2.0, 1.0]),
                                  np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.333,
                                            0.333, 0.333, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]))

            print(result)

            self.assertEquals(len(result), 9)
            self.assertAlmostEqual(result[0], 0.5)
            self.assertAlmostEqual(result[1], 1.0)
            self.assertAlmostEqual(result[2], 1.5)
            self.assertAlmostEqual(result[3], 2.0)
            self.assertTrue(np.isnan(result[4]))
            self.assertAlmostEqual(result[5], 1.0)
            self.assertAlmostEqual(result[6], 1.5)
            self.assertAlmostEqual(result[7], 1.333333333)
            self.assertAlmostEqual(result[8], 1.5)

            # Third case

            result = convolve_nan(np.array([np.nan, np.nan, np.nan, 0.0, 1.0, 2.0, 1.0, 2.0, 1.0]),
                                  np.array([0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.333,
                                            0.333, 0.333, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]))

            print(result)

            self.assertEquals(len(result), 9)
            self.assertAlmostEqual(result[0], 0.5)
            self.assertAlmostEqual(result[1], 1.0)
            self.assertAlmostEqual(result[2], 1.5)
            self.assertAlmostEqual(result[3], 2.0)
            self.assertTrue(np.isnan(result[4]))
            self.assertAlmostEqual(result[5], 1.0)
            self.assertAlmostEqual(result[6], 1.5)
            self.assertAlmostEqual(result[7], 1.333333333)
            self.assertAlmostEqual(result[8], 1.5)

            print("")


    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestConvolve))
    unittest.TextTestRunner().run(suite)



