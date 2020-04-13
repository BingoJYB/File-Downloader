import os
from datetime import datetime
from pathlib import Path

import requests
import urllib.request
from bs4 import BeautifulSoup

from libs.defaults import BASE_URL, URL, DATE_FORMAT, DOWNLOAD_PATH


class FileScraper(object):
    def __init__(self):
        self.response = requests.get(URL)
        self.soup = BeautifulSoup(self.response.text, 'html.parser')

    def get_file_metadata(self):
        div = self.soup.find('div', {'class': 'linkItem info 2'})
        first_a_tag = div.find("a", recursive=False)
        link = first_a_tag['href']

        download_url = BASE_URL + link
        download_date = datetime.now().strftime(DATE_FORMAT)

        return download_url, download_date

    def download_file(self, file_metadata):
        _, file_extension = os.path.splitext(file_metadata.file_url)
        Path(DOWNLOAD_PATH).mkdir(parents=True, exist_ok=True)

        urllib.request.urlretrieve(
            file_metadata.file_url,
            DOWNLOAD_PATH + file_metadata.date + file_extension)
