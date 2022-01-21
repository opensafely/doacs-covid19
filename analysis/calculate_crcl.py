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


        #calculate all weight ranges, actual ABW, ideal IBW, adjusted ADJ
        df["ABW"] = df.weight
        df.loc[df["sex"] == 'M', 'IBW'] = 50 + (2.3 * (df.height - 60))
        df.loc[df["sex"] == 'F', 'IBW'] = 45.5 + (2.3 * (df.height - 60))
        df["ADJ"] = df.IBW + 0.4 * (df.ABW - df.IBW)

        #IF BMI NOT PRESENT, CALCULATE FROM WEIGHT/HEIGHT
        
        #weight for calculation
        df.loc[df["bmi"] <30, 'weight_crcl_1'] = df.ABW
        df.loc[df["bmi"] >=30,'weight_crcl_1'] = df.IBW
        df.loc[df["bmi"] ==0, 'weight_crcl_1'] = 0

        df.loc[df["bmi"] <30, 'weight_crcl_2'] = df.ABW
        df.loc[df["bmi"] >=30,'weight_crcl_2'] = df.ADJ
        df.loc[df["bmi"] ==0, 'weight_crcl_2'] = 0

        #crcl range
        df.loc[df["sex"] == 'M', 'crcl_1'] = (1.23 * (140-df.age) * df.weight_crcl_1) / df.serum_creatinine
        df.loc[df["sex"] == 'F', 'crcl_1'] = (1.04 * (140-df.age) * df.weight_crcl_1) / df.serum_creatinine

        df.loc[df["sex"] == 'M', 'crcl_2'] = (1.23 * (140-df.age) * df.weight_crcl_2) / df.serum_creatinine
        df.loc[df["sex"] == 'F', 'crcl_2'] = (1.04 * (140-df.age) * df.weight_crcl_2) / df.serum_creatinine

        #calculate recommended dose for each doac
        
        #apixaban
        apixaban_conditions = [
            ((df["atrial_fib"] == 1) & (df["crcl_2"] <15)),
        ((df["atrial_fib"] == 1) & (df["crcl_1"] >=15) & (df["crcl_2"] <=29)),
        ((df["atrial_fib"] == 1) & (df["crcl_2"] >=30) & (df["age"] >=80) & (df["weight"] >60) & (df["serum_creatinine"] <133)),
        ((df["atrial_fib"] == 1) & (df["crcl_2"] >=30) & (df["weight"] <=60) & (df["age"] <80) & (df["serum_creatinine"] <133)),
        ((df["atrial_fib"] == 1) & (df["crcl_2"] >=30) & (df["serum_creatinine"] >=133) & (df["weight"] >60) & (df["age"] <80)),
        ((df["atrial_fib"] == 1) & (df["crcl_2"] >=30) & (df["age"] >=80) & (df["weight"] <=60) & (df["serum_creatinine"] <133)),
        ((df["atrial_fib"] == 1) & (df["crcl_2"] >=30) & (df["weight"] <=60) & (df["age"] <80) & (df["serum_creatinine"] >=133)),
        ((df["atrial_fib"] == 1) & (df["crcl_2"] >=30) & (df["serum_creatinine"] >=133) & (df["weight"] <=60) & (df["age"] <80))
        ]
        
        apixaban_values = ['nr', 'A2.5', 'A5', 'A5', 'A5', 'A2.5', 'A2.5', 'A2.5']

        df['apixaban'] = np.select(apixaban_conditions, apixaban_values)

        #rivaroxaban
        rivaroxaban_conditions = [
            ((df["atrial_fib"] == 1) & (df["crcl_2"] <15)),
        ((df["atrial_fib"] == 1) & (df["crcl_2"] >=15) & (df["crcl_2"] <=49)),
        ((df["atrial_fib"] == 1) & (df["crcl_2"] >50))
        ]
        
        rivaroxaban_values = ['nr', 'R15', 'R20']

        df['rivaroxaban'] = np.select(rivaroxaban_conditions, rivaroxaban_values)

        #edoxaban
        edoxaban_conditions = [
            ((df["atrial_fib"] == 1) & (df["crcl_2"] <15)),
        ((df["atrial_fib"] == 1) & (df["crcl_1"] >=15) & (df["crcl_2"] <=50)),
        ((df["atrial_fib"] == 1) & (df["crcl_2"] >50) & (df["weight"] <=60) & (df["on_pgpi"] == 1)), ### + IS on certain p-gp inhibitors ciclosporin 80906007, dronedarone 443310000, erthromycin 30427009, ketoconazole 40232005
        ((df["atrial_fib"] == 1) & (df["crcl_2"] >50) & (df["weight"] >60) & (df["on_pgpi"] == 0)) ### + NOT on certain p-gp inhibitors ciclosporin 80906007, dronedarone 443310000, erthromycin 30427009, ketoconazole 40232005
        ]
        
        edoxaban_values = ['nr', 'E30', 'E30', 'E60']

        df['edoxaban'] = np.select(edoxaban_conditions, edoxaban_values)

        #dabigatran110
        dabigatran110_conditions = [
            ((df["atrial_fib"] == 1) & (df["crcl_2"] <30)),
            ((df["atrial_fib"] == 1) & (df["crcl_1"] >=30) & (df["crcl_2"] <=50) & (df["age"] <75) & (df["on_verapamil"] == 0) & (df["contra_indications"] == 0)), ### + NOT taking verapamil 47898004, NO gastritus, esophagitus, gastroesophageal refulx or increased risk of bleeding
            ((df["atrial_fib"] == 1) & (df["crcl_2"] >=30) & (df["age"] >=80) & (df["on_verapamil"] == '1')), ### + IS taking verapamil
            ((df["atrial_fib"] == 1) & (df["crcl_2"] >=30) & (df["age"] >=75) & (df["age"] <=80) & (df["contra_indications"] == 1)) ### + HAS gastritus, esophagitus, gastroesophageal refulx or increased risk of bleeding
        ]
        
        dabigatran110_values = ['nr', 'D110', 'D110', 'D110']

        df['dabigatran110'] = np.select(dabigatran110_conditions, dabigatran110_values)

        #dabigatran150
        dabigatran150_conditions = [
            ((df["atrial_fib"] == 1) & (df["crcl_2"] <30)),
            ((df["atrial_fib"] == 1) & (df["crcl_1"] >=30) & (df["crcl_2"] <=50) & (df["age"] <75) & (df["on_verapamil"] == 0) & (df["contra_indications"] == 0)), ### + NOT taking verapamil 47898004, NO gastritus, esophagitus, gastroesophageal refulx or increased risk of bleeding
            ((df["atrial_fib"] == 1) & (df["crcl_2"] >=30) & (df["age"] >=75) & (df["age"] <=80) & (df["contra_indications"] == 1)) ### + HAS gastritus, esophagitus, gastroesophageal refulx or increased risk of bleeding
        ]

        dabigatran150_values = ['nr', 'D150', 'D150']

        df['dabigatran150'] = np.select(dabigatran150_conditions, dabigatran150_values)
       
        #now need to check if on correct dose!
        conditions = [
            (df['doac_dose_calculated'] == df['apixaban']),
        (df['doac_dose_calculated'] == df['rivaroxaban']),
        (df['doac_dose_calculated'] == df['edoxaban']),
        (df['doac_dose_calculated'] == df['dabigatran110']),
        (df['doac_dose_calculated'] == df['dabigatran150'])
        ]

        values = ['1', '1', '1', '1', '1']

        df['dose_match'] = np.select(conditions, values)
        
        



        
        #df.to_csv(f'output/df_with_calculation_{date}.csv') # this will be a new file
        df.to_csv(os.path.join(OUTPUT_DIR, file)) # this will overwrite




        
