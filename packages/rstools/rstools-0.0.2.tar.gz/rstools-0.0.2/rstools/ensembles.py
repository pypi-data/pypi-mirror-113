# Fix paths for imports to work in unit tests ----------------

if __name__ == "__main__":
    from _fix_paths import fix_paths

    fix_paths()

# ------------------------------------------------------------

# Load libraries ---------------------------------------------

import numpy as np

from roomsage_data_science_tools.probability_distributions.beta import get_beta_dist_mean, get_beta_dist_variance
from roomsage_data_science_tools.statistical_tools import calculate_progressive_effective_moe

# ------------------------------------------------------------


def integrate_beta_biased_unbiased(su, sb, nu, nb, moe=0.1, moe_form='absolute', abs_moe_l_bound=0.001, p_cond=0.005, p_cond_moe=0.5):

    """
    :param su: successes from unbiased series
    :param sb: successes from biased series
    :param nu: trials from unbiased series
    :param nb: trials from biased series
    :param float moe: Margin of error. By default in absolute form as defined in Wikipedia.
        Can also be used in a relative form, e.g. relative moe=0.1 means that
        the real margin of error is equal to forecast * moe.
    :param str moe_form: absolute (default), relative, rel_abs, rel_min_s, progressive_d_moe or progressive_multi_p:
    :param float abs_moe_l_bound: lower bound of relative error (used if moe_form is rel_abs or progressive)
    :param float p_cond: The value for which progressive effective moe is equal to 2*moe*p_cond (if moe_form is
        progressive_d_moe) or p_cond_moe*p_cond (if moe_form is progressive_multi_p)
    :param float p_cond_moe: Used if moe_form is progressive_multi_p
    :return:
    """

    fu = get_beta_dist_mean(su, nu)
    fb = get_beta_dist_mean(sb, nb)

    lambda_0 = calculate_beta_biased_unbiased_weights(su, sb, nu, nb, moe, moe_form, abs_moe_l_bound, p_cond, p_cond_moe)
    return lambda_0 * fu + (1 - lambda_0) * fb


def calculate_beta_biased_unbiased_weights(su, sb, nu, nb, moe=0.1, moe_form='absolute', abs_moe_l_bound=0.001, p_cond=0.005, p_cond_moe=0.5):

    """
    :param su: successes from unbiased series
    :param sb: successes from biased series
    :param nu: trials from unbiased series
    :param nb: trials from biased series
    :param moe:
    :param moe_form:
    :param abs_moe_l_bound:
    :param p_cond:
    :param p_cond_moe:
    :return:
    """

    fu = get_beta_dist_mean(su, nu)
    var_u = get_beta_dist_variance(su, nu)
    var_b = get_beta_dist_variance(sb, nb)

    lambda_0 = get_beta_biased_unbiased_lambda(fu, var_u, var_b, moe, moe_form, abs_moe_l_bound, p_cond, p_cond_moe)
    return lambda_0


def get_beta_biased_unbiased_lambda(fu, var_u, var_b, moe, moe_form, abs_moe_l_bound, p_cond, p_cond_moe):

    if moe_form == 'absolute':
        b = (moe/2)**2
    elif moe_form == 'relative':
        b = (moe * fu / 2) ** 2
    elif moe_form in ['progressive_d_moe', 'progressive_multi_p']:
        b = (calculate_progressive_effective_moe(fu, moe=moe, moe_form=moe_form, abs_moe_l_bound=abs_moe_l_bound,
                                                 p_cond=p_cond, p_cond_moe=p_cond_moe)/2)**2
    else:
        raise Exception("Unhandled moe_form")

    if b <= 1 / (1/var_u + 1/var_b):
        lambda_0 = var_b / (var_u + var_b)
    else:
        lambda_0 = (var_b + np.sqrt(var_u * (b - var_b) + b * var_b)) / (var_u + var_b)

    return np.minimum(1, lambda_0)
