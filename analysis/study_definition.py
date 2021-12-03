# Import functions
from typing import DefaultDict
from cohortextractor import StudyDefinition, Measure, codelist, codelist_from_csv, combine_codelists, filter_codes_by_category, patients
from codelists import *
from datetime import date

study = StudyDefinition(
    index_date = "2021-11-01",

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
    ##
    doac=patients.with_these_medications(
        doac_codes, 
        between=["index_date", "last_day_of_month(index_date)"],
        returning="code",
        return_expectations = {
            "rate": "universal",
            "category": {
            "ratios": {
                "0208020Z0AAAAAA": 0.08,
                "0208020Z0AAABAB": 0.08,
                "0208020X0AAABAB": 0.08,
                "0208020X0AAACAC": 0.08,
                "0208020X0AAAAAA": 0.08,
                "0208020AAAAAAAA": 0.08,
                "0208020AAAAABAB": 0.08,
                "0208020AAAAACAC": 0.08,
                "0208020Y0AAAAAA": 0.08,
                "0208020Y0AAABAB": 0.08,
                "0208020Y0AAAEAE": 0.08,
                "0208020Y0AAADAD": 0.06,
                "0208020Y0AAACAC": 0.06,
            },
            },
        },
    ),
    doac_dose_calculated=patients.categorised_as(
        {"0": "DEFAULT",
        "A2.5": "doac = '0208020Z0AAAAAA'",
        "A5": "doac = '0208020Z0AAABAB'",
        "D110": "doac = '0208020X0AAABAB'",
        "D150": "doac = '0208020X0AAACAC'",
        "D75": "doac = '0208020X0AAAAAA'",
        "E15": "doac = '0208020AAAAAAAA'",
        "E30": "doac = '0208020AAAAABAB'",
        "E60": "doac = '0208020AAAAACAC'",
        "R10": "doac = '0208020Y0AAAAAA'",
        "R15": "doac = '0208020Y0AAABAB'",
        "R15/20 titration": "doac = '0208020Y0AAAEAE'",
        "R2.5": "doac = '0208020Y0AAADAD'",
        "R20": "doac = '0208020Y0AAACAC'",
        },
        return_expectations={
         "category": {"ratios": {"0": 0.02, "A2.5": 0.07, "A5": 0.07, "D110": 0.08, "D150": 0.08, "D75": 0.08, "E15": 0.08, "E30": 0.08, "E60": 0.08, "R10": 0.08, "R15": 0.08, "R15/20 titration": 0.08, "R2.5": 0.06, "R20": 0.06,}},
        "incidence": 0.2,
        },
    ),
        
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
    serumcreatinine_recorded=patients.with_these_clinical_events(
        creatinine_codes,
        find_last_match_in_period=True,
        between=["index_date - 12 months", "index_date"],
        returning="binary_flag",
        return_expectations = {
        "incidence": 0.2,},
    ),
    #serum_creatinine=patients.with_these_clinical_events(
        #creatinine_codes,
        #find_last_match_in_period=True,
        #between=["index_date - 12 months", "index_date"],
        #returning="numeric_value",
        #include_date_of_match=True,
        #include_month=True,
        #return_expectations={
            #"float": {"distribution": "normal", "mean": 60.0, "stddev": 15},
            #"date": {"earliest": "2020-12-01", "latest": "2021-11-01"},
            #"incidence": 0.95,},
    #),
    weight_recorded=patients.with_these_clinical_events(
        weight_codes,
        find_last_match_in_period=True,
        between=["index_date - 12 months", "index_date"],
        returning="binary_flag",
        return_expectations = {
        "incidence": 0.2,},
    ),
    atrial_fib=patients.with_these_clinical_events(
        af_codes,
        on_or_before="last_day_of_month(index_date)",
        returning="binary_flag",
        return_expectations={"incidence": 0.18,},
    ),
    

    # BMI, weight and height
    bmi=patients.most_recent_bmi(
        on_or_before="last_day_of_month(index_date)",
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
        on_or_before="last_day_of_month(index_date)",
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
        on_or_before="last_day_of_month(index_date)",
        returning="numeric_value",
        include_date_of_match=True,
        include_month=True,
        return_expectations={
            "float": {"distribution": "normal", "mean": 60.0, "stddev": 15},
            "date": {"earliest": "2020-12-01", "latest": "2021-11-01"},
            "incidence": 0.95,},
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
            "18-29": """ age >=  18 AND age < 30""",
            "30-39": """ age >=  30 AND age < 40""",
            "40-49": """ age >=  40 AND age < 50""",
            "50-59": """ age >=  50 AND age < 60""",
            "60-69": """ age >=  60 AND age < 70""",
            "70-79": """ age >=  70 AND age < 80""",
            ">80": """ age >=  80 AND age < 120""",
        },
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "missing": 0.055,
                    "18-29": 0.135,
                    "30-39": 0.135,
                    "40-49": 0.135,
                    "50-59": 0.135,
                    "60-69": 0.135,
                    "70-79": 0.135,
                    ">80": 0.135,
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
        id="doacs_by_sex_and_age",
        numerator="on_doac",
        denominator="population",
        group_by=["sex", "age"],
        small_number_suppression=True,
    ),

    Measure(
        id="doacs_by_carer",
        numerator="on_doac",
        denominator="population",
        group_by=["carer"]
    ),

    Measure(
        id="doacs_with_weight_recorded",
        numerator="weight_recorded",
        denominator="population",
        group_by=["on_doac"]
    ),

    Measure(
        id="doacs_with_egfr_recorded",
        numerator="egfr_recorded",
        denominator="population",
        group_by=["on_doac"]
    ),

    Measure(
        id="doacs_with_crcl_recorded",
        numerator="crcl_recorded",
        denominator="population",
        group_by=["on_doac"]
    ),

    Measure(
        id="doacs_with_serumcreatinine_recorded",
        numerator="serumcreatinine_recorded",
        denominator="population",
        group_by=["on_doac"]
    ),

    Measure(
        id="doacs_with_af_recorded",
        numerator="atrial_fib",
        denominator="population",
        group_by=["on_doac"]
    ),
        
]

