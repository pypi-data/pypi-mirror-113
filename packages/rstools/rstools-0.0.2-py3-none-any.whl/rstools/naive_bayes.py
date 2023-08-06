# Load libraries ---------------------------------------------

import numpy as np
from typing import Iterable
# ------------------------------------------------------------


def naive_bayes(p_x, p_a, p_x_a):
    """
    Calculate probability of an action (e.g. click, conversion) for a given combination of features.

    .. math::
        P(X|A,B) = P(A|X)P(B|X)P(X) / (P(A|X)P(B|X)P(X) + P(A|~X)P(B|~X)P(~X))

    :param float p_x: P(X) - probability of a given action (e.g. conversion or click)
    :param Iterable p_a: [P(A), P(B), ...] - list of probabilities of a certain features (e.g. P(A)=P(gender=male), P(B)=P(device=mobile))
    :param Iterable p_x_a: [P(X|A), P(X|B), ...] - list of conditional probabilities that a given action occurs for a given feature
                                               (e.g. P(X|A)=P(click | gender=male))
    :return: probability of combination of given features (e.g. P(A,B)=  P(gender=male, device=mobile) and
             probability of an action for a combination of given features (e.g. P(X|A,B) = P(click | gender=male, device=mobile)
    :rtype: float, float
    """

    p_not_x = 1 - p_x  # P(~X)
    p_not_x_a = [1 - p for p in p_x_a]  # [P(~X|A), P(~X|B, ...]

    if p_x == 0:
        p_a_not_x = reverse_conditional_probability(p_not_x, p_a, p_not_x_a)  # [P(A|~X), P(B|~X), ...]
        p_base = p_not_x * np.prod(p_a_not_x)  # P(A,B,...)
        p_base = np.maximum(0, p_base)
        return p_base, 0

    p_a_x = reverse_conditional_probability(p_x, p_a, p_x_a)  # [P(A|X), P(B|X, ...]
    p_a_not_x = reverse_conditional_probability(p_not_x, p_a, p_not_x_a)  # [P(A|~X), P(B|~X), ...]

    p_base = p_x * np.prod(p_a_x) + p_not_x * np.prod(p_a_not_x)  # P(A,B,...)
    p_base = np.maximum(0, p_base)

    if any(i == 0 for i in p_x_a):
        return p_base, 0

    p_joint = p_x * np.prod(p_a_x) / p_base  # P(X|A,B,...)
    p_joint = np.maximum(0, p_joint)

    return p_base, p_joint


def reverse_conditional_probability(p_x, p_a, p_x_a):
    """
    Change conditional probability from P(X|A) form into P(A|X) according to Bayes' theorem
    .. math::
        P(A|X) = P(X|A)P(A) / P(X)

    :param float p_x: P(X) - probability of a given action (e.g. conversion or click)
    :param [Iterable, List] p_a: [P(A), P(B), ...] - list of probabilities of a certain features (e.g. P(A)=P(gender=male), P(B)=P(device=mobile))
    :param [Iterable, List] p_x_a: [P(X|A), P(X|B), ...] - list of conditional probabilities that a given action occurs for a given feature
                                               (e.g. P(X|A)=P(click | gender=male))
    :return:
    """
    return [p_x_a[i] * p_a[i] / p_x for i in range(len(p_a))]


if __name__ == "__main__":

    import unittest

    class TestNaiveBayes(unittest.TestCase):

        def test_naive_bayes(self):

            p_x = 0.2
            p_a = [0.8, 0.2]
            p_x_a = [0.21, 0.05]

            p_a_x = [p_x_a[i]*p_a[i] / p_x for i in range(len(p_a))]

            p_not_x = 1 - p_x
            p_not_x_a = [1 - i for i in p_x_a]
            p_a_not_x = [p_not_x_a[i]*p_a[i] / p_not_x for i in range(len(p_a))]

            numerator = p_x * np.prod(p_a_x)
            denominator = (p_x * np.prod(p_a_x) + p_not_x * np.prod(p_a_not_x))

            y = numerator / denominator
            p_x_ab = naive_bayes(p_x=p_x, p_a=p_a, p_x_a=p_x_a)

            self.assertEqual(p_x_ab[0], denominator)
            self.assertEqual(p_x_ab[1], y)

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestNaiveBayes))
    unittest.TextTestRunner().run(suite)
