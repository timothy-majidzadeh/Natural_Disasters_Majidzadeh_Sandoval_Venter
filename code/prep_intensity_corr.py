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

fema_raw = pd.read_csv(
		wd/f"../data/Fema.csv"
	)

st_areas = pd.read_csv(
		wd/f"../data/st_areas.csv"
	)

temps_raw = pd.read_csv(
		wd/f"../data/annual_state_avg_temps.csv"
	)

us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}

def first(series):
	return np.mean(series[0:5])

def last(series):
	return np.mean(series[-5:])

temps_first_last = temps_raw[(temps_raw['year'] >= 1960) & (temps_raw['year'] < 2024)] \
	.sort_values(['state', 'year']) \
	.groupby('state') \
	.agg(
		{
		'temp_farenheit': [first, last]
		}
	)

temps_first_last.columns = temps_first_last.columns.droplevel()
temps_first_last['change'] = temps_first_last['last'] - temps_first_last['first']
temps_first_last.reset_index(inplace=True)
temps_first_last['state'] = temps_first_last['state'].map(us_state_to_abbrev)

fema_with_areas = fema_raw \
	.merge(
		st_areas,
		how = 'left',
		on = 'state'
	)
fema_with_areas['thousand_square_miles'] = pd.to_numeric(fema_with_areas['area(sq_miles)'].str.replace(',', '')) / 1000

fema_filtered = fema_with_areas[(fema_with_areas['year'] >= 2018) & (fema_with_areas['year'] < 2024)] 

fema_intensity = fema_filtered\
	.groupby(['state']) \
	.agg(
		{
		'fema_number': pd.Series.nunique,
		'thousand_square_miles': 'first'
		}
	)
fema_intensity['intensity'] = fema_intensity['fema_number'] / fema_intensity['thousand_square_miles']
fema_intensity = fema_intensity.sort_values('intensity', ascending = False)

fema_filtered = fema_filtered \
	.merge(
		temps_first_last,
		'inner',
		'state'
	)

fema_intensity = fema_intensity \
	.merge(
		temps_first_last,
		'inner',
		'state'
	)

fema_filtered.to_csv(
	wd/f'../data/fema_w_temp_change.csv',
	index=False
)

fema_intensity.to_csv(
	wd/f'../data/temp_change_w_intensity.csv',
	index=False
)