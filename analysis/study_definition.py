# Import functions
from typing import DefaultDict
from cohortextractor import StudyDefinition, Measure, codelist, codelist_from_csv, combine_codelists, filter_codes_by_category, patients
from codelists import *
from datetime import date

study = StudyDefinition(
    index_date = "2021-11-01",  # date.today().isoformat()

    # Default expectations
    default_expectations={
        "date": {"earliest": "1970-01-01", "latest": "index_date"},
        "rate": "uniform",
        "incidence": 0.2,
    },

    # Define study population
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
            "index_date",
        ),
        has_died=patients.died_from_any_cause(
            on_or_before="index_date",
            returning="binary_flag",
        ),
    ),

    # With these medications
    on_doac=patients.with_these_medications(
        doac_codes, 
        between=["index_date", "last_day_of_month(index_date)"],
        returning="binary_flag",
        find_last_match_in_period = True,
        return_expectations = {
            "incidence": 0.2,},
    ),
    doac=patients.with_these_medications(
        doac_chemical, 
        between=["index_date", "last_day_of_month(index_date)"],
        returning="code",
        return_expectations = {
            "rate": "universal",
            "category": {
            "ratios": {
                "Apixaban": 0.25,
                "Edoxaban": 0.25,
                "Dabigatran etexilate": 0.25,
                "Rivaroxaban": 0.25,
            },
            },
        },
    ),
    #doac_dose_calculated=patients.categorised_as(
        #{"0": "DEFAULT",
        #"10": "doac = 'Apixaban'",
        #"60": "doac = 'Edoxaban'",
        #"300": "doac = 'Dabigatran'",
        #"20": "doac = 'Rivaroxaban'",
        #},
        #return_expectations={
         #"category": {"ratios": {"0": 0.1, "10": 0.2, "60": 0.2, "300": 0.25, "20": 0.25}},
        #"incidence": 0.2,
        #},
    #),
    
    # With these clinical events
    egfr_recorded=patients.with_these_clinical_events(
        egfr_codes,
        find_last_match_in_period=True,
        between=["index_date - 12 months", "index_date"],
        returning="binary_flag",
        return_expectations = {
            "incidence": 0.2,},
    ),
    crcl_recorded=patients.with_these_clinical_events(
        crcl_codes,
        find_last_match_in_period=True,
        between=["index_date - 12 months", "index_date"],
        returning="binary_flag",
        return_expectations = {
        "incidence": 0.2,},
    ),
    weight_recorded=patients.with_these_clinical_events(
        weight_codes,
        find_last_match_in_period=True,
        between=["index_date - 12 months", "index_date"],
        returning="binary_flag",
        return_expectations = {
        "incidence": 0.2,},
    ),
    serum_creatinine=patients.with_these_clinical_events(
        crcl_codes,
        find_last_match_in_period=True,
        between=["index_date - 2 years", "index_date"],
        returning="numeric_value",
        include_date_of_match=True,
        include_month=True,
        return_expectations={
            "float": {"distribution": "normal", "mean": 60.0, "stddev": 15},
            "date": {"earliest": "2020-12-01", "latest": "2021-11-01"},
            "incidence": 0.95,},
    ),

    # BMI, weight and height
    bmi=patients.most_recent_bmi(
        between=["index_date - 2 years", "index_date"],
        minimum_age_at_measurement=18,
        include_measurement_date=True,
        date_format="YYYY-MM",
        return_expectations={
            "date": {"earliest": "2019-12-01", "latest": "2021-10-31"},
            "float": {"distribution": "normal", "mean": 28, "stddev": 8},
            "incidence": 0.80,}
    ),
    weight=patients.with_these_clinical_events(
        weight_codes,
        find_last_match_in_period=True,
        between=["index_date - 2 years", "index_date"],
        returning="numeric_value",
        include_date_of_match=True,
        include_month=True,
        return_expectations={
            "float": {"distribution": "normal", "mean": 60.0, "stddev": 15},
            "date": {"earliest": "2020-12-01", "latest": "2021-11-01"},
            "incidence": 0.95,},
    ),
    height=patients.with_these_clinical_events(
        height_codes,
        find_last_match_in_period=True,
        between=["index_date - 2 years", "index_date"],
        returning="numeric_value",
        include_date_of_match=True,
        include_month=True,
        return_expectations={
            "float": {"distribution": "normal", "mean": 60.0, "stddev": 15},
            "date": {"earliest": "2020-12-01", "latest": "2021-11-01"},
            "incidence": 0.95,},
    ),
    weight_for_crcl=patients.categorised_as(
        {"missing": "DEFAULT",
        "actual": """bmi <18.5""",
        "ideal": """bmi >=18.5 AND bmi <25""",
        "adjusted": """bmi >=25""",
        },
        return_expectations={
         "category": {"ratios": {"missing": 0.1, "actual": 0.3, "ideal": 0.3, "adjusted": 0.3}},
        "incidence": 0.8,
        },
    ),

    # Demographic information
    age=patients.age_as_of(
        "index_date",
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
    ),
    age_band=patients.categorised_as(
        {
            "missing": "DEFAULT",
            "<20": """ age >= 0 AND age < 20""",
            "20-29": """ age >=  20 AND age < 30""",
            "30-39": """ age >=  30 AND age < 40""",
            "40-49": """ age >=  40 AND age < 50""",
            "50-59": """ age >=  50 AND age < 60""",
            "60-69": """ age >=  60 AND age < 70""",
            "70-79": """ age >=  70 AND age < 80""",
            "80-89": """ age >=  80 AND age < 90""",
            ">90": """ age >=  90 AND age < 120""",
        },
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "missing": 0.005,
                    "<20": 0.12,
                    "20-29": 0.125,
                    "30-39": 0.125,
                    "40-49": 0.125,
                    "50-59": 0.125,
                    "60-69": 0.125,
                    "70-79": 0.125,
                    ">90": 0.125,
                }
            },
        },
    ),
    sex=patients.sex(
        return_expectations={
            "category": {"ratios": {"M": 0.49, "F": 0.51}},
            "incidence": 1},
    ),
    carer=patients.with_these_clinical_events(
        carer,
        between=["index_date", "last_day_of_month(index_date)"],
        returning = "binary_flag",
        find_last_match_in_period = True,
        return_expectations = {
            "incidence": 0.2,}
    ),

    # Organisation
    region=patients.registered_practice_as_of(
        "index_date",
        returning="nuts1_region_name",
        return_expectations={
            "rate": "universal",
            "category": {
            "ratios": {
                "East of England": 0.1,
                "London": 0.1,
                "Midlands": 0.1,
                "North East and Yorkshire": 0.2,
                "North West": 0.2,
                "South East": 0.1,
                "South West": 0.2,
            },
            },
        },
    ),





)


measures = [
    
    Measure(
        id="doacs_by_region",
        numerator="on_doac",
        denominator="population",
        group_by=["region"],
    ),
    
    Measure(
        id="doacs_by_age_band",
        numerator="on_doac",
        denominator="population",
        group_by=["age_band"]
    ),

    Measure(
        id="doacs_by_sex",
        numerator="on_doac",
        denominator="population",
        group_by=["sex"]
    ),

    Measure(
        id="doacs_by_carer",
        numerator="on_doac",
        denominator="population",
        group_by=["carer"]
    ),

    Measure(
        id="doacs_by_ethnicity",
        numerator="on_doac",
        denominator="population",
        group_by=["ethnicity"]
    ),

    Measure(
        id="doacs_with_weight_recorded",
        numerator="on_doac",
        denominator="population",
        group_by=["weight_recorded"]
    ),

    Measure(
        id="doacs_with_egfr_recorded",
        numerator="on_doac",
        denominator="population",
        group_by=["egfr_recorded"]
    ),

    Measure(
        id="doacs_with_crcl_recorded",
        numerator="on_doac",
        denominator="population",
        group_by=["crcl_recorded"]
    ),
        
]

