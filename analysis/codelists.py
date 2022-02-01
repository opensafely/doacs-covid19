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
    column="code",
)

#  Serum creatinine
creatinine_codes = codelist(
    ["codelists/user-RachelS99-doac-creatinine-level.csv"],
    system="snomed",
    column="code",
)

# eGFR
egfr_codes = codelist(
    ["codelists/user-RachelS99-doac-estimated-glomerular-filtration-rate.csv"],
    system="snomed",
    column="code",
)

# Creatinine clearance test
crcl_codes = codelist(
    ["codelists/user-RachelS99-doac-creatinine-clearance.csv"],
    system="snomed",
    column="code",
)

# certain p-gp inhibitors ciclosporin 80906007, dronedarone 443310000, erthromycin 30427009, ketoconazole 40232005
pgpi_codes = codelist(
    ["codelists/user-RachelS99-doac-certain-p-gp-inhibitors.csv"],
    system="snomed",
    column="code",
)

# verapamil 47898004
verapamil_codes = codelist(
    ["47898004"],
    system="snomed",
)

# gastritus, esophagitus, gastroesophageal refulx or increased risk of bleeding
contra_codes = codelist(
    ["codelists/user-RachelS99-doac-contraindications.csv"],
    system="snomed",
    column="code",
)

# Weight
weight_codes = codelist(
    ["27113001", "162763007"],
    system="snomed",
)

# Height
height_codes = codelist(
    ["271603002", "162755006"],
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