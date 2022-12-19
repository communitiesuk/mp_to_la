import pandas as pd

# constituency to LA ons code is taken from here:
# 'https://geoportal.statistics.gov.uk/datasets/ons::ward-to-westminster-parliamentary-constituency-to-local-authority-district-to-upper-tier-local-authority-december-2020-lookup-in-the-united-kingdom-v2-1/explore'

# MP names are taken from here:
# 'https://www.theyworkforyou.com/mps/?f=csv'
# Have manually added West Lancashire which is due a by election after Rosie Cooper resigned on 20 Nov 2022
# Manually changed Weston-Super-Mare to Weston-super-Mare to make the constituency merge work

# dictionary of old to new LA names
restructured_names_2023 = {'Aylesbury Vale': 'Buckinghamshire',
                           'Chiltern': 'Buckinghamshire',
                           'South Bucks': 'Buckinghamshire',
                           'Wycombe': 'Buckinghamshire',
                           'Bournemouth UA': 'Bournemouth, Christchurch & Poole',
                           'Christchurch': 'Bournemouth, Christchurch & Poole',
                           'Poole UA': 'Bournemouth, Christchurch & Poole',
                           'East Dorset': 'Dorset',
                           'North Dorset': 'Dorset',
                           'West Dorset': 'Dorset',
                           'Purbeck': 'Dorset',
                           'Weymouth and Portland': 'Dorset',
                           'West Somerset': 'Somerset',
                           'Taunton Deane': 'Somerset',
                           'Corby': 'North Northamptonshire',
                           'East Northamptonshire': 'North Northamptonshire',
                           'Kettering': 'North Northamptonshire',
                           'Wellingborough': 'North Northamptonshire',
                           'Daventry': 'West Northamptonshire',
                           'Northampton': 'West Northamptonshire',
                           'South Northamptonshire': 'West Northamptonshire',
                           'Allerdale': 'Cumberland',
                           'Carlisle': 'Cumberland',
                           'Copeland': 'Cumberland',
                           'Barrow-in-Furness': 'Westmorland and Furness',
                           'Eden': 'Westmorland and Furness',
                           'South Lakeland': 'Westmorland and Furness',
                           'Craven': 'North Yorkshire',
                           'Hambleton': 'North Yorkshire',
                           'Harrogate': 'North Yorkshire',
                           'Richmondshire': 'North Yorkshire',
                           'Ryedale': 'North Yorkshire',
                           'Scarborough': 'North Yorkshire',
                           'Selby': 'North Yorkshire',
                           'Mendip': 'Somerset',
                           'Sedgemoor': 'Somerset',
                           'South Somerset': 'Somerset',
                      }

# dictionary of old to new ons codes
restructured_ons_codes_2023 = {'E07000049': 'E06000059',
                               'E07000050': 'E06000059',
                               'E07000051': 'E06000059',
                               'E07000052': 'E06000059',
                               'E07000053': 'E06000059',
                               'E06000028': 'E06000058',
                               'E07000048': 'E06000058',
                               'E06000029': 'E06000058',
                               'E07000190': 'E06000066',
                               'E07000191': 'E06000066',
                               'E07000004': 'E06000060',
                               'E07000005': 'E06000060',
                               'E07000006': 'E06000060',
                               'E07000007': 'E06000060',
                               'E07000150': 'E06000061',
                               'E07000152': 'E06000061',
                               'E07000153': 'E06000061',
                               'E07000156': 'E06000061',
                               'E07000151': 'E06000062',
                               'E07000154': 'E06000062',
                               'E07000155': 'E06000062',
                               'E07000187': 'E06000066',
                               'E07000188': 'E06000066',
                               'E07000189': 'E06000066',
                               'E07000026': 'E06000063',
                               'E07000028': 'E06000063',
                               'E07000029': 'E06000063',
                               'E07000027': 'E06000064',
                               'E07000030': 'E06000064',
                               'E07000031': 'E06000064',
                               'E07000163': 'E06000065',
                               'E07000164': 'E06000065',
                               'E07000165': 'E06000065',
                               'E07000166': 'E06000065',
                               'E07000167': 'E06000065',
                               'E07000168': 'E06000065',
                               'E07000169': 'E06000065',
                               }

df_mp_names = pd.read_csv('mp_names.csv')
df_lad_pcon = pd.read_csv('lad_to_pcon.csv')

# filter to England only 
# remove duplicates
df_lad_pcon = (df_lad_pcon
               [df_lad_pcon.LAD20CD.str.startswith('E')]
               .drop_duplicates(subset=['PCON20CD', 'LAD20CD'])
               )

# merge mp names by constituency name
# sort by MP name
# keep selected columns
# restructure
df_lad_pcon = (df_lad_pcon.merge(df_mp_names, left_on='PCON20NM', right_on='Constituency', how='left')
               .sort_values(by=['First name', 'Last name'])
               [['First name', 'Last name', 'PCON20CD', 'PCON20NM', 'LAD20CD', 'LAD20NM']]
               .replace(restructured_names_2023)
               .replace(restructured_ons_codes_2023)
               )

# output to excel
df_lad_pcon.to_excel('mp_to_la_lookup.xlsx', index=False)

