# Fix paths for imports to work in unit tests ----------------

if __name__ == "__main__":
    from _fix_paths import fix_paths

    fix_paths()

# ------------------------------------------------------------

# Load libraries ---------------------------------------------

# ------------------------------------------------------------


def calculate_progressive_effective_moe(p, moe, moe_form, abs_moe_l_bound, p_cond, p_cond_moe):

    """
    :param float p: Probability of success
    :param float moe: Margin of error. By default in absolute form as defined in Wikipedia.
        Can also be used in a relative form, e.g. relative moe=0.1 means that
        the real margin of error is equal to forecast * moe.
    :param str moe_form: absolute (default), relative, rel_abs, rel_min_s, progressive_d_moe or progressive_multi_p
    :param float abs_moe_l_bound: lower bound of relative error (used if moe_form is rel_abs or progressive)
    :param float p_cond: The value for which progressive effective moe is equal to 2*moe*p_cond (if moe_form is
        progressive_d_moe) or p_cond_moe*p_cond (if moe_form is progressive_multi_p)
    :param float p_cond_moe: Used if moe_form is progressive_multi_p
    :return:
    """

    epsilon = 0.000001
    K = 1 - 2 * abs_moe_l_bound / moe

    if moe_form == 'progressive_d_moe':
        V = 1 / K * (2 - abs_moe_l_bound / (p_cond * moe))
    elif moe_form == 'progressive_multi_p':
        V = 1 / (K * moe) * (p_cond_moe - abs_moe_l_bound / p_cond)

    A = (V - 1) * (p_cond + epsilon) * (0.5 + epsilon) / (0.5 - p_cond)
    B = (0.5 + epsilon - V * (p_cond + epsilon)) / (0.5 - p_cond)
    C = A / (p + epsilon) + B

    e_moe = C * K * p * moe + abs_moe_l_bound
    return e_moe
