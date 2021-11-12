import re
import json
import os
from pathlib import Path
from typing import Match
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from collections import Counter
from datetime import timedelta as td

BASE_DIR = Path(__file__).parents[1]
OUTPUT_DIR = BASE_DIR / "output"

def validate_directory(dirpath):
    if not dirpath.is_dir():
        raise ValueError(f"Not a directory")

def join_ethnicity(directory: str) -> None:
    """Finds 'input_ethnicity.csv' in directory and combines with each input file."""
    
    dirpath = Path(directory)
    validate_directory(dirpath)
    filelist = dirpath.iterdir()

    #get ethnicity input file
    ethnicity_df = pd.read_csv(dirpath / 'input_ethnicity.csv')
    
    ethnicity_dict = dict(zip(ethnicity_df['patient_id'], ethnicity_df['ethnicity']))  

    for file in filelist:
        if Match(file.name):
            df = pd.read_feather(dirpath / file.name)
        
            df['ethnicity'] = df['patient_id'].map(ethnicity_dict)
            df.to_csv(dirpath / file.name)


            