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
    cur.execute("CREATE TABLE IF NOT EXISTS artworks (id INT AUTO_INCREMENT PRIMARY KEY, title TEXT, origin TEXT, dept TEXT, styles TEXT, subjects TEXT)")
    
    artworks = get_api(url)
    for art_dict in artworks:
        # id = art_dict["id"]
        title = art_dict["title"]
        origin = art_dict["place_of_origin"]
        dept = art_dict["department_title"]
        styles = art_dict["style_titles"]
        subjects = art_dict["subject_titles"]

        sql = "INSERT INTO artworks (title, origin, dept, styles, subjects) VALUES (?, ?, ?, ?, ?)"
        vals = (title, origin, dept, styles, subjects)
        cur.execute(sql, vals)
    
    conn.commit()
    conn.close()


def main():
    url = "https://api.artic.edu/api/v1/artworks"
    get_api(url)
    db = "art_institute.db"
    store_database(db,url)

if __name__ == "__main__":
    main()
    

