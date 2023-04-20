import requests
import json
import sqlite3
import os

def get_api(url):
    params = {"limit": 25, "fields": "id,title,place_of_origin,department_title", "random":True}

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
                    dept TEXT, 
                    FOREIGN KEY (origin_id) REFERENCES origin(id)
                    )""")
    conn.commit()

def create_origin_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS origin (id INTEGER PRIMARY KEY AUTOINCREMENT, origin TEXT UNIQUE)")
    conn.commit()

def add_origin(url, cur, conn):
    artworks = get_api(url)
    # for art_dict in artworks: 
    #     cur.execute("INSERT OR IGNORE INTO origin (origin) VALUES (?)",
    #               (art_dict["place_of_origin"]))


    origins = set()
    for artwork in artworks:
        origins.add(artwork['place_of_origin'])

    for idx, origin in enumerate(origins):
        cur.execute("INSERT OR IGNORE INTO origin (id, origin) VALUES (?, ?)", (idx+1, origin))
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
        
        sql = "INSERT OR IGNORE INTO artworks (id, title, origin_id, dept) VALUES (?, ?, (SELECT id FROM origin WHERE origin = ?), ?)"
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
    
    add_origin(url, cur, conn)
    add_artwork(url, cur, conn)
    

    conn.close()

if __name__ == "__main__":
    main()
    

