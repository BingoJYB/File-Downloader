import hashlib
import os
import sqlite3
from datetime import datetime

import requests
import urllib.request
from apscheduler.schedulers.blocking import BlockingScheduler
from bs4 import BeautifulSoup

from lib.defaults import BASE_URL, URL, DATE_FORMAT


def hash_for_file(file_url):
    file_hash = int(hashlib.sha1(file_url.encode(
        'utf-8')).hexdigest(), 16) % (10 ** 16)

    return file_hash


def create_table_if_not_exist(conn):
    conn.execute(
        '''
            CREATE TABLE IF NOT EXISTS DOCUMENT
            (
                URL    TEXT     PRIMARY KEY     NOT NULL,
                HASH   INT                      NOT NULL,
                DATE   TEXT
            );
        '''
    )


def check_file_update(conn, file_metadata):
    is_updated = False
    file_url = file_metadata['file_url']
    file_hash = file_metadata['file_hash']
    date = file_metadata['date']

    cursor = conn.execute('SELECT * FROM DOCUMENT')
    record = cursor.fetchone()

    if record:
        if record[2] != file_hash:
            conn.execute('UPDATE DOCUMENT SET URL=?, HASH=?, DATE=? WHERE ROWID=1',
                         (file_url, file_hash, date))
            conn.commit()
            is_updated = True
    else:
        conn.execute('INSERT INTO DOCUMENT (URL, HASH, DATE) VALUES(?,?,?)',
                     (file_url, file_hash, date))
        conn.commit()
        is_updated = True

    return is_updated


def get_file_metadata():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    div = soup.find('div', {'class': 'linkItem info 2'})
    first_a_tag = div.find("a", recursive=False)
    link = first_a_tag['href']

    file_url = BASE_URL + link
    file_hash = hash_for_file(file_url)
    date = datetime.now().strftime(DATE_FORMAT)

    return file_url, file_hash, date


def download_file(file_url, date):
    _, file_extension = os.path.splitext(file_url)
    urllib.request.urlretrieve(
        file_url, 'download_files/' + date + file_extension)


if __name__ == '__main__':

    file_url, file_hash, date = get_file_metadata()

    file_metadata = dict(
        file_url=file_url,
        file_hash=file_hash,
        date=date
    )

    conn = sqlite3.connect('app.db')
    create_table_if_not_exist(conn)

    if check_file_update(conn, file_metadata):
        download_file(file_url, date)

    conn.close()
