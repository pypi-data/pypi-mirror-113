# Fix paths for imports to work in unit tests ----------------

if __name__ == "__main__":

    from _fix_paths import fix_paths
    fix_paths()

# ------------------------------------------------------------

# Load libraries ---------------------------------------------

import numpy as np
import pandas as pd

# ------------------------------------------------------------


def fit_binomial_model(var_x, var_y, b):


    lambda_0 = (var_y + np.sqrt(var_x * (b - var_y) + b * var_y)) / (var_x + var_y)
    return np.minimum(1, lambda_0)
