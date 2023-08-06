# Fix paths for imports to work in unit tests ----------------

if __name__ == "__main__":
    
    from _fix_paths import fix_paths
    fix_paths()

# ------------------------------------------------------------

# Load libraries ---------------------------------------------

import pandas as pd

# ------------------------------------------------------------


def get_df_first_row(df):
    """
    Returns the first Data Frame row as a dictionary.

    :param pd.DataFrame df: Data Frame.
    :return: The first row as a dictionary.
    :rtype: dict
    """

    result = None

    if len(df) > 0:
        result = {}

        for column in df.columns:
            result[column] = df[column][0]

    return result
