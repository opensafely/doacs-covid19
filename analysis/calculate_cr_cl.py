import pandas as pd
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
        df.loc[(df["atrial_fib"] == 1) & (df["crcl_2"] <15), 'apixaban'] = 'nr'

        df.loc[(df["atrial_fib"] == 1) & (df["crcl_1"] >=15) & (df["crcl_2"] <=29), 'apixaban'] = 'A2.5'

        df.loc[(df["atrial_fib"] == 1) & (df["crcl_2"] >=30) & (df["age"] >=80) & (df["weight"] >60) & (df["serum_creatinine"] <133), 'apixaban'] = 'A5'
        df.loc[(df["atrial_fib"] == 1) & (df["crcl_2"] >=30) & (df["weight"] <=60) & (df["age"] <80) & (df["serum_creatinine"] <133), 'apixaban'] = 'A5'
        df.loc[(df["atrial_fib"] == 1) & (df["crcl_2"] >=30) & (df["serum_creatinine"] >=133) & (df["weight"] >60) & (df["age"] <80), 'apixaban'] = 'A5'

        df.loc[(df["atrial_fib"] == 1) & (df["crcl_2"] >=30) & (df["age"] >=80) & (df["weight"] <=60) & (df["serum_creatinine"] <133), 'apixaban'] = 'A2.5'
        df.loc[(df["atrial_fib"] == 1) & (df["crcl_2"] >=30) & (df["weight"] <=60) & (df["age"] <80) & (df["serum_creatinine"] >=133), 'apixaban'] = 'A2.5'
        df.loc[(df["atrial_fib"] == 1) & (df["crcl_2"] >=30) & (df["serum_creatinine"] >=133) & (df["weight"] <=60) & (df["age"] <80), 'apixaban'] = 'A2.5'

        #rivaroxaban
        df.loc[(df["atrial_fib"] == 1) & df["crcl_2"] <15, 'rivaroxaban'] = 'nr'

        df.loc[(df["atrial_fib"] == 1) & (df["crcl_1"] >=15) & (df["crcl_2"] <=49), 'rivaroxaban'] = 'R15'

        df.loc[(df["atrial_fib"] == 1) & (df["crcl_2"] >50), 'rivaroxaban'] = 'R20'

        #edoxaban
        df.loc[(df["atrial_fib"] == 1) & df["crcl_2"] <15, 'edoxaban'] = 'nr'

        df.loc[(df["atrial_fib"] == 1) & (df["crcl_1"] >=15) & (df["crcl_2"] <=50), 'edoxaban'] = 'E30'
        df.loc[(df["atrial_fib"] == 1) & (df["crcl_2"] >50) & (df["weight"] <=60), 'edoxaban'] = 'E30' ### + IS on certain p-gp inhibitors ciclosporin, dronedarone, erthromycin, ketoconazole

        df.loc[(df["atrial_fib"] == 1) & (df["crcl_2"] >50) & (df["weight"] >60), 'edoxaban'] = 'E60' ### + NOT on certain p-gp inhibitors ciclosporin, dronedarone, erthromycin, ketoconazole

        #dabigatran
        df.loc[(df["atrial_fib"] == 1) & df["crcl_2"] <30, 'dabigatran1'] = 'nr'
        df.loc[(df["atrial_fib"] == 1) & df["crcl_2"] <30, 'dabigatran2'] = 'nr'

        df.loc[(df["atrial_fib"] == 1) & (df["crcl_1"] >=30) & (df["crcl_2"] <=50) & (df["age"] <75), 'dabigatran1'] = 'D110' ### + NOT taking verapamil, no gastritus, esophagitus, gastroesophageal refulx or increased risk of bleeding
        df.loc[(df["atrial_fib"] == 1) & (df["crcl_1"] >=30) & (df["crcl_2"] <=50) & (df["age"] <75), 'dabigatran2'] = 'D150' ### + NOT taking verapamil, no gastritus, esophagitus, gastroesophageal refulx or increased risk of bleeding

        df.loc[(df["atrial_fib"] == 1) & (df["crcl_2"] >=30) & (df["age"] >=80), 'dabigatran1'] = 'D110' ### + IS taking verapamil

        df.loc[(df["atrial_fib"] == 1) & (df["crcl_2"] >=30) & (df["age"] >=75) & (df["age"] <=80), 'dabigatran1'] = 'D110' ### + HAS gastritus, esophagitus, gastroesophageal refulx or increased risk of bleeding
        df.loc[(df["atrial_fib"] == 1) & (df["crcl_2"] >=30) & (df["age"] >=75) & (df["age"] <=80), 'dabigatran2'] = 'D150' ### + HAS gastritus, esophagitus, gastroesophageal refulx or increased risk of bleeding

        

        
        
        df.to_csv(f'output/df_with_calculation_{date}.csv') # this will be a new file
        #df.to_csv(os.path.join(OUTPUT_DIR, file)) # this will overwrite




        
