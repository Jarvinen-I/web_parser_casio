import ssl
import os
import lxml
import urllib.request
import time
import json
import csv
from bs4 import BeautifulSoup
from datetime import datetime


def get_all_pages():
    ssl._create_default_https_context = ssl._create_unverified_context

    resp = urllib.request.urlopen('https://shop.casio.ru/catalog/g-shock/')
    soup = BeautifulSoup(resp, 'lxml')

    if not os.path.exists('data'):
        os.mkdir('data')

    with open('data/page_1.html', 'w', encoding='utf-8') as file:
        file.write(str(soup))

    with open('data/page_1.html', 'r', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    pages_count = int(soup.find('div', class_='bx-pagination-container').find_all('a')[-2].text)

    for i in range(1, pages_count + 1):
        url = f'https://shop.casio.ru/catalog/g-shock/?PAGEN_1={i}'

        req = urllib.request.urlopen(url)
        soup = BeautifulSoup(req, 'lxml')

        with open(f'data/page_{i}.html', 'w', encoding='utf-8') as file:
            file.write(str(soup))

        time.sleep(2)

    return pages_count + 1


def collect_data(pages_count):
    current_date = datetime.now().strftime('%d_%m_%Y')
    data = []

    with open(f'data_{current_date}.csv', 'w', encoding='utf-8-sig') as csv_file:
        writer = csv.writer(csv_file, delimiter=';', lineterminator='\n')

        writer.writerow(
            (
                'Артикул',
                'Ссылка'
            )
        )

    for page in range(1, pages_count):
        with open(f'data/page_{page}.html', 'r', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        items_cards = soup.find_all('a', class_='product-item__link')

        for item in items_cards:
            product_article = item.find('p', class_='product-item__articul').text.strip()
            product_url = 'https://shop.casio.ru' + item.get('href')

            data.append(
                {
                    'product_article': product_article,
                    'product_url': product_url
                }
            )

            with open(f'data_{current_date}.csv', 'a', encoding='utf-8-sig') as csv_file:
                writer = csv.writer(csv_file, delimiter=';', lineterminator='\n')

                writer.writerow(
                    (
                        product_article,
                        product_url
                    )
                )

    with open(f'data_{current_date}.json', 'a', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)



def main():
    pages_count = get_all_pages()
    collect_data(pages_count=pages_count)


if __name__ == '__main__':
    main()
