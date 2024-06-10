import requests
from bs4 import BeautifulSoup
import re
current_page = 1
proceed = True
while proceed:
    url = "https://www.artsper.com/tn/contemporary-artists?page=" + str(current_page)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    secondary_title = soup.find("span", class_="secondary-title")
    if secondary_title and secondary_title.text.strip() == "No artwork matches your search":
        proceed = False
    else:
        all_artists = soup.find_all("section", class_="carousel carousel--artist")
        
        for artist in all_artists:
            item = {}
            item['link'] = "https://www.artsper.com" + artist.find("a").attrs["href"]
            link_page = requests.get(item['link'])
            link_soup = BeautifulSoup(link_page.text, "html.parser")
            item['nom'] = artist.find("a").text
            item['ville']=link_soup.find("span").text
            print(item['nom'])
            print(item['ville'])
    current_page += 1
            