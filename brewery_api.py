import requests
import json
import os
import sqlite3
from brewery_stats import get_avg_brewery_type_by_state

def get_api(url):
    params = {"per_page": 100, "page": 1, "limit": 100, "fields": "id,name,brewery_type,state", "random":True}
   
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

def createBreweriesTable(cur, conn):
    cur.execute("""CREATE TABLE IF NOT EXISTS breweries (
                id TEXT PRIMARY KEY, 
                name TEXT UNIQUE, 
                brewery_type_id INTEGER NOT NULL, 
                state_id INTEGER NOT NULL, 
                FOREIGN KEY (brewery_type_id) REFERENCES types(id), 
                FOREIGN KEY (state_id) REFERENCES states(id)
                )""")
    conn.commit()

def createTypeTable(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS types (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, type TEXT UNIQUE)")
    conn.commit()

def createStateTable(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS states (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, state TEXT UNIQUE)")
    conn.commit()

def addTypes(breweries, cur, conn):
    types = set()
    for brewery in breweries:
        types.add(brewery["brewery_type"])

    for idx, t in enumerate(types):
        cur.execute(
            """INSERT OR IGNORE INTO types (id, type)
            VALUES (?, ?)
            """,
            (idx+1, t)
        )
    conn.commit()

def addStates(breweries, cur, conn):
    states = set()
    for brewery in breweries:
        states.add(brewery["state"])

    for idx, s in enumerate(states):
        cur.execute(
            """INSERT OR IGNORE INTO states (id, state)
            VALUES (?, ?)
            """,
            (idx+1, s)
        )
    conn.commit()

def addBreweries(breweries, cur, conn):
    rows = 0
    for brewery in breweries:
        if rows >= 25:
            break
        id_num = brewery["id"]
        name = brewery["name"]
        brewery_type = brewery["brewery_type"]
        state = brewery["state"]
        cur.execute(
            """INSERT OR IGNORE INTO breweries (id, name, brewery_type_id, state_id)
            VALUES (?, ?, (SELECT id FROM types WHERE type = ?), (SELECT id FROM states WHERE state = ?))
            """,
            (id_num, name, brewery_type, state)
            )
        rows += 1
    conn.commit()
'''
def get_info(cur, conn):
    cur.execute(
         """
        SELECT Types.type, States.state
        FROM Breweries
        JOIN Types ON Breweries.brewery_type_id = Types.id
        JOIN States ON Breweries.state_id = States.id
        """
    )
    return cur.fetchall()
'''

def main():
    url = "https://api.openbrewerydb.org/v1/breweries"
    breweries = get_api(url)
    cur, conn = setUpDatabase("brewery_database.db")
    createBreweriesTable(cur, conn)
    createTypeTable(cur, conn)
    createStateTable(cur, conn)

    addBreweries(breweries, cur, conn)
    addTypes(breweries, cur, conn)
    addStates(breweries, cur, conn)
    avg_brewery_type_by_state = get_avg_brewery_type_by_state(cur)
    for state in avg_brewery_type_by_state:
        print(f"{state}:")
        for brewery_type, percentage in avg_brewery_type_by_state[state].items():
            print(f"{brewery_type}: {percentage:.2%}")
        print()

if __name__ == "__main__":
    main()