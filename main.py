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


def loading_book_content(url, id):
    payload = {
        'id': {id}
    }
    book = requests.get(url, params=payload)
    book.raise_for_status()
    if book.history == []:
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
        img_book = (soup.find('div', class_='bookimage').find('img')['src'])
        url_img = urllib.parse.urlsplit(img_book)
        split_url = splitext(url_img.path)
        extension = split_url[1]
        path_url_img = urljoin(url, img_book)
        download_image(path_url_img, id, extension, book.content)
        parse_book_page(soup)



def download_txt(content, name_book, id):
    path_books = 'Books'
    os.makedirs(path_books, exist_ok=True)
    filename = f'{id}. {name_book}.txt'
    save_path = os.path.join(path_books, filename)
    with open(f'{save_path}', 'wb') as file:
        file.write(content)


def download_image(path_url_img, id, extension, content):
    path_img_books = 'images'
    os.makedirs(path_img_books, exist_ok=True)
    filename = f'{id}{extension}'
    img = requests.get(path_url_img)
    save_path = os.path.join(path_img_books, filename)
    with open(save_path, 'wb') as file:
        file.write(img.content)


def parse_book_page(soup):
    title_tag = (soup.find('body').find('h1'))
    title_text = title_tag.text
    info_book = title_text.split('::')
    name_book = info_book[0].strip()
    name_book = f'{sanitize_filename(name_book)}'
    print(name_book)
    book_author = info_book[1].strip()
    print(book_author)
    comment_text = (soup.find_all('span', class_='black'))
    if comment_text:
        for comment in comment_text:
            print(comment.text)
    book_genre = (soup.find('span', class_='d_book'))
    print(book_genre.text)




if __name__ == '__main__':
    parser = createparser()
    args = parser.parse_args(sys.argv[1:])
    url_book = 'http://tululu.org/txt.php'
    for id_books in range(args.start_id, args.end_id+1):
        loading_book_content(url_book, id_books)


