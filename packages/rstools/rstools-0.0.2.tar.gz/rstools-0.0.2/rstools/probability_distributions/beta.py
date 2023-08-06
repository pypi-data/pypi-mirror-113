# Fix paths for imports to work in unit tests ----------------

if __name__ == "__main__":

    from _fix_paths import fix_paths
    fix_paths()

# ------------------------------------------------------------

# Load libraries ---------------------------------------------

import numpy as np

# ------------------------------------------------------------


def get_beta_dist_variance(s, n):
    """
    Calculate beta distribution variance for given number of successes and trials

    :param s: Number of successes
    :param n: Number of trails
    :return:
    """
    return ((s + 1)*(n - s + 1)) / ((n + 2)**2 * (n + 3))


def get_beta_dist_std_deviation(s, n):
    """
    Calculate beta distribution standard deviation for given number of successes and trials

    :param s: Number of successes
    :param n: Number of trails
    :return:
    """
    return np.sqrt(((s + 1)*(n - s + 1)) / ((n + 2)**2 * (n + 3)))


def get_beta_dist_mean(s, n):
    """
    Calculate beta distribution mean for given number of successes and trials

    :param s: Number of successes
    :param n: Number of trails
    :return:
    """
    return (s + 1) / (n + 2)
