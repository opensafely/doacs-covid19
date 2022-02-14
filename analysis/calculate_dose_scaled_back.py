import pandas as pd
import numpy as np
import os
import re
import json
from collections import Counter

def match_input_files(file: str) -> bool:
    """Checks if file name has format outputted by cohort extractor"""
    pattern = r"^input_20\d\d-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])\.csv"
    return True if re.match(pattern, file) else False


def get_date_input_file(file: str) -> str:
    """Gets the date in format YYYY-MM-DD from input file name string"""
    # check format
    if not match_input_files(file):
        raise Exception("Not valid input file format")

    else:
        date = result = re.search(r"input_(.*)\.csv", file)
        return date.group(1)

def round_5(x):
    return int(5 * round(float(x)/5))

OUTPUT_DIR = "output"

for file in os.listdir(OUTPUT_DIR):
    if match_input_files(file):
        df = pd.read_feather(os.path.join(OUTPUT_DIR, file))

        date = get_date_input_file(file)
        # e.g date='2020-01-01'
        if date == "2020-01-01":

            unique_doac_dose = Counter(df["doac_dose_calculated"])
            with open("output/doac_dose_calculated.json", "w") as fp:
                json.dump(unique_doac_dose, fp)

            # calculate recommended dose for each doac based on recorded crcl

            # deal with null values in numeric value vars
            df["crcl"] = df["crcl"].fillna(-1)

            
            
            unique_crcl = Counter(df["crcl"].apply(lambda x: round_5(x)))
            with open("output/crcl.json", "w") as fp:
                json.dump(unique_crcl, fp)


            # apixaban
            apixaban_conditions = [
                ((df["atrial_fib"] == 1) & (df["crcl"] < 15) & (df["crcl"] >= 0)),
                ((df["atrial_fib"] == 1) & (df["crcl"] >= 15) & (df["crcl"] <= 29)),
                ((df["atrial_fib"] == 1) & (df["crcl"] >= 30)),
            ]

            apixaban_values = ["nr", "A2.5", "A5"]

            df["apixaban"] = np.select(apixaban_conditions, apixaban_values)

            # rivaroxaban
            rivaroxaban_conditions = [
                ((df["atrial_fib"] == 1) & (df["crcl"] < 15) & (df["crcl"] >= 0)),
                ((df["atrial_fib"] == 1) & (df["crcl"] >= 15) & (df["crcl"] <= 49)),
                ((df["atrial_fib"] == 1) & (df["crcl"] > 50)),
            ]

            rivaroxaban_values = ["nr", "R15", "R20"]

            df["rivaroxaban"] = np.select(rivaroxaban_conditions, rivaroxaban_values)

            # edoxaban
            edoxaban_conditions = [
                ((df["atrial_fib"] == 1) & (df["crcl"] < 15) & (df["crcl"] >= 0)),
                ((df["atrial_fib"] == 1) & (df["crcl"] >= 15) & (df["crcl"] <= 50)),
                ((df["atrial_fib"] == 1) & (df["crcl"] > 50)),
            ]

            edoxaban_values = ["nr", "E30", "E60"]

            df["edoxaban"] = np.select(edoxaban_conditions, edoxaban_values)

            # dabigatran
            dabigatran_conditions = [
                ((df["atrial_fib"] == 1) & (df["crcl"] < 30) & (df["crcl"] >= 0)),
                ((df["atrial_fib"] == 1) & (df["crcl"] >= 30) & (df["crcl"] <= 50)),
                ((df["atrial_fib"] == 1) & (df["crcl"] >= 30)),
            ]

            dabigatran_values = ["nr", "D110", "D150"]

            df["dabigatran"] = np.select(dabigatran_conditions, dabigatran_values)
        
            # now need to check if on correct dose!
            conditions = [
                (df["doac_dose_calculated"] == df["apixaban"]),
                (df["doac_dose_calculated"] == df["rivaroxaban"]),
                (df["doac_dose_calculated"] == df["edoxaban"]),
                (df["doac_dose_calculated"] == df["dabigatran"]),
            ]

            values = ["1", "1", "1", "1"]

            df["dose_match"] = np.select(conditions, values)

            # with af & crcl recorded & exclusions
            afcrcl_conditions = [
                ((df["atrial_fib"] == 1) & (df["crcl_recorded"] == 1)),
                ((df["atrial_fib"] == 0)),
                ((df["crcl_recorded"] == 0)),
                (df["crcl_exclude"] == 0),
            ]

            afcrcl_values = ["1", "0", "0", "0"]

            df["af_&_crcl"] = np.select(afcrcl_conditions, afcrcl_values)

            # df.to_csv(f'output/df_with_calculation_{date}.csv') # this will be a new file
            df.to_feather(os.path.join(OUTPUT_DIR, file))  # this will overwrite
