import requests
import json
import sqlite3
import datetime
import dateutil.relativedelta
from datetime import datetime
import matplotlib.pyplot as plt

def get_api(url, start, end):
	querystring = {"station":"KARB0","start":start,"end":end}

	headers = {	
		"X-RapidAPI-Key": "6f2ff269bdmshbf6fcc25cf324e3p15c9a7jsn13798e293a74",
		"X-RapidAPI-Host": "meteostat.p.rapidapi.com"
	}
	response = requests.request("GET", url, headers=headers, params=querystring)
	return response.json()

def get_range(cur):
	# Find earliest date
	cur.execute('''
		SELECT *
		FROM weather
		ORDER BY year, month
		LIMIT 1
	''')
	earliest = cur.fetchone()
	if earliest is None:
		earliest = (datetime.now().year, datetime.now().month)

	# Calculate 12 months prior
	earliest = datetime.strptime(f'{earliest[0]}-{earliest[1]}', "%Y-%m")
	low = earliest - dateutil.relativedelta.relativedelta(months = 13)
	high = earliest - dateutil.relativedelta.relativedelta(months = 1)
	return (
		f'{low.year}-{str(low.month).zfill(2)}-01',
		f'{high.year}-{str(high.month).zfill(2)}-01'
	)

def init_database(cur):
	cur.execute('''
		CREATE TABLE IF NOT EXISTS weather (
			year INT NOT NULL,
			month INT NOT NULL,
			tavg DECIMAL(5,2),
			PRIMARY KEY (year, month)
		)
	''')

def insert_month(cur, entry):
	cur.execute(
		"INSERT INTO weather (year, month, tavg) VALUES (?, ?, ?)",
		(entry['year'], entry['month'], entry['tavg'])
	)
	
def parse_data(cur, data):
	for entry in data['data']:
		date = datetime.strptime(entry['date'], "%Y-%m-%d")
		tavg = entry['tavg']
		insert_month(cur, {
			'year': date.year,
			'month': date.month,
			'tavg': tavg
		})

def main():
	# Connect to + Initialize database
	conn = sqlite3.connect("weather.db")
	cur = conn.cursor()
	init_database(cur)

	# Retrieve data from api
	url = "https://meteostat.p.rapidapi.com/stations/monthly"
	(low, high) = get_range(cur)
	response = get_api(url, low, high)

	# Parse and show data
	parse_data(cur, response)

	# Cleanup
	conn.commit()
	conn.close()

if __name__ == "__main__":
    main()
