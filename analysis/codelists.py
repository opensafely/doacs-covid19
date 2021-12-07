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
    "codelists/nhsd-primary-care-domain-refsets-afib_cod.csv",
    system="snomed",
)

# Serum creatinine
creatinine_codes = codelist(
    ["451..", "44J3.", "44J3z", "4I37.", "X771Q", "X80D7", "XE26a", "XE2q5", "XaERX", "XaERc", "XaETQ", "XacUK"],
    system="CTV3",
)

# eGFR
egfr_codes = codelist(
    ["857971000000104", "1011491000000107", "1011481000000105", "1020291000000100", "1107411000000100", "166181000000100", "167182002", "167183007", "222521000000103", "231131000000104", "444336003", "703502005", "791801000000102", "80274001", "963601000000106", "963621000000102", "996231000000108"],
    system="snomed",
)

# Creatinine clearance test
crcl_codes = codelist(
    ["167181009", "395680003", "968191000000100", "250735000", "1015981000000100", "167183007", "167182002"],
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