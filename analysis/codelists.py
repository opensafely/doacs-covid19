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
    ["1015971000000100", "1000731000000107", "113075003", "1010391000000109", "275792000", "168154007", "1032061000000108", "15373003", "1000981000000109", "1000991000000106", "1001011000000107"],
    system="snomed"
)

# eGFR
egfr_codes = codelist(
    ["1107411000000104", "857971000000104", "1011491000000107", "1011481000000105", "1020291000000100", "1107411000000100", "166181000000100", "167182002", "167183007", "222521000000103", "231131000000104", "444336003", "703502005", "791801000000102", "80274001", "963601000000106", "963621000000102", "996231000000108"],
    system="snomed",
)

# Creatinine clearance test
crcl_codes = codelist(
    ["1015981000000103", "784580008", "442407001", "442238003", "167181009", "395680003", "968191000000100", "250735000", "1015981000000100", "167183007", "167182002", "66329006", "1824008", "72950008", "42541005", "1967400092", "197012004", "74361008", "197028009", "235663001", "235664007", "444926003", "235654003", "235655002", "708164002", "235656001", "52305004"," 235657005", "360375007", "235659008", "235660003", "235661004", "235662006", "276527006", "285344007", "266433003", "235595009", "41788008", "28293008", "165388009", "248253003", "75753009"],
    system="snomed",
)

# certain p-gp inhibitors ciclosporin 80906007, dronedarone 443310000, erthromycin 30427009, ketoconazole 40232005
pgpi_codes = codelist(
    ["80906007", "443310000", "30427009", "40232005"],
    system="snomed",
)

# verapamil 47898004
verapamil_codes = codelist(
    ["47898004"],
    system="snomed",
)

# gastritus, esophagitus, gastroesophageal refulx or increased risk of bleeding
contra_codes = codelist(
    ["196731005", "4556007", "266503008", "25458004", "266504002", "84568007", "2043009", "89538001", "186143000", "2367005", "8493009", "196735001", "60002000"]
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