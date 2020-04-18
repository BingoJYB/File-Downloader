import csv
import logging
import os
from datetime import datetime
from pathlib import Path

import requests
import urllib.request
from bs4 import BeautifulSoup

from libs.defaults import BASE_URL
from libs.defaults import URL
from libs.defaults import DATE_FORMAT
from libs.defaults import DOWNLOAD_PATH

logger = logging.getLogger("fileScraper")
logger.setLevel(logging.INFO)
c_handler = logging.FileHandler('app.log')
c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)


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

        try:
            download_path = self.parse_config_file()
        except Exception as err:
            logger.error(f"Load download path with: {err}")
            logger.error(f"Use default path {DOWNLOAD_PATH}")
            download_path = DOWNLOAD_PATH

        if download_path is None:
            download_path = DOWNLOAD_PATH
            logger.info(f"Use default path {DOWNLOAD_PATH}")

        Path(download_path).mkdir(parents=True, exist_ok=True)

        urllib.request.urlretrieve(
            file_metadata.file_url,
            download_path + file_metadata.date + file_extension)

    def parse_config_file(self, csv_path='config.csv'):
        with open(csv_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0

            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                else:
                    return row[0]

        return
