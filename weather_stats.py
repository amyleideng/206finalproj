import json
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

def calculate_average(cur):
	cur.execute('SELECT DISTINCT year FROM weather')
	available_year = [row[0] for row in cur.fetchall()]
	data = {}

	# Calculate average per year 
	for year in available_year:
		cur.execute('SELECT AVG(tavg) FROM weather WHERE year = ?', (year,))
		tavg = cur.fetchone()[0]
		data[year] = tavg

	return data

def show_data(fp):
	data = json.load(fp)
	years = list(data.keys())
	temps = list(data.values())

	# Plot data as bar graph
	plt.bar(np.array([y for y in years]), np.array([t for t in temps]), tick_label=years)
	plt.xticks(rotation=45, ha='right', fontsize=8)
	plt.title('Average Temperatures by Year')
	plt.xlabel('Year')
	plt.ylabel('Temperature (Celsius)')
	plt.show()

def main():
	# Connect to + Initialize database
	conn = sqlite3.connect("weather.db")
	cur = conn.cursor()

	# Calculate, Store, Show data
	data = calculate_average(cur)
	with open('calculations.json', 'w') as file:
		json.dump(data, file)
	with open('calculations.json', 'r') as file:
		show_data(file)

	# Cleanup
	conn.commit()
	conn.close()

if __name__ == "__main__":
    main()
