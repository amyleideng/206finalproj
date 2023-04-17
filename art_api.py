import requests
import json

def get_api(url):
    params = {"limit": 100, "fields": "id,title,place_of_origin,department_title,style_titles,subject_titles", "random":True}
   
    response = requests.get(url, params=params)
    artworks_data = response.json()

    artworks = artworks_data["data"]
    # print(artworks)
    return artworks

def main():
    url = "https://api.artic.edu/api/v1/artworks"
    get_api(url)

if __name__ == "__main__":
    main()
    

