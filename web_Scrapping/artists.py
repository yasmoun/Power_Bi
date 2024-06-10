import requests
from bs4 import BeautifulSoup
import re
import mysql.connector



current_page = 1
proceed = True
while proceed:
    url = "https://www.artsper.com/tn/contemporary-artworks?page=" + str(current_page)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    secondary_title = soup.find("span", class_="secondary-title")
    if secondary_title and secondary_title.text.strip() == "No artwork matches your search":
        proceed = False
    else:
        all_oeuvres = soup.find_all("article", class_="card-artwork item item--max-col-3")
        for oeuvre in all_oeuvres:
            item = {}
            item['titre'] = oeuvre.cite.text
            item['artiste'] = oeuvre.find("a", class_="js-catch-click").text
            item['price'] = oeuvre.find("span", class_="card-artwork__price").text.strip()
            item['link'] = "https://www.artsper.com" + oeuvre.find("a").attrs["href"]
            link_page = requests.get(item['link'])
            link_soup = BeautifulSoup(link_page.text, "html.parser")
            discount_element = link_soup.find("span", class_="price price-current mr-5")
            if discount_element:
                item['discount'] = discount_element.text.strip()
            else:
                item['discount'] = "non Soldé"
            
            date_left_element = link_soup.find("em", class_="remaining")
            if date_left_element:
                item['date_left'] = date_left_element.attrs["data-remaining"]
            else:
                item['date_left'] = "Date non disponible"
            
            item['cD'] = oeuvre.find("p", class_="card-artwork__text")
            if item['cD']:
                parties = item['cD'].text.split(" - ")
                categorie = parties[0]
                dimension= parties[1]
            else:
                item['categorie'] = "Catégorie non disponible"
                item['dimension'] = "Dimensions non disponibles"

            nombree=link_soup.find("div",class_="pl-30").p.text
            if nombree=="Unique work":
                nombre=1
            else :
                match = re.search(r'\b(\d+)\b', nombree) 
                if match:
                    nombre = match.group(1)
                else:
                    nombre = 0
            valablee = link_soup.find("p", class_="color-orange mt-10")
            if valablee:
                valable_text = valablee.text.strip()
                v = re.search(r'\b(\d+)\b', valable_text)
                valable = v.group(1) 
            else:
                if item['price']=="Sold" and nombre==1 :
                    valable=0
                else:
                    valable=1

            
            adre =link_soup.find("p", class_="color-grey-6 dis-flex y-center").text.split()
            lieu=adre[0]
            year_birth = adre[2]
            yearIns= link_soup.find("p", class_="dis-flex")
            if yearIns:
                year_inscription = yearIns.text.strip()
                v = re.search(r'\b(\d+)\b', year_inscription )
                yearIn = v.group(1)


            titre = item['titre']
            artiste = item['artiste']
            categorie = categorie 
            dimension = dimension
            quantite = nombre
            disponibilite = valable
            prix = item['price']
            remise=item['discount']
            date_limite=item['date_left']           
            #sql = "INSERT INTO oeuvres (titre, artiste,categorie, dimension, quantite, disponibilite,prix,remise,date_limite) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            #values = (titre, artiste,categorie, dimension, quantite, disponibilite,prix,remise,date_limite)

            #cursor.execute(sql, values)
            print(yearIn)
            print(lieu)

        #conn.commit()
            nom = link_soup.find("span", class_="typography--bold typography--underline pointer").text

        current_page += 1
