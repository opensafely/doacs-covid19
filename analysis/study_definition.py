from cohortextractor import (
    StudyDefinition,
    Measure,
    patients
)
from codelists import *

study=StudyDefinition(

    index_date="2021-10-01",

    # Configure the expectations framework
    default_expectations={
        "date": {"earliest": "2016-03-01", "latest": "today"},
        "rate": "exponential_increase",
        "incidence": 0.5,
    },
    population=patients.with_these_medications(
        doac_codes,
        between=["2016-03-01", "2021-10-31"],
        return_expectations={
            "incidence": 0.9}, 
    ),
)
