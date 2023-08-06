# Fix paths for imports to work in unit tests ----------------

if __name__ == "__main__":
    from _fix_paths import fix_paths

    fix_paths()

# ------------------------------------------------------------

# Load libraries ---------------------------------------------

import pandas as pd
import numpy as np

from roomsage_data_science_tools.probability_distributions.binomial_confidence_interval import get_optimized_ci_length_for_binomial
from roomsage_data_science_tools.statistical_tools import calculate_progressive_effective_moe

# ------------------------------------------------------------


def determine_time_scale_binomial(data, cl=0.05, moe=0.1, abs_moe_l_bound=0.001, p_cond=0.005, p_cond_moe=0.5, min_s=10,
                                  moe_form="absolute", max_window_size=None, possible_values=[]):
    """
    Returns a window size of a time series so that the values in a resampled
    (as in pandas.Series.resample) times series would have a maximal random noise
    of moe with confidence level cl.

    :param Union[pd.DataFrame, np.ndarray] data: Input values with two columns (successes, trials).
        Most recent records at the bottom.
    :param float cl: Confidence level.
    :param float moe: Margin of error. By default in absolute form as defined in Wikipedia.
        Can also be used in a relative form, e.g. relative moe=0.1 means that
        the real margin of error is equal to forecast * moe.
    :param float abs_moe_l_bound: lower bound of relative error (used if moe_form is rel_abs or progressive)
    :param int min_s: minimal number of successes (used if moe_form is rel_min_s)
    :param float p_cond: The value for which progressive effective moe is equal to 2*moe*p_cond (if moe_form is
        progressive_d_moe) or p_cond_moe*p_cond (if moe_form is progressive_multi_p)
    :param float p_cond_moe: Used if moe_form is progressive_multi_p
    :param str moe_form: absolute (default), relative, rel_abs, rel_min_s, progressive_d_moe or progressive_multi_p.
    :param int max_window_size: Maximal allowed window size even if the margin of error is not attained in this window.
    :param list possible_values: list of possible time scales, if empty list every time scale value from 0 to max_window_size is possible
    :rtype: int
    :return: Window size of a time series so that the values in a resampled
        (as in pandas.Series.resample) times series would have a maximal random noise
        of moe with confidence level cl.
    """

    def check_conditions(x):

        f = lambda x: get_optimized_ci_length_for_binomial(data[x, 0], data[x, 1], cl)  # get length of confidence interval for given time-step
        p = lambda x: data[x, 0] / data[x, 1] if data[x, 1] != 0 else 0  # get probability of success for given time-step
        t = lambda x: data[x, 1]  # get number of trials for given time-step

        if moe_form == "absolute":
            cond = f(x) < 2 * moe
        elif moe_form == 'relative':
            cond = f(x) < 2 * moe * p(x)
        elif moe_form == 'rel_abs':
            cond = f(x) < 2 * np.maximum(moe * p(x), abs_moe_l_bound)
        elif moe_form == 'rel_min_s':
            cond = f(x) < 2 * np.maximum(moe * p(x), min_s / t(x))
        elif moe_form in ['progressive_d_moe', 'progressive_multi_p']:
            cond = f(x) < 2 * calculate_progressive_effective_moe(p(x), moe, moe_form, abs_moe_l_bound, p_cond, p_cond_moe)
        else:
            raise Exception("Unhandled moe_form")

        return cond

    if isinstance(data, pd.DataFrame) or isinstance(data, pd.Series):
        data = data.values
    elif isinstance(data, list):
        data = np.array(data)

    if not max_window_size:
        max_window_size = data.shape[0]

    max_window_size = np.minimum(max_window_size, data.shape[0])
    data = np.cumsum(data[::-1][:max_window_size], axis=0)

    if not possible_values:
        a = 0
        b = max_window_size-1
        possible_values = list(range(a, max_window_size))
    else:
        a = 0
        b = len(possible_values) - 1
        possible_values = [x-1 for x in possible_values]

    if check_conditions(possible_values[a]):
        return possible_values[a] + 1
    if not check_conditions(possible_values[b]):
        return possible_values[b] + 1

    while True:
        ix = int((a+b)/2)
        if b == (a+1):
            return possible_values[b] + 1

        if check_conditions(possible_values[ix]):
            b = ix
        else:
            a = ix


if __name__ == "__main__":

    def test_determine_time_scale_binomial():
        size = 30
        p = 0.5
        p = np.array([p]*size)
        trials = np.random.randint(0, 51, size)
        successes = np.random.binomial(trials, p)
        data = np.array(list(zip(successes, trials)))

        print(data)

        moe_form = "absolute"
        cl = 0.05
        moe = 0.03
        window_size = determine_time_scale_binomial(data, cl, moe, moe_form=moe_form)

        print("Absolute moe window size={}".format(window_size))

        moe_form = "relative"
        moe = 0.1
        window_size = determine_time_scale_binomial(data, cl, moe, moe_form=moe_form)

        print("Relative moe window size={}".format(window_size))

        moe_form = "rel_abs"
        moe = 0.1
        window_size = determine_time_scale_binomial(data, cl, moe, moe_form=moe_form)

        print("Rel-abs moe window size={}".format(window_size))

        moe_form = "rel_min_s"
        moe = 0.1
        window_size = determine_time_scale_binomial(data, cl, moe, moe_form=moe_form)

        print("Relative with minimum successes moe window size={}".format(window_size))

        moe_form = "progressive_d_moe"
        moe = 0.1
        window_size = determine_time_scale_binomial(data, cl, moe, moe_form=moe_form)

        print("Progressive d moe window size={}".format(window_size))

        moe_form = "progressive_multi_p"
        moe = 0.1
        window_size = determine_time_scale_binomial(data, cl, moe, moe_form=moe_form)

        print("Progressive multi p moe window size={}".format(window_size))

        try:
            determine_time_scale_binomial(data, cl, moe, moe_form="fake_moe_form")
        except Exception as e:
            print(e)


    test_determine_time_scale_binomial()
