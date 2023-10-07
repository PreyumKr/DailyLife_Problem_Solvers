# python script to generate colouring pages
# Just add the sceapeops.io API keys and it will generate colouring pages according to the instructions given.
from pathlib import Path

import requests
import csv
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).parent
READY = BASE_DIR / 'ready'

API_KEY = ''  # add scrapeops.io api key here

titles = []

keys = ['adult coloring book for men fishing', ]  # add the keyphrases for parsing here.


def write_csv(data):

    name = ','.join(keys)

    if len(name) > 100:
        name = name[:100]

    with open(f'{READY}/{name}.csv', 'a') as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        writer.writerow(data)


def get_html(url):
    response = requests.get(
      url='https://proxy.scrapeops.io/v1/',
      params={
          'api_key': API_KEY,
          'url': url,

      },
    )
    response.encoding = 'utf-8'

    return response.text


def main():
    for elem in keys:
        url = 'https://www.amazon.com/s?k=' + elem.replace(' ', '+')

        print(f'Parsing titles for the key phrase "{elem}"\n'
              f'Link: {url}')

        html = get_html(url)

        soup = BeautifulSoup(html, 'lxml')

        block = soup.select('div[cel_widget_id*="MAIN-SEARCH_RESULTS"]')

        for i in block:
            title = i.find('h2').text
            data = {'title': title,
                    }

            if title not in titles:
                titles.append(title)

                write_csv(data)

        print(f'{len(block)} titles are written in the CSV file (ready folder)')


if __name__ == '__main__':
    if not API_KEY:
        print('Register a free account on scrapeops.io, copy the API key,\n'
              'and assign it to the string constant API_KEY in the main.py file')
    else:
        main()
