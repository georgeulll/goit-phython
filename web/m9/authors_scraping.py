import json

import requests
from bs4 import BeautifulSoup

from scraping_qoutes import get_url

base_url = "http://quotes.toscrape.com"


def get_author(urls: list):
    store_ = []
    for web_url in urls:
        response = requests.get(web_url)
        soup = BeautifulSoup(response.text, "lxml")

        author_data = soup.select('div[class=author-details]')
        a_name = author_data[0].find('h3', class_='author-title')
        a_born_date = author_data[0].find('span', class_='author-born-date')
        a_born_location = author_data[0].find('span', class_='author-born-location')
        a_description = author_data[0].find('div', class_='author-description')
        store_.append(
            {'fullname': a_name.text.strip(),
             'born_date': a_born_date.text.strip(),
             'born_location': a_born_location.text.strip(),
             'description': a_description.text.strip()
             }
        )
    return store_


def get_author_url():
    url_author = []
    urls_pages = get_url(base_url)
    for url in urls_pages:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        author_link = soup.select('span a ')
        for i in range(10):
            url_link = base_url + author_link[i]['href']
            if url_link in url_author:
                continue
            else:
                url_author.append(url_link)
    return url_author


if __name__ == '__main__':
    author_urls = get_author_url()
    data = get_author(author_urls)

    with open('authors.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)