# import libraries
import requests
import csv 
from bs4 import BeautifulSoup

# book url to scrape from
book_url = "http://books.toscrape.com/catalogue/walt-disneys-alice-in-wonderland_777/index.html"
page = requests.get(book_url)

# open csv file and write headings
f = csv.writer(open('csv_files/one_book_scrape.csv', 'w'))
f.writerow(["url", 'universal_product_code', 'title', 'price_including_tax','price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])

# scape data 
book_url = book_url
page = requests.get(book_url)
soup = BeautifulSoup(page.content, 'html.parser')
url = book_url
universal_product_code = soup.find('table', class_='table table-striped').find_all('td')[0].text
title = soup.find('h1').text
price_including_tax = soup.find('table', class_='table table-striped').find_all('td')[2].text
price_excluding_tax = soup.find('table', class_='table table-striped').find_all('td')[3].text
number_available = soup.find('table', class_='table table-striped').find_all('td')[5].text
product_description = ""
for meta in soup.findAll("meta"):
    metaname = meta.get('name', '').lower()
    metaprop = meta.get('property', '').lower()
    if 'description' == metaname or metaprop.find("description")>0:
        product_description = meta['content'].strip()
category = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()
review_rating = soup.find('div', class_='col-sm-6 product_main').find_all('p')[2]['class'][1]
image_url = soup.find('img')
image_url = image_url['src']
image_url = image_url.replace('../..', 'http://books.toscrape.com/')

# write scaped data to csv file
f.writerow([url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url])
