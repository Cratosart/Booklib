import requests
import os

path_books = 'Books'
path = os.makedirs(path_books, exist_ok=True)

for id in range (1,11):
    url = f'http://tululu.org/txt.php?id={id}'

    response = requests.get(url)
    response.raise_for_status()

    filename = f'id{id}.txt'
    with open(f'{path_books}/{filename}', 'wb') as file:
        file.write(response.content)