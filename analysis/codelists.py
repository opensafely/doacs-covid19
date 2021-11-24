from cohortextractor import (
    codelist_from_csv,
    codelist,
)

# DOACs
doac_codes = codelist_from_csv(
    "codelists/opensafely-direct-acting-oral-anticoagulants-doac.csv",
    system="snomed",
    column='id',
    category_column="bnf_code"
)
doac_chemical = codelist_from_csv(
    "codelists/opensafely-direct-acting-oral-anticoagulants-doac.csv",
    system="snomed",
    column='id',
    category_column="chemical"
)

af_codes = codelist_from_csv(
    "codelists/opensafely-atrial-fibrillation-clinical-finding.csv",
    system="ctv3",
    column="CTV3Code"
)

# Serum creatinine
creatinine_codes = codelist(
    ["113075003", "1000731000000100", "168154007", "1032061000000100", "15373003", "1010391000000100", "1000981000000100", "1000991000000100", "1001011000000100"],
    system="snomed",
)

# eGFR
egfr_codes = codelist(
    ["1107411000000104"],
    system="snomed",
)

# Creatinine clearance test
crcl_codes = codelist(
    ["167181009"],
    system="snomed",
)

# Weight
weight_codes = codelist(
    ["27113001"],
    system="snomed",
)

# Height
height_codes = codelist(
    ["271603002"],
    system="snomed",
)

# Ethnicity codes
eth2001 = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-eth2001.csv",
    system="snomed",
    column="code",
    category_column="grouping_6_id",
)

# Any other ethnicity code
non_eth2001 = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-non_eth2001.csv",
    system="snomed",
    column="code",
)

# Ethnicity not given - patient refused
eth_notgiptref = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-eth_notgiptref.csv",
    system="snomed",
    column="code",
)

# Ethnicity not stated
eth_notstated = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-eth_notstated.csv",
    system="snomed",
    column="code",
)

# Ethnicity no record
eth_norecord = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-eth_norecord.csv",
    system="snomed",
    column="code",
)

# Are they registered as a carer, a person caring for a dependant
carer = codelist_from_csv(
    "codelists/primis-covid19-vacc-uptake-carer.csv",
    system="snomed",
    column="code",
)