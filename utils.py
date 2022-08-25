from bs4 import BeautifulSoup
from threading import Thread
import requests

def parse_cities(link : str) -> None:
    cities = list()

    source = requests.get(link)
    soup = BeautifulSoup(source.text, 'lxml')  

    for item in soup.find_all('a'):
        if item is not None:
            cities.append(item)

