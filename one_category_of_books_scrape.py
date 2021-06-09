# import libraries
import requests
import csv 
import re
from bs4 import BeautifulSoup

# variable that checks if category has multiple pages
additional_pages = True

# category url to scrape book data from
category_url = "http://books.toscrape.com/catalogue/category/books/default_15/index.html"

# variable to keep track of the current page
category_url_additional_page_count = 1

# list that stores all book urls
book_urls = []

# looping through each page of the category
while(additional_pages): 
    page = requests.get(category_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    soup_string = str(soup.find_all("h3"))
    book_urls.append(soup_string)
    category_url_additional_page_count+= 1
    category_url_additional_page_count_str = str(category_url_additional_page_count)
    category_url = "http://books.toscrape.com/catalogue/category/books/default_15/page-" + category_url_additional_page_count_str + ".html"
    r = requests.get(category_url)
    if(r.status_code != 200):
        additional_pages = False

# replacing book shortcut url with full url
book_urls = [w.replace('../../../', 'http://books.toscrape.com/catalogue/') for w in book_urls]

# extracting urls only
book_urls = [re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', str(book_urls))]

# changing list to string
str_book_lists = ','.join(book_urls[0])

# creating a list of all urls from the category
my_urls = str_book_lists.split(",")

# open csv file and write headings
f = csv.writer(open('csv_files/one_category_of_books_scrape.csv', 'w', encoding="utf-8"))
f.writerow(["url", 'universal_product_code', 'title', 'price_including_tax','price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url'])

# scape data and write to csv file for each book
for x in my_urls:
    book_url = x
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
    f.writerow([url, universal_product_code, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url])