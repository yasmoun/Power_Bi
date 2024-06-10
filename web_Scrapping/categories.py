from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.webdriver import WebDriver
from bs4 import BeautifulSoup

# Chemin vers le pilote WebDriver Edge
webdriver_path = r'C:\Users\yasmine\Downloads\edgedriver_win64 (1)\msedgedriver.exe'

# Initialiser le service du navigateur Edge
edge_service = Service(webdriver_path)

# Démarrer le service
edge_service.start()

# Initialiser le navigateur Edge
driver = WebDriver(service=edge_service)

# Charger la page
url = "https://www.artsper.com/tn/contemporary-artworks"
driver.get(url)

# Récupérer le contenu de la page après le chargement dynamique
page_source = driver.page_source

# Fermer le navigateur
driver.quit()

# Analyser le HTML de la page avec BeautifulSoup
soup = BeautifulSoup(page_source, "html.parser")

# Trouver la balise avec la classe "catalog__filters"
filters_section = soup.find("div", class_="ais-RefinementList")

if filters_section:
    # Si la balise est trouvée, trouver toutes les catégories à l'intérieur de cette balise
    all_categories = filters_section.find_all("li", class_="ais-RefinementList-item")
    
    for categorie in all_categories:
        try:
            item = {}
            item['categ'] = categorie.find("span", class_="ais-RefinementList-labelText").text
            print(item['categ'])
        except Exception as e:
            print("Erreur lors de l'extraction de la catégorie :", e)
else:
    print("Balise 'catalog__filters' non trouvée.")