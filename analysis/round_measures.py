import pandas as pd
import numpy as np
from pathlib import Path

from study_definition import measures

# https://github.com/opensafely/strepa_scarlet/blob/233a96cc2ae3dd4963867ec1cc967bc7aa83f783/analysis/report/report_utils.py#L83
def round_values(x, base=10, redact=False, redaction_threshold=5):
    """
    Rounds values to nearest multiple of base.  If redact is True, values less than or equal to
    redaction_threshold are converted to np.nan.
    Args:
        x: Value to round
        base: Base to round to
        redact: Boolean indicating if values less than redaction_threshold should be
        redacted
        redaction_threshold: Threshold for redaction
        Returns:
            Rounded value
    """

    if isinstance(x, (int, float)):
        if np.isnan(x):
            rounded = np.nan

        else:
            if redact and x <= redaction_threshold:
                rounded = np.nan

            else:
                rounded = int(base * round(x / base))
    return rounded

# https://github.com/opensafely/strepa_scarlet/blob/233a96cc2ae3dd4963867ec1cc967bc7aa83f783/analysis/join_and_round.py#L92
def round_table(measure_table, numerator_col, denominator_col, value_col):
    measure_table[numerator_col] = measure_table[numerator_col].astype(float)
    measure_table[denominator_col] = measure_table[denominator_col].astype(float)

    measure_table[numerator_col] = measure_table[numerator_col].apply(
        lambda x: round_values(x, base=5)
    )
    measure_table[denominator_col] = measure_table[denominator_col].apply(
        lambda x: round_values(x, base=5)
    )
    # recompute value
    measure_table[value_col] = measure_table[numerator_col] / measure_table[denominator_col]
    return measure_table

if __name__ == "__main__":

    measures_dir = "output/filtered"

    for m in measures:
        measure_file = Path(measures_dir) / f"measure_{m.id}.csv"
      
        measure_table = pd.read_csv(measure_file)
        round_table(measure_table, m.numerator, m.denominator, "value")
        measure_table.to_csv(measure_file, index=False)
