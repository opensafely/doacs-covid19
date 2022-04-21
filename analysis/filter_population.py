import re
import pandas as pd
from pathlib import Path

def match_input_files(file: str) -> bool:
    """Checks if file name has format outputted by cohort extractor"""
    pattern = r"^input_20\d\d-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])\.feather"
    return True if re.match(pattern, file) else False


filter_dir = Path("output/filtered")
if not Path(filter_dir).exists():
    Path.mkdir(filter_dir)


for file in Path("output").iterdir():
    if match_input_files(file.name):
        df = pd.read_feather(f"output/{file.name}")

        # filter out missing age band and non M/F sex
        df_subset = df.loc[((df["sex"].isin(["M", "F"])) & (df["age_band"] != "missing")),:].reset_index()
        
        df_subset.to_feather(f"output/filtered/{file.name}")