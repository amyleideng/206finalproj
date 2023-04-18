import unittest
import requests
import json
import os
import sqlite3

def get_api(url):
    params = {"per_page": 100, "page": 1, "limit": 100, "fields": "id,name,brewery_type,address_1,address_2,address_3,city,state_province,postal_code,country,longitude,latitude,phone,website_url,state,street", "random":True}
   
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.reason}")
        return None

    try:
        brewing_data = response.json()
        return brewing_data
    except:
        print("Error parsing JSON response")
        return None

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def createTable(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS breweries (id INTEGER PRIMARY KEY, id_num TEXT, name TEXT, type TEXT, city TEXT, postal_code TEXT, country TEXT, state TEXT)")
    conn.commit()

def addBreweries(url, cur, conn):
    rows = 0
    while rows < 25:
        breweries = get_api(url)
        for brewery in breweries:
            id_num = brewery["id"]
            name = brewery["name"]
            type = brewery["brewery_type"]
            city = brewery["city"]
            postal_code = brewery["postal_code"]
            country = brewery["country"]
            state = brewery["state"]
            cur.execute(
                """INSERT OR IGNORE INTO breweries (id, name, brewery_type, 
                city, postal_code, country, state)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (id_num, name, type, city, postal_code, country, state)
            )
        conn.commit()
            

def main():
    url = "https://api.openbrewerydb.org/v1/breweries"
    get_api(url)
    cur, conn = setUpDatabase("brewery_database.db")
    createTable(cur, conn)
    addBreweries(url, cur, conn)

if __name__ == "__main__":
    main()