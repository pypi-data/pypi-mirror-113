# Fix paths for imports to work in unit tests ----------------

if __name__ == "__main__":
    
    from _fix_paths import fix_paths
    fix_paths()

# ------------------------------------------------------------

# Load libraries ---------------------------------------------

import numpy as np
import math
from scipy.optimize import fsolve

# ------------------------------------------------------------


def lw(x):
    """
    Lambert W function (the inverse to x e^{x}), for real x >= 0.

    :param float x: The input value.
    :return: Lambert W function value for x.
    :rtype: float
    """

    def func(w, x):
        return np.log(x) - np.log(w) - w

    if x == 0:
        return 0
    if x > 2.5:
        lnx = np.log(x)
        w0 = lnx - np.log(lnx)
    elif x > 0.25:
        w0 = 0.8 * np.log(x + 1)
    else:
        w0 = x * (1.0 - x)

    return fsolve(func, w0, args=(x,))[0]


def lwexpapp(a, x):
    """
    Returns an approximation of the W(exp(a + x)) value (W is the Lambert W function)
    for small constant a and x large. Allows to calculate the value of this function
    for larger x, which is not possible directly due to an overflow in exp.

    :param float a: action_set parameter.
    :param float x: The function variable.
    :return: An approximation of the W(exp(a + x)) value.
    :rtype: float
    """
    return x * (1 - (math.log(x) - a) / (1 + x))


def lambertw(var):
    """
    Applies Lambert W function to a list, array or a number. For a list or array
    an numpy array is returned, for a number a single value is returned.

    :param Union[list, np.ndarray, float] var: Input.
    :return: Array of values or a single value of Lambert W function on the input.
    :rtype: Union[np.ndarray, float]
    """

    if type(var) == list:
        return np.array([lw(x) for x in var])
    else:
        return lw(var)


def lambertwexp(var):
    """
    Returns the value of a superposition of Lambert W function and exp function,
    which can be applied to larger inputs due to the use of an approximation.

    :param Union[list, np.ndarray, float] var: Input variable in the form
        of a list, numpy array or a number.
    :return: Array of values or a single value of Lambert W function
        composed with exp on the input.
    :rtype: Union[np.ndarray, float]
    """

    if type(var) == list:
        return np.array([(lw(math.exp(x)) if x < 709 else lwexpapp(0, x)) for x in var])
    else:
        return lw(math.exp(var)) if var < 709 else lwexpapp(0, var)
