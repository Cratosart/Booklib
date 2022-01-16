# # coding: UTF-8
import os
import requests

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def check_for_redirect(book):
    print('Ошибка')


def loading_book_content(url, id):
        payload = {
            'id': {id}
        }
        book = requests.get(url, params=payload)
        book.raise_for_status()
        if book.history == []:
            try:
                url = f'https://tululu.org/b{id}/'
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'lxml')
                title_tag = (soup.find('body').find('h1'))

                title_text = title_tag.text
                info_book = title_text.split('::')
                name_book = info_book[0].strip()
                name_book = f'{sanitize_filename(name_book)}'
                book_author = info_book[1].strip()
                download_txt(book.content, name_book, id)
                return name_book
            except:
                check_for_redirect(book)


def download_txt(content, name_book, id):
    path_books = 'Books'
    os.makedirs(path_books, exist_ok=True)
    filename = f'{id}. {name_book}.txt'
    save_path = os.path.join(path_books, filename)
    with open(f'{save_path}', 'wb') as file:
        file.write(content)



if __name__ == '__main__':
    url_book = 'http://tululu.org/txt.php'
    for id in range(1,11):
        loading_book_content(url_book, id)

