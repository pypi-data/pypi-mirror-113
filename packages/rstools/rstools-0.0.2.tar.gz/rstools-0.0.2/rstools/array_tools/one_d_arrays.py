# Fix paths for imports to work in unit tests ----------------

if __name__ == "__main__":
    
    from _fix_paths import fix_paths
    fix_paths()

# ------------------------------------------------------------

# Load libraries ---------------------------------------------

import numpy as np

# ------------------------------------------------------------


def find_almost_equal(array, value, delta):
    """
    Returns indices of elements within delta of value in the given array.

    :param np.ndarray array: Array.
    :param float value: Value to be found.
    :param float delta: Highest negligible difference between value and actual
        array elements which are considered equal.
    :return: Indices of elements within delta of value in the given array.
    :rtype: np.ndarray
    """
    
    indices = []

    for idx in range(len(array)):
        if abs(value - array[idx]) <= delta:
            indices.append(idx)
    
    return np.array(indices)


# ==============================================================================
# Unit tests
# ==============================================================================

if __name__ == "__main__":

    import unittest


    class TestOneDArrayTools(unittest.TestCase):
        def test_find_almost_equal(self):
            print("find_almost_equal test -------------")

            result = find_almost_equal(np.array([4.0, 4.4, 4.5, 5.0, 6.0, 5.49, 5.5, 3.0]),
                                       5.0, 0.5)

            print(result)

            self.assertEquals(result[0], 2)
            self.assertEquals(result[1], 3)
            self.assertEquals(result[2], 5)
            self.assertEquals(result[3], 6)

            print("")


    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestOneDArrayTools))
    unittest.TextTestRunner().run(suite)
