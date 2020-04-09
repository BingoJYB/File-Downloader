import requests
import urllib.request
from bs4 import BeautifulSoup

BASE_URL = 'https://www.deutsche-boerse.com'
URL = 'https://www.deutsche-boerse.com/dbg-en/investor-relations/statistics'


def download_file():

    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    div = soup.find('div', {'class': 'linkItem info 2'})
    first_a_tag = div.find("a", recursive=False)
    link = first_a_tag['href']

    download_url = BASE_URL + link
    urllib.request.urlretrieve(
        download_url, 'download_files/' + link[link.find('/major') + 1:])


if __name__ == '__main__':
    download_file()
