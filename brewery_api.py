import requests
import json
import os
import sqlite3
from brewery_stats import get_avg_brewery_type_by_state
from brewery_stats import plot_avg_brewery_type_by_state

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

def write_json_file(avg_brewery_type_by_state):
    path = os.path.dirname(os.path.abspath(__file__))
    with open("brewery_stats.json", "w") as file:
        json.dump(avg_brewery_type_by_state, file, indent = 4)

def merge_databases(db_names, new_db_name):
    conn = sqlite3.connect(new_db_name)

    for i, db_name in enumerate(db_names):
        conn.execute(f"ATTACH DATABASE '{db_name}' AS db{i}")
    
    # Copy tables from art_institute.db
    conn.execute("""
        CREATE TABLE IF NOT EXISTS artworkss (
                    id INTEGER PRIMARY KEY, 
                    title TEXT, 
                    origin_id INTEGER, 
                    dept_id INTEGER, 
                    FOREIGN KEY (origin_id) REFERENCES origin(id),
                    FOREIGN KEY (dept_id) REFERENCES dept(id)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS origins (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            origins TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS depts (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            depts TEXT
        )
    """)
    conn.execute("""
        INSERT OR IGNORE INTO artworkss
        SELECT * FROM db0.artworks
    """)
    conn.execute("""
        INSERT OR IGNORE INTO origins
        SELECT * FROM db0.origin
    """)
    conn.execute("""
        INSERT OR IGNORE INTO depts
        SELECT * FROM db0.dept
    """)
    
    # Copy tables from brewery_database.db
    conn.execute("""
        CREATE TABLE IF NOT EXISTS breweriess (
            id TEXT PRIMARY KEY,
            name TEXT,
            state_id INTEGER,
            brewery_type_id INTEGER,
            FOREIGN KEY (state_id) REFERENCES states (id),
            FOREIGN KEY (brewery_type_id) REFERENCES types (id)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS statess (
            id INTEGER PRIMARY KEY,
            states TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS typess (
            id INTEGER PRIMARY KEY,
            types TEXT
        )
    """)
    conn.execute("""
        INSERT OR IGNORE INTO breweriess
        SELECT * FROM db1.breweries
    """)
    conn.execute("""
        INSERT OR IGNORE INTO statess
        SELECT * FROM db1.states
    """)
    conn.execute("""
        INSERT OR IGNORE INTO typess
        SELECT * FROM db1.types
    """)
    
    # Copy tables from weather.db
    conn.execute("""
        CREATE TABLE IF NOT EXISTS weathers (
			year INT NOT NULL,
			month INT NOT NULL,
			tavg DECIMAL(5,2),
			PRIMARY KEY (year, month)
        )
    """)
    conn.execute("""
        INSERT OR IGNORE INTO weathers
        SELECT * FROM db2.weather
    """)
    
    conn.commit()
    conn.close()

def main():
    url = "https://api.openbrewerydb.org/v1/breweries"
    breweries = get_api(url)
    cur, conn = setUpDatabase("brewery_database.db")
    #making brewery_database.db
    createBreweriesTable(cur, conn)
    createTypeTable(cur, conn)
    createStateTable(cur, conn)
    cursor = conn.cursor()
    cursor.execute("PRAGMA database_list")
    print(cursor.fetchall())
    addBreweries(breweries, cur, conn)
    addTypes(breweries, cur, conn)
    addStates(breweries, cur, conn)

    #plot data
    avg_brewery_type_by_state = get_avg_brewery_type_by_state(cur)
    plot_avg_brewery_type_by_state(avg_brewery_type_by_state)
    write_json_file(avg_brewery_type_by_state)

    #making combined database
    #reassigning cur and conn
    cur, conn = setUpDatabase("combined.db")
    db_names = ["art_institute.db", "brewery_database.db", "weather.db"]
    new_db_name = "combined.db"
    merge_databases(db_names, new_db_name)
 

if __name__ == "__main__":
    main()