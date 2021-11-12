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
    
   
)