# Author: Timothy Majidzadeh
# Date Created: July 16, 2024
# Purpose: Parse the monthly temperature data accessed at https://www.ncei.noaa.gov/pub/data/cirs/climdiv/.
# Documentation: https://www.ncei.noaa.gov/pub/data/cirs/climdiv/county-readme.txt

# Import directories
from pathlib import Path
import pandas as pd
import numpy as np

# Change wd to run on other machines.
wd = Path("C:/Users/tmajidzadeh/Desktop/MIDS Notes/Datasci 209 (Data Visualization)/209_Majidzadeh_Sandoval_Venter/code")
schema = {
	"Column1": str,
	"Column2": float,
	"Column3": float,
	"Column4": float,
	"Column5": float,
	"Column6": float,
	"Column7": float,
	"Column8": float,
	"Column9": float,
	"Column10": float,
	"Column11": float,
	"Column12": float,
	"Column13": float,
}


types = ['min', 'max', 'avg']
raw_data_counties = {}
for temp_type in types:
	raw_data_counties[temp_type] = pd.read_excel(wd/f'../data/raw/climdiv-{temp_type}-raw.xlsx', dtype=schema, engine='calamine')
	# print(raw_data[temp_type].head())

raw_data_states = {}
for temp_type in types:
	raw_data_states[temp_type] = pd.read_excel(wd/f'../data/raw/climdiv-state-{temp_type}-raw.xlsx', dtype=schema, engine='calamine')
	# print(raw_data[temp_type].head())

county_xwalk = pd.read_csv(
	"C:/Users/tmajidzadeh/Desktop/MIDS Notes/Datasci 209 (Data Visualization)/209_Majidzadeh_Sandoval_Venter/data/ssa_fips_state_county_2023.csv",
	dtype = {
		'fipscounty': '|S',
		'fy2023cbs': '|S',
		'ssa_CODE': '|S'
	}
)
county_xwalk = county_xwalk[['fipscounty', 'countyname_fips']]
county_xwalk['countyname_fips'] = county_xwalk['countyname_fips'].str.capitalize() + " County"

state_dict = {
	"01": "Alabama",
	"30": "New York",
    "02": "Arizona",
    "31": "North Carolina",
    "03": "Arkansas",
    "32": "North Dakota",
    "04": "California",
    "33": "Ohio",
    "05": "Colorado",
    "34": "Oklahoma",
    "06": "Connecticut",
    "35": "Oregon",
    "07": "Delaware",
    "36": "Pennsylvania",
    "08": "Florida",
    "37": "Rhode Island",
    "09": "Georgia",
    "38": "South Carolina",
    "10": "Idaho",
    "39": "South Dakota",
    "11": "Illinois",
    "40": "Tennessee",
    "12": "Indiana",
    "41": "Texas",
    "13": "Iowa",
    "42": "Utah",
    "14": "Kansas",
    "43": "Vermont",
    "15": "Kentucky",
    "44": "Virginia",
    "16": "Louisiana",
    "45": "Washington",
    "17": "Maine",
    "46": "West Virginia",
    "18": "Maryland",
    "47": "Wisconsin",
    "19": "Massachusetts",
    "48": "Wyoming",
    "20": "Michigan",
    "50": "Alaska",
    "21": "Minnesota",
    "22": "Mississippi",
    "23": "Missouri",
    "24": "Montana",
    "25": "Nebraska",
    "26": "Nevada",
    "27": "New Hampshire",
    "28": "New Jersey",
    "29": "New Mexico",
}

state_dict_2 = {
	"001": "Alabama",
	"030": "New York",
    "002": "Arizona",
    "031": "North Carolina",
    "003": "Arkansas",
    "032": "North Dakota",
    "004": "California",
    "033": "Ohio",
    "005": "Colorado",
    "034": "Oklahoma",
    "006": "Connecticut",
    "035": "Oregon",
    "007": "Delaware",
    "036": "Pennsylvania",
    "008": "Florida",
    "037": "Rhode Island",
    "009": "Georgia",
    "038": "South Carolina",
    "010": "Idaho",
    "039": "South Dakota",
    "011": "Illinois",
    "040": "Tennessee",
    "012": "Indiana",
    "041": "Texas",
    "013": "Iowa",
    "042": "Utah",
    "014": "Kansas",
    "043": "Vermont",
    "015": "Kentucky",
    "044": "Virginia",
    "016": "Louisiana",
    "045": "Washington",
    "017": "Maine",
    "046": "West Virginia",
    "018": "Maryland",
    "047": "Wisconsin",
    "019": "Massachusetts",
    "048": "Wyoming",
    "020": "Michigan",
    "050": "Alaska",
    "021": "Minnesota",
    "022": "Mississippi",
    "023": "Missouri",
    "024": "Montana",
    "025": "Nebraska",
    "026": "Nevada",
    "027": "New Hampshire",
    "028": "New Jersey",
    "029": "New Mexico",
}

fips_dict = {
    'Alabama': '01',
    'Alaska': '02',
    'Arizona': '04',
    'Arkansas': '05',
    'California': '06',
    'Colorado': '08',
    'Connecticut': '09',
    'Delaware': '10',
    'Florida': '12',
    'Georgia': '13',
    'Hawaii': '15',
    'Idaho': '16',
    'Illinois': '17',
    'Indiana': '18',
    'Iowa': '19',
    'Kansas': '20',
    'Kentucky': '21',
    'Louisiana': '22',
    'Maine': '23',
    'Maryland': '24',
    'Massachusetts': '25',
    'Michigan': '26',
    'Minnesota': '27',
    'Mississippi': '28',
    'Missouri': '29',
    'Montana': '30',
    'Nebraska': '31',
    'Nevada': '32',
    'New Hampshire': '33',
    'New Jersey': '34',
    'New Mexico': '35',
    'New York': '36',
    'North Carolina': '37',
    'North Dakota': '38',
    'Ohio': '39',
    'Oklahoma': '40',
    'Oregon': '41',
    'Pennsylvania': '42',
    'Rhode Island': '44',
    'South Carolina': '45',
    'South Dakota': '46',
    'Tennessee': '47',
    'Texas': '48',
    'Utah': '49',
    'Vermont': '50',
    'Virginia': '51',
    'Washington': '53',
    'West Virginia': '54',
    'Wisconsin': '55',
    'Wyoming': '56',
}

month_dict = {
	"Jan": 1,
	"Feb": 2,
	"Mar": 3,
	"Apr": 4,
	"May": 5,
	"Jun": 6,
	"Jul": 7,
	"Aug": 8,
	"Sep": 9,
	"Oct": 10,
	"Nov": 11,
	"Dec": 12
}

element_dict = {
	"01": "Precipitation",
	"02": "Average Temperature",
	"25": "Heating Degree Days",
	"26": "Cooling Degree Days",
	"27": "Maximum Temperature",
	"28": "Minimum Temperature"
}

def process_data(df, mode):
	'''
	Clean the data, reshape to long format and create human-readable columns and indexes.
	Inputs:
		Raw temperature data from the NCEI.
		mode: 'county' for county data. Any other value for state data.
	Outputs:
		Long-format data with columns for year, month, state, county, and the temperature in farenheit.
	'''
	if mode == 'county':
		df['state_code'] = df['Column1'].str[:2]
		df['county_fips'] = df['Column1'].str[2:5]
		df['element_code'] = df['Column1'].str[5:7]
		df['year'] = df['Column1'].str[7:].astype(int)
		df['state'] = df['state_code'].map(state_dict)
	else:
		df['state_code'] = df['Column1'].str[:3]
		df['county_fips'] = df['Column1'].str[3:4]
		df['element_code'] = df['Column1'].str[4:6]
		df['year'] = df['Column1'].str[6:].astype(int)
		df['state'] = df['state_code'].map(state_dict_2)

	df['element'] = df['element_code'].map(element_dict)
	df.rename(
		columns = {
			"Column1": "raw_id",
			"Column2": "Jan",
			"Column3": "Feb",
			"Column4": "Mar",
			"Column5": "Apr",
			"Column6": "May",
			"Column7": "Jun",
			"Column8": "Jul",
			"Column9": "Aug",
			"Column10": "Sep",
			"Column11": "Oct",
			"Column12": "Nov",
			"Column13": "Dec"
		},
		inplace = True
	)
	if mode == 'county':
		df = df.melt(
			id_vars=['raw_id', 'state_code', 'state', 'county_fips', 'element_code', 'element', 'year'],
			value_vars=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
			var_name='month',
			value_name='temp_farenheit'
		)
	else:
		df = df.melt(
			id_vars=['raw_id', 'state_code', 'state', 'element_code', 'element', 'year'],
			value_vars=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
			var_name='month',
			value_name='temp_farenheit'
		)
	df['month_num'] = df['month'].map(month_dict)
	df['country'] = "United States"
	df['state_fips'] = df['state'].map(fips_dict)
	
	if mode == 'county':
		df['fipscounty'] = df['state_fips'] + df['county_fips']
		df = df.merge(
			county_xwalk,
			on = 'fipscounty',
			how = 'left'
		)

	return df

processed_data_counties, annual_data_counties = {}, {}
for temp_type in raw_data_counties.keys():
	processed_data_counties[temp_type] = process_data(raw_data_counties[temp_type], mode='county')
	processed_data_counties[temp_type].to_csv(wd/f'../data/monthly_county_{temp_type}_temps.csv', index=False)

	annual_data_counties[temp_type] = processed_data_counties[temp_type] \
		.groupby(['country', 'state', 'state_fips', 'fipscounty', 'countyname_fips', 'element_code', 'element', 'year']) \
		.agg({'temp_farenheit': np.nanmean})
	annual_data_counties[temp_type].to_csv(wd/f'../data/annual_county_{temp_type}_temps.csv', index=True)

concatenated = pd.concat(
	[processed_data_counties[temp_type] for temp_type in raw_data_counties.keys()]
)
concatenated.to_csv(wd/'../data/monthly_county_appended_temps.csv', index=False)

concatenated = pd.concat(
	[annual_data_counties[temp_type] for temp_type in raw_data_counties.keys()]
)
concatenated.to_csv(wd/'../data/annual_county_appended_temps.csv', index=True)


processed_data_states, annual_data_states = {}, {}
for temp_type in raw_data_states.keys():
	processed_data_states[temp_type] = process_data(raw_data_states[temp_type], mode='state')
	processed_data_states[temp_type].to_csv(wd/f'../data/monthly_state_{temp_type}_temps.csv', index=False)

	annual_data_states[temp_type] = processed_data_states[temp_type] \
		.groupby(['country', 'state', 'state_fips', 'element_code', 'element', 'year']) \
		.agg({'temp_farenheit': np.nanmean})
	annual_data_states[temp_type].to_csv(wd/f'../data/annual_state_{temp_type}_temps.csv', index=True)

concatenated = pd.concat(
	[processed_data_states[temp_type] for temp_type in raw_data_states.keys()]
)
concatenated.to_csv(wd/'../data/monthly_states_appended_temps.csv', index=False)

concatenated = pd.concat(
	[annual_data_states[temp_type] for temp_type in raw_data_states.keys()]
)
concatenated.to_csv(wd/'../data/annual_states_appended_temps.csv', index=True)