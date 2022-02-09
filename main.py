import os
import requests
import urllib.parse
import argparse
import sys

from os.path import splitext
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin


def createparser ():
    parser = argparse.ArgumentParser()
    parser.add_argument('start_id', nargs='?', default=1, type=int)
    parser.add_argument('end_id', nargs='?', default=10, type=int)
    return parser


def download_txt(url_book, identifier, url_content):
    payload = {
            'id': {identifier}
        }
    book = requests.get(url_book, params=payload)
    book.raise_for_status()
    for redirect in book.history:
        if not redirect == []:
            return
    book_author, book_name = parse_book_page(url_content)
    save_book(book.content, book_name, identifier)
    get_comment(url_content)
    download_image(url_content)


def download_image(url_content):
    response = requests.get(url_content)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    img_book = (soup.find('div', class_='bookimage').find('img')['src'])
    url_img = urllib.parse.urlsplit(img_book)
    split_url = splitext(url_img.path)
    extension = split_url[1]
    path_url_img = urljoin(url_content, img_book)
    path_img_books = 'images'
    os.makedirs(path_img_books, exist_ok=True)
    filename = f'{identifier}{extension}'
    img = requests.get(path_url_img)
    save_path = os.path.join(path_img_books, filename)
    with open(save_path, 'wb') as file:
        file.write(img.content)


def get_comment(url_content):
    response = requests.get(url_content)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    comment_text = (soup.find_all('span', class_='black'))
    if comment_text:
        for comment in comment_text:
            print(comment.text)
    book_genre = (soup.find('span', class_='d_book'))
    print(book_genre.text)

def save_book(content, book_name, identifier):
    path_books = 'Books'
    os.makedirs(path_books, exist_ok=True)
    filename = f'{identifier}. {book_name}.txt'
    save_path = os.path.join(path_books, filename)
    with open(f'{save_path}', 'wb') as file:
        file.write(content)


def parse_book_page(url_content):
    response = requests.get(url_content)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = (soup.find('body').find('h1'))
    title_text = title_tag.text
    info_book = title_text.split('::')
    name_book = info_book[0].strip()
    name_book = f'{sanitize_filename(name_book)}'
    book_author = info_book[1].strip()
    return book_author, name_book



if __name__ == '__main__':
    parser = createparser()
    args = parser.parse_args(sys.argv[1:])
    url_book = 'http://tululu.org/txt.php'
    url_content = 'https://tululu.org/b'
    for identifier in range(args.start_id, args.end_id+1):
        # loading_book_content(url_book, id)
        url_content = f'https://tululu.org/b{identifier}/'
        download_txt(url_book, identifier, url_content)