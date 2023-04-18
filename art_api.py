import requests
import json
import sqlite3

def get_api(url):
    params = {"limit": 100, "fields": "id,title,place_of_origin,department_title,style_titles,subject_titles", "random":True}
   
    response = requests.get(url, params=params)
    artworks_data = response.json()

    artworks = artworks_data["data"]
    return artworks

def store_database(db, url):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS artworks (id INTEGER PRIMARY KEY, id_num TEXT, title TEXT, origin TEXT, dept TEXT, styles TEXT, subjects TEXT)")

    rows = 0
    while rows < 25: 
        artworks = get_api(url)
        for art_dict in artworks:
            cur.execute("SELECT * FROM artworks WHERE id=?", (art_dict["id"],))
            existing_artwork = cur.fetchone()
            if existing_artwork:
                continue

            id_num = art_dict["id"]
            title = art_dict["title"]
            place_of_origin = art_dict["place_of_origin"]
            department_title = art_dict["department_title"]
            style_titles = ", ".join(art_dict["style_titles"])
            subject_titles = ", ".join(art_dict["subject_titles"])

            sql = "INSERT INTO artworks (id_num, title, origin, dept, styles, subjects) VALUES (?, ?, ?, ?, ?, ?)"
            vals = (id_num, title, place_of_origin, department_title, style_titles, subject_titles)
            cur.execute(sql, vals)

            conn.commit()
            rows += 1
            if rows >= 25:
                break
    conn.close()


def main():
    url = "https://api.artic.edu/api/v1/artworks"
    get_api(url)
    db = "art_institute.db"
    store_database(db,url)

if __name__ == "__main__":
    main()
    

