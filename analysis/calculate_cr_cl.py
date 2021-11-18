import pandas as pd
from utilities import OUTPUT_DIR, match_input_files

        
for file in OUTPUT_DIR.iterdir():
    if match_input_files(file.name):
        df = pd.read_csv(OUTPUT_DIR / file.name)

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