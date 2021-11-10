# Import functions
from cohortextractor import (
    StudyDefinition,
    Measure,
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
    population=patients.satisfying(
        """
        registered = 1
        AND
        NOT has_died
        AND 
        age <= 120
        AND 
        age>=18
        """,
        registered=patients.registered_as_of(
            index_date,
        )
        ),
    ) 
    ### FILTERS TO ADD
    # age - 18-120
    # died
    # registered

    
    # Medications
    doacs=patients.with_these_medications(
        doac_codes, 
        on_or_before=end_date, # make this between index date and last_day_of_month(index_date)
        returning="date", # can change to binary_flag
        find_first_match_in_period=True,
        date_format="YYYY-MM", # this can disappear if not using date
        #return_expectations={"date": {"latest": "2020-03-01"}},
    ),

     # Clinical events
    creatinine=patients.with_these_clinical_events(
        creatinine_codes,
        find_last_match_in_period=True,
        between=["2020-12-01", "2021-11-01"], # similar date to doac
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
        between=["2019-12-01", "2021-10-31"], # this could use index date
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
    carer=patients.with_these_clinical_events(
        carer,
        between = [start_date, end_date],
        returning = "binary_flag",
        find_last_match_in_period = True,
        return_expectations = {
            "incidence": 0.2,}
    ),

    # Organisation
    region=patients.registered_practice_as_of(
        "2021-11-01",
        returning="nuts1_region_name",
        return_expectations={
            "rate": "universal",
            "category": {
            "ratios": {
                "EAST OF ENGLAND": 0.1,
                "LONDON": 0.1,
                "MIDLANDS": 0.1,
                "NORTH EAST AND YORKSHIRE": 0.2,
                "NORTH WEST": 0.2,
                "SOUTH EAST": 0.1,
                "SOUTH WEST": 0.2,
            },
        },
    },
)
)
