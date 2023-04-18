import requests
import json
import sqlite3
import os

def get_api(url):
    params = {"limit": 100, "fields": "id,title,place_of_origin,department_title,style_titles,subject_titles", "random":True}
   
    response = requests.get(url, params=params)
    artworks_data = response.json()

    artworks = artworks_data["data"]
    return artworks

def setup_database(db):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db)
    # conn = sqlite3.connect(db)
    cur = conn.cursor()
    return cur, conn

def create_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS artworks (id_num INTEGER PRIMARY KEY, title TEXT UNIQUE, origin TEXT, dept TEXT, styles TEXT, subjects TEXT)")
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
        style_titles = ", ".join(art_dict["style_titles"])
        subject_titles = ", ".join(art_dict["subject_titles"])
        
        sql = "INSERT OR IGNORE INTO artworks (id_num, title, origin, dept, styles, subjects) VALUES (?, ?, ?, ?, ?, ?)"
        vals = (id, title, place_of_origin, department_title, style_titles, subject_titles)
        cur.execute(sql, vals)

        rows += 1

    conn.commit()

def main():
    url = "https://api.artic.edu/api/v1/artworks"
    get_api(url)

    # db = "art_institute.db"
    cur, conn = setup_database("art_institute.db")
    create_table(cur, conn)
    add_artwork(url, cur, conn)
    
    conn.close()

if __name__ == "__main__":
    main()
    

