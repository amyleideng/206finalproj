import requests
import json
import sqlite3
import os

def get_api(url):
    params = {"limit": 100, "fields": "id,title,place_of_origin,department_title", "random":True}

    response = requests.get(url, params=params)
    artworks_data = response.json()
    artworks = artworks_data["data"]

    return artworks

def setup_database(db):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    cur = conn.cursor()
    return cur, conn

def create_table(cur, conn):
    cur.execute("""CREATE TABLE IF NOT EXISTS artworks (
                    id INTEGER PRIMARY KEY, 
                    title TEXT UNIQUE, 
                    origin_id INTEGER, 
                    dept_id INTEGER, 
                    FOREIGN KEY (origin_id) REFERENCES origin(id),
                    FOREIGN KEY (dept_id) REFERENCES dept(id)
                    )""")
    conn.commit()

def create_origin_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS origin (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, origin TEXT UNIQUE)")
    conn.commit()

def create_dept_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS dept (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, dept TEXT UNIQUE)")
    conn.commit()

def add_origin(url, cur, conn):
    artworks = get_api(url)

    origins = set()
    for art_dict in artworks:
        origins.add(art_dict['place_of_origin'])

    for idx, origin in enumerate(origins):
        cur.execute("INSERT OR IGNORE INTO origin (id, origin) VALUES (?, ?)", (idx+1, origin))
    conn.commit()

def add_dept(url, cur, conn):
    artworks = get_api(url)
    depts = set()
    for art_dict in artworks:
        depts.add(art_dict["department_title"])

    for idx, dept in enumerate(depts):
        cur.execute("INSERT OR IGNORE INTO dept (id, dept) VALUES (?, ?)", (idx+1, dept))
    conn.commit()

def add_artwork(url, cur, conn):
    rows = 0
    artworks = get_api(url)
    for art_dict in artworks:
        if rows >= 25:
            break 
        id = art_dict["id"]
        title = art_dict["title"]
        place_of_origin = art_dict["place_of_origin"]
        department_title = art_dict["department_title"]
        
        sql = "INSERT OR IGNORE INTO artworks (id, title, origin_id, dept_id) VALUES (?, ?, (SELECT id FROM origin WHERE origin = ?), (SELECT id FROM dept WHERE dept = ?))"
        vals = (id, title, place_of_origin, department_title)
        cur.execute(sql, vals)

        rows += 1

    conn.commit()

def main():
    url = "https://api.artic.edu/api/v1/artworks"
    get_api(url)

    cur, conn = setup_database("art_institute.db")
    create_table(cur, conn)
    create_origin_table(cur, conn)
    create_dept_table(cur, conn)

    add_origin(url, cur, conn)
    add_dept(url, cur, conn)
    add_artwork(url, cur, conn)
    

    conn.close()

if __name__ == "__main__":
    main()
    

