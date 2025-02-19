import requests
from bs4 import BeautifulSoup
import csv
import asyncio
import aiohttp
import time

async def fetch_html(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

def scrape_book(book_url):
    """Fonction permettant d'extraire les données d'un livre à partir de l'URL produit"""
    # Requête HTTP
    response = requests.get(book_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extraction des informations nécessaires
    title = soup.find("h1").string

    table = soup.find("table", class_="table table-striped")
    universal_product_code = table.find_all("td")[0].string
    price_including_tax = table.find_all("td")[3].string.strip("Â")
    price_excluding_tax = table.find_all("td")[2].string.strip("Â")

    number_available = soup.find("p", class_="instock availability").text.strip()

    unordered_list = soup.find("ul", class_="breadcrumb")
    category = unordered_list.find_all("li")[-2].text.strip()

    return [book_url, universal_product_code, title, price_including_tax,
            price_excluding_tax, number_available, category]

async def get_books_urls_from_category(category_url, books_urls = None):
    """Fonction récursive permettant de récupérer les URLS de tous les livres d'une catégorie"""

    if books_urls is None:
        books_urls = []
    text = await fetch_html(category_url)
    soup = BeautifulSoup(text, 'html.parser')

    category = soup.find("h1").string

    # Extraction des URLs des livres de la page actuelle
    for url in soup.select("h3 a"):
        books_urls.append(url["href"].replace("../../..", "http://books.toscrape.com/catalogue"))

    # Si bouton next, on appelle la fonction récursivement
    next_page = soup.select_one("li.next a")

    if next_page:
        next_page_url = category_url.rsplit("/", 1)[0] + "/" + next_page["href"]
        return await get_books_urls_from_category(next_page_url, books_urls)

    print(f"Il y a {len(books_urls)} livres dans la catégorie {category}.")
    return books_urls

def write_books_data(list_category_urls):
    books_data = []
    for url in list_category_urls:
        books_data.append(scrape_book(url))

    # Sauvegarde des données dans un fichier CSV
    filename = "books_data.csv"
    headers = ["Page url", "UPC", "Title", "Price Including Tax", "Price Excluding Tax", "Availability", "Category"]

    with open(filename, "w") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(books_data)

    print(f"Données extraites et sauvegardées dans {filename}")    


async def main():
    start_time = time.time()
    urls = [
        "http://books.toscrape.com/catalogue/category/books/travel_2/index.html",
        "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
        "http://books.toscrape.com/catalogue/category/books/travel_2/index.html",
        "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        "http://books.toscrape.com/catalogue/category/books/travel_2/index.html",
        "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        "http://books.toscrape.com/catalogue/category/books/travel_2/index.html",
        "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        "http://books.toscrape.com/catalogue/category/books/travel_2/index.html",
        "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        "http://books.toscrape.com/catalogue/category/books/travel_2/index.html",
        "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        "http://books.toscrape.com/catalogue/category/books/travel_2/index.html",
        "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        "http://books.toscrape.com/catalogue/category/books/travel_2/index.html",
        "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        "http://books.toscrape.com/catalogue/category/books/travel_2/index.html",
        "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        "http://books.toscrape.com/catalogue/category/books/travel_2/index.html",
        "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        "http://books.toscrape.com/catalogue/category/books/travel_2/index.html",
        "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        "http://books.toscrape.com/catalogue/category/books/travel_2/index.html",
        "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        "http://books.toscrape.com/catalogue/category/books/travel_2/index.html",
        "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        "http://books.toscrape.com/catalogue/category/books/travel_2/index.html",
        "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        "http://books.toscrape.com/catalogue/category/books/travel_2/index.html",
        "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
    ]
    tasks = [get_books_urls_from_category(url) for url in urls]
    res = await asyncio.gather(*tasks)
    print(res)
    end_time = time.time()
    print(f"⚡ Exécution : {end_time - start_time:.2f} sec")

asyncio.run(main())



