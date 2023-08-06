# Fix paths for imports to work in unit tests ----------------

if __name__ == "__main__":
    from _fix_paths import fix_paths

    fix_paths()

# ------------------------------------------------------------

# Load libraries ---------------------------------------------

from typing import Iterable
import numpy as np

from roomsage_data_science_tools.statistical_tools import calculate_progressive_effective_moe

# ------------------------------------------------------------


def remove_outliers(s, method='box_and_whiskers'):

    if method == 'box_and_whiskers':
        q1, q3 = np.percentile(s, [25, 75])
        iqr = q3 - q1

        lower_map = s < q1 - 1.5*iqr
        upper_map = s > q3 + 1.5*iqr

        outliers = lower_map | upper_map
        return s[~outliers]


def spot_deviation(s, moe=0.03, abs_moe_l_bound=0.001, p_cond=0.005, p_cond_moe=0.5, moe_form='absolute', n_deviations=2):
    """
    Given a time series s (from oldest to newest) returns the index of the first
    value after a significant change in the series.

    :param Iterable s: Input time series.
    :param float moe: Margin of error. By default in absolute form as defined in Wikipedia.
        Can also be used in a relative form, e.g. relative moe=0.1 means that
        the real margin of error is equal to forecast * moe.
    :param float abs_moe_l_bound: lower bound of relative error (used if moe_form is rel_abs or progressive)
    :param float p_cond: The value for which progressive effective moe is equal to 2*moe*p_cond (if moe_form is
        progressive_d_moe) or p_cond_moe*p_cond (if moe_form is progressive_multi_p)
    :param float p_cond_moe: Used if moe_form is progressive_multi_p
    :param str moe_form: Either absolute (default) or relative.
    :param int n_deviations: Number of consecutive deviations required .
    :rtype: int
    :return: Index of the first element after a significant change in the time series.
    """

    s_shifts = []
    for n in range(n_deviations + 1):
        s_shifts.append(np.roll(s, -n)[:-n_deviations])

    diffs = np.array([[0.0]*(len(list(s)) - n_deviations)]*n_deviations)

    for n in range(n_deviations):
        if moe_form in ['absolute', 'progressive_d_moe', 'progressive_multi_p']:
            diffs[n] = np.abs(s_shifts[n] - s_shifts[n_deviations])
        elif moe_form == 'relative':
            diffs[n] = np.abs(s_shifts[n] - s_shifts[n_deviations]) / s_shifts[n_deviations]

    if moe_form in ['progressive_d_moe', 'progressive_multi_p']:
        e_moe = []
        for i, p in enumerate(s_shifts[n_deviations]):
            e_moe.append(calculate_progressive_effective_moe(p, moe, moe_form, abs_moe_l_bound, p_cond, p_cond_moe))
        moe = np.array(e_moe)

    m = diffs[0] > moe
    for n in range(n_deviations - 1):
        m &= diffs[n + 1] > moe

    cut_index = np.where(m)[0]

    if len(cut_index) > 0:
        cut_index = cut_index[-1] + n_deviations
    else:
        cut_index = 0

    return cut_index


if __name__ == "__main__":

    def test_spot_deviation():
        s = np.array([10, 7, 5, 6, 7, 1, 0.5, 0.7, 0.3])

        cut_index = spot_deviation(s, moe=1)
        print("Cut index={}".format(cut_index))
        print("First element={}".format(s[cut_index]))

    test_spot_deviation()
