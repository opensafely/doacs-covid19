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
    
    # Medications
    doacs=patients.with_these_medications(
        doac_codes, 
        on_or_before=end_date,
        returning="date",
        find_first_match_in_period=True,
        date_format="YYYY-MM",
        return_expectations={"date": {"latest": "2020-03-01"}},
    ),

     # Clinical events
    creatinine=patients.with_these_clinical_events(
        creatinine_codes,
        find_last_match_in_period=True,
        between=["2020-12-01", "2021-11-01"],
        returning="numeric_value",
        include_date_of_match=True,
        include_month=True,
        return_expectations={
            "float": {"distribution": "normal", "mean": 60.0, "stddev": 15},
            "date": {"earliest": "2020-12-01", "latest": "2021-11-01"},
            "incidence": 0.95,},
    ),

    # BMI recorded
    bmi=patients.most_recent_bmi(
    between=["2019-12-01", "2021-10-31"],
    minimum_age_at_measurement=18,
    include_measurement_date=True,
    date_format="YYYY-MM",
    return_expectations={
        "date": {"earliest": "2019-12-01", "latest": "2021-10-31"},
        "float": {"distribution": "normal", "mean": 28, "stddev": 8},
        "incidence": 0.80,}
    ),

    # Demographic information
    age=patients.age_as_of(
        end_date, 
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"}},
    ),
    sex=patients.sex(
        return_expectations={
            "category": {"ratios": {"M": 0.49, "F": 0.51}},
            "incidence": 1},
    ),
)
