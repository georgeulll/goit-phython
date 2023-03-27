import json

import requests
from bs4 import BeautifulSoup

base_url = "http://quotes.toscrape.com"


def get_quote(web_urls: list):
    store_ = []
    for page_url in web_urls:
        response = requests.get(page_url)
        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.find_all("span", class_='text')
        authors = soup.find_all("small", class_="author")
        all_tags = soup.find_all('div', class_='tags')

        for i in range(len(quotes)):
            quote = quotes[i].text
            author = authors[i].text
            tags_for_quoter = all_tags[i].find_all('a', class_='tag')
            tags_ = [tag.text for tag in tags_for_quoter]
            store_.append(
                {'tags': tags_,
                 'author': author,
                 'quote': quote
                 }
            )
    return store_


urls = [base_url]


def get_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    next_page = soup.select('ul[class=pager] li[class=next] a')
    if next_page:
        new_prefix_url = next_page[0]['href']
        new_url = base_url+new_prefix_url
        urls.append(new_url)
        get_url(new_url)
    return urls


if __name__ == '__main__':
    u = get_url(base_url)
    data = get_quote(u)

    with open('quotes.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)