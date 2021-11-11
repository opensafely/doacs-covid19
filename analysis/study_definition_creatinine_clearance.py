# Import functions
from cohortextractor import (
    StudyDefinition,
    codelist,
    codelist_from_csv,
    combine_codelists,
    filter_codes_by_category,
    patients,
)

# Import codelist
from codelists import *

start_date = "2016-03-01"
end_date = "2021-11-01"

study = StudyDefinition(

    # Default dummy data behaviour
    index_date = end_date,
    default_expectations={
        "date": {"earliest": start_date, "latest": end_date},
        "rate": "uniform",
        "incidence": 0.5,
    },
    
    # Define the study population
    population = patients.all(),
    
    # BMI, weight and height
    bmi=patients.most_recent_bmi(
        between=["index_date - 2 years", "index_date"],
        minimum_age_at_measurement=18,
        return_expectations={
            "float": {"distribution": "normal", "mean": 28, "stddev": 8},
            "incidence": 0.80,}
    ),
    bmi_band=patients.categorised_as(
        {
            "missing": "DEFAULT",
            "Underweight": """ bmi >= 0 AND bmi < 18.5""",
            "Normal weight": """ bmi >=  18.5 AND bmi < 24.9""",
            "Overweight / obese": """ bmi >=  25""",
        },
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "missing": 0.1,
                    "Underwight": 0.2,
                    "Normal weight": 0.5,
                    "Overweight / obese": 0.2,
                }
            },
        },
    ),
)