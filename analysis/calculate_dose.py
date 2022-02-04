import pandas as pd
import numpy as np
import os
import re


def match_input_files(file: str) -> bool:
    """Checks if file name has format outputted by cohort extractor"""
    pattern = r'^input_20\d\d-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])\.csv' 
    return True if re.match(pattern, file) else False

def get_date_input_file(file: str) -> str:
    """Gets the date in format YYYY-MM-DD from input file name string"""
    # check format
    if not match_input_files(file):
        raise Exception('Not valid input file format')

    else:
        date = result = re.search(r'input_(.*)\.csv', file)
        return date.group(1)

OUTPUT_DIR = "output"

for file in os.listdir(OUTPUT_DIR):
    if match_input_files(file):
        df = pd.read_csv(os.path.join(OUTPUT_DIR, file))

        date = get_date_input_file(file)
        # e.g date='2020-01-01'

        #calculate recommended dose for each doac based on recorded crcl
        
        #2.rivaroxaban
        rivaroxaban_conditions = [
            ((df["atrial_fib"] == 1) & (df["crcl"] <15)),
        ((df["atrial_fib"] == 1) & (df["crcl"] >=15) & (df["crcl"] <=49)),
        ((df["atrial_fib"] == 1) & (df["crcl"] >50))
        ]
        
        rivaroxaban_values = ['nr', 'R15', 'R20']

        df['rivaroxaban'] = np.select(rivaroxaban_conditions, rivaroxaban_values)

       



       
        #with af & crcl recorded & exclusions
        afcrcl_conditions = [
            ((df["atrial_fib"] == 1) & (df["crcl_recorded"] ==1)),
        ((df["atrial_fib"] == 0)),
        ((df["crcl_recorded"] == 0)),
        (df['crcl_exclude'] == 0),
        (df['serumcreatininecreatinine_exclude'] == 0),
        (df['weight_exclude'] == 0)
        ]

        afcrcl_values = ['1', '0', '0', '0', '0', '0']

        df['af_&_crcl'] = np.select(afcrcl_conditions, afcrcl_values)

        
        



        
        #df.to_csv(f'output/df_with_calculation_{date}.csv') # this will be a new file
        df.to_csv(os.path.join(OUTPUT_DIR, file)) # this will overwrite




        
