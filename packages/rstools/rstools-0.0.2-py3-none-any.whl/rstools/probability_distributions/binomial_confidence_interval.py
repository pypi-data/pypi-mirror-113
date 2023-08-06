# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 18:05:38 2018

@author: ziolo
"""

# Fix paths for imports to work in unit tests ----------------

if __name__ == "__main__":
    from _fix_paths import fix_paths

    fix_paths()

# ------------------------------------------------------------


import functools

import numpy as np
import pickle
import scipy
import os
from scipy.optimize import bisect
from scipy.stats import norm


exact_ci_lengths_df = None


def standard_z_score(alpha, test_type="two-sided"):
    if test_type == "two-sided":
        return norm.ppf(1 - alpha / 2)
    elif test_type == "one-sided":
        return norm.ppf(1 - alpha)
    else:
        raise Exception("Wrong type")


@functools.lru_cache(50000)
def get_binomial_probability(s, n, p):
    """
    :param int s: Number of successes.
    :param int n: Number of trials.
    :param float p: Probability of a success.
    :return: Probability of the observed number of successes.
    :rtype: float
    """

    p_used = 0
    q_used = 0
    newton_used = 0

    max_p_used = s
    max_q_used = n - s
    max_newton_used = s

    newton_numerator = float(n)
    newton_denominator = 1.0

    obs_prob = 1

    while p_used < max_p_used and newton_used < max_newton_used:
        if obs_prob >= 1:
            obs_prob *= p
            p_used += 1
        else:
            obs_prob *= newton_numerator / newton_denominator
            newton_numerator -= 1.0
            newton_denominator += 1.0
            newton_used += 1

    while q_used < max_q_used and newton_used < max_newton_used:
        if obs_prob >= 1:
            obs_prob *= 1 - p
            q_used += 1
        else:
            obs_prob *= newton_numerator / newton_denominator
            newton_numerator -= 1.0
            newton_denominator += 1.0
            newton_used += 1

    while p_used < max_p_used:
        obs_prob *= p
        p_used += 1

    while q_used < max_q_used:
        obs_prob *= 1 - p
        q_used += 1

    while newton_used < max_newton_used:
        obs_prob *= newton_numerator / newton_denominator
        newton_numerator -= 1.0
        newton_denominator += 1.0
        newton_used += 1

    return obs_prob


@functools.lru_cache(50000)
def binomial_cumulative(s, n, p):
    return scipy.stats.binom.cdf(s, n, p)


def reversed_binomial_cumulative(s, n, p):
    return 1-binomial_cumulative(s - 1, n, p)


@functools.lru_cache(1000)
def get_exact_ci_for_binomial_distribution(s, n, alpha):
    """
    :param int s: Number of successes.
    :param int n: Number of trials.
    :param float alpha: Confidence level.
    :return: Bounds of the exact confidence interval (Clopper-Pearson method).
    :rtype: np.ndarray
    """

    if int(n) == 0:
        return np.array([0.0, 1.0])

    s = max(min(n, s), 0)

    low = lambda pl: reversed_binomial_cumulative(s, n, pl) - alpha / 2
    up = lambda pu: binomial_cumulative(s, n, pu) - alpha / 2

    return np.array([bisect(low, 0, 1) if s != 0 else 0.0,
                     bisect(up, 0, 1) if s != n else 1.0])


def get_normal_ci_for_binomial_distribution(s, n, alpha):
    """
    :param int s: Number of successes.
    :param int n: Number of trials.
    :param float alpha: Confidence level.
    :return: Bounds of the exact confidence interval (based on the normal
        approximation).
    :rtype: np.ndarray
    """

    if int(n) == 0:
        return np.array([0.0, 1.0])

    s = max(min(n, s), 0)

    p = float(s) / n
    z = standard_z_score(alpha)

    return np.array([p - z * np.sqrt(p * (1 - p) / n),
                     p + z * np.sqrt(p * (1 - p) / n)])


def get_wilson_ci_for_binomial_distribution(s, n, alpha):
    """
    :param int s: Number of successes.
    :param int n: Number of trials.
    :param float alpha: Confidence level.
    :return: Bounds of the exact confidence interval (based on the Wilson
        approximation).
    :rtype: np.ndarray
    """

    if int(n) == 0:
        return np.array([0.0, 1.0])

    s = max(min(n, s), 0)

    p = float(s) / n
    z = standard_z_score(alpha)

    return np.array([(p + z**2 / (2 * n)) / (1 + z**2 / n) - z / (1 + z**2 / n)
                     * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)),
                     (p + z**2 / (2 * n)) / (1 + z**2 / n) + z / (1 + z**2 / n)
                     * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2))])


def get_naive_ci_for_binomial_distribution(s, n, alpha):
    """
    :param int s: Number of successes.
    :param int n: Number of trials.
    :param float alpha: Confidence level.
    :return: Bounds of the confidence interval (built symmetrically around s).
    :rtype: np.ndarray
    """

    if int(n) == 0:
        return np.array([0.0, 1.0])

    s = max(min(n, s), 0)

    p = float(s) / n

    center = s
    previous_lower_bound = center
    previous_upper_bound = center

    previous_interval = np.array([previous_lower_bound, previous_upper_bound])
    previous_probability = 0

    next_interval = np.array([previous_lower_bound, previous_upper_bound])
    next_probability = get_binomial_probability(center, n, p)

    while next_probability < 1 - alpha:
        next_lower_bound = max(previous_lower_bound - 1, 0)
        next_upper_bound = min(previous_upper_bound + 1, n)

        previous_interval = next_interval
        previous_probability = next_probability

        next_interval = np.array([next_lower_bound, next_upper_bound])

        next_probability = next_probability \
            + (get_binomial_probability(next_lower_bound, n, p) if previous_lower_bound != 0 else 0.0) \
            + (get_binomial_probability(next_upper_bound, n, p) if previous_upper_bound != n else 0.0)

        previous_lower_bound = next_lower_bound
        previous_upper_bound = next_upper_bound

    if abs(previous_probability - (1 - alpha)) \
            < abs(next_probability - (1 - alpha)):
        ci = previous_interval
    else:
        ci = next_interval

    return ci.astype(float) / n


def get_ci_for_binomial(s, n, alpha):
    if type(n) == list or type(n) == np.ndarray:
        result = []
        for idx in range(len(n)):
            if int(n[idx]) <= 500:
                get_ci = get_exact_ci_for_binomial_distribution
            else:
                get_ci = get_wilson_ci_for_binomial_distribution
            ci = get_ci(int(s[idx]), int(n[idx]), alpha)
            result.append(ci)
        return np.array(result)
    else:
        if n <= 500:
            get_ci = get_exact_ci_for_binomial_distribution
        else:
            get_ci = get_wilson_ci_for_binomial_distribution
        ci = get_ci(int(s), int(n), alpha)
        return ci


def get_ci_length_for_binomial(s, n, alpha):
    """
    :param Union[int, np.ndarray] s: Number of successes.
    :param Union[int, np.ndarray] n: Number of trials.
    :param float alpha: Confidence level.
    :return: Length or an np.ndarray of length of confidence intervals.
    :rtype: Union[int, np.ndarray]
    """

    ci = get_ci_for_binomial(s, n, alpha)
    if type(n) == list or type(n) == np.ndarray:
        result = []
        for x in ci:
            result.append(x[1] - x[0])
        return np.array(result)
    else:
        return ci[1] - ci[0]


def get_exact_ci_interval_size(s, n, alpha):
    interval = get_exact_ci_for_binomial_distribution(s, n, alpha)

    return interval[1] - interval[0]


@functools.lru_cache(100000)
def get_optimized_ci_length_for_binomial(s, n, alpha):

    global exact_ci_lengths_df

    if exact_ci_lengths_df is None:
        path = os.path.join("roomsage_data_science_tools", "probability_distributions", "exact_ci_lengths_df.p")
        with open(path, 'rb') as fp:
            exact_ci_lengths_df = pickle.load(fp)

    if n <= 500:
        cil = exact_ci_lengths_df.loc[int(s), int(n)]
    else:
        ci = get_wilson_ci_for_binomial_distribution(int(s), int(n), alpha)
        cil = ci[1] - ci[0]
    return cil


if __name__ == "__main__":

    # alpha = 0.05
    #
    # print(standard_z_score(alpha))
    #
    # # examples = [(0, 0)]
    # # examples = [(0, 3), (1, 3), (2, 3), (3, 3)]
    # # examples = [(0, 10), (1, 10), (5, 10), (9, 10), (10, 10)]
    # # examples = [(0, 100), (1, 100), (25, 100), (50, 100), (75, 100), (99, 100), (100, 100)]
    # examples = [(0, 500), (1, 500), (125, 500), (250, 500), (375, 500), (499, 500), (500, 500)]
    # # examples = [(0, 1000), (1, 1000), (250, 1000), (500, 1000), (750, 1000), (999, 1000), (1000, 1000)]
    #
    # for idx in range(len(examples)):
    #     s = examples[idx][0]
    #     n = examples[idx][1]
    #     print("s={} n={}".format(s, n))
    #     print("Exact: {}".format(get_exact_ci_for_binomial_distribution(s, n, alpha)))
    #     print("Normal: {}".format(get_normal_ci_for_binomial_distribution(s, n, alpha)))
    #     print("Wilson: {}".format(get_wilson_ci_for_binomial_distribution(s, n, alpha)))
    #     print("Naive: {}".format(get_naive_ci_for_binomial_distribution(s, n, alpha)))
    #     print("")

    print(get_ci_length_for_binomial(2, 100, 0.01))

    confidence_level = 0.05

    weight_adjustments = 1.0 / np.maximum(100 * get_ci_length_for_binomial([2, 5, 1],
                                                                           [100, 180, 150],
                                                                           confidence_level),
                                          0.1) - 0.01

    print(weight_adjustments)
    print(get_ci_length_for_binomial([2, 5, 1], [100, 180, 150], confidence_level))
