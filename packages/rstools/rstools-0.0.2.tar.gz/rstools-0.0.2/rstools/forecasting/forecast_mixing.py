# Fix paths for imports to work in unit tests ----------------

if __name__ == "__main__":

    from _fix_paths import fix_paths
    fix_paths()

# ------------------------------------------------------------

# Load libraries ---------------------------------------------

import numpy as np
import pandas as pd

from roomsage_data_science_tools.probability_distributions.beta import get_beta_dist_mean, get_beta_dist_variance
# ------------------------------------------------------------


def calculate_weights_for_mixing_periods(var_x, var_y, b):

    """
    Calculate weights for mixing two periods, where second period has higher bias and lower variance than the first one

    :param float var_x: Variance of the first period
    :param float var_y: Variance of the second period
    :param float b:
    :return:
    """

    lambda_0 = (var_y + np.sqrt(var_x * (b - var_y) + b * var_y)) / (var_x + var_y)
    return np.minimum(1, lambda_0)


def get_forecast_for_beta_dist(data, superior_level_data, mix_var_multiplier=4, min_forecast_accuracy=0.2):

    """
    :param Union[pd.DataFrame, np.ndarray, pd.Series] data: Dataframe with input values (successes, trials)
    :param Union[pd.DataFrame, np.ndarray, pd.Series] superior_level_data: Dataframe with successes  and trials for superior level
    :param mix_var_multiplier:
    :param min_forecast_accuracy:
    :return:
    """

    if isinstance(data, pd.DataFrame) or isinstance(data, pd.Series):
        data = data.values
    elif isinstance(data, list):
        data = np.array(data)

    if isinstance(superior_level_data, pd.DataFrame) or isinstance(superior_level_data, pd.Series):
        superior_level_data = superior_level_data.values
    elif isinstance(superior_level_data, list):
        superior_level_data = np.array(superior_level_data)

    x = data[-1, :]
    u_x = get_beta_dist_mean(x[0], x[1])
    var_x = get_beta_dist_variance(x[0], x[1])

    for i in range(1, data.shape[0] + 1):

        y = data[-i:].sum(axis=0)

        u_y = get_beta_dist_mean(y[0], y[1])
        var_y = get_beta_dist_variance(y[0], y[1])

        b = np.maximum(mix_var_multiplier * var_y, (min_forecast_accuracy * u_x) ** 2)
        lambda_0 = calculate_weights_for_mixing_periods(var_x, var_y, b)

        if b == (min_forecast_accuracy * u_x) ** 2:
            return lambda_0 * u_x + (1 - lambda_0) * u_y

        u_x = lambda_0 * u_x + (1 - lambda_0) * u_y
        var_x = lambda_0**2 * var_x + (1-lambda_0)**2 * var_y

    u_y = get_beta_dist_mean(superior_level_data[0], superior_level_data[1])
    var_y = get_beta_dist_variance(superior_level_data[0], superior_level_data[1])

    b = np.maximum(mix_var_multiplier * var_y, (min_forecast_accuracy * u_x) ** 2)
    lambda_0 = calculate_weights_for_mixing_periods(var_x, var_y, b)

    return lambda_0 * u_x + (1 - lambda_0) * u_y
