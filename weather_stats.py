import sqlite3
import numpy as np
import matplotlib.pyplot as plt


def show_data(cur):
	cur.execute('SELECT DISTINCT year FROM weather')
	available_year = [row[0] for row in cur.fetchall()]
	years = []
	temps = []

	# Calculate average per year 
	for year in available_year:
		cur.execute('SELECT AVG(tavg) FROM weather WHERE year = ?', (year,))
		tavg = cur.fetchone()[0]
		years.append(year)
		temps.append(tavg)

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

	# Parse and show data
	show_data(cur)

	# Cleanup
	conn.commit()
	conn.close()

if __name__ == "__main__":
    main()