import requests
import json
import sqlite3
from sqlite3 import error

def get_api(url):
    params = {"per_page": 100, "page": 1, "limit": 100, "fields": "id,name,brewery_type.address_1,address_2,address_3,city,state_province,postal_code,country,longitude,latitude,phone,website_url,state,street", "random":True}
   
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.reason}")
        return None

    try:
        brewing_data = response.json()
        num_breweries = len(brewing_data)
        print(f"Number of breweries: {num_breweries}")
        for brewery in brewing_data:
            print(brewery["name"], brewery["city"], brewery["state"], brewery["website_url"])
        return brewing_data
    except:
        print("Error parsing JSON response")
        return None

def store_database():
    #connect to the database
    conn = sqlite3.connect('brewery_database.db')

    #get a cursos from the database connection
    cur = conn.cursor()

    #select data from the User table
    cur.execute('CREATE TABLE Breweries (Brewery, State, Type) VALUES (?, ?)')
    for row in cur:
        print(row)

    #close the cursor
    cur.close()

def main():
    url = "https://api.openbrewerydb.org/v1/breweries"
    get_api(url)

if __name__ == "__main__":
    main()