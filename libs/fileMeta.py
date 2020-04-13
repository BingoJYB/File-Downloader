import hashlib


class FileMetaData(object):
    def __init__(self, file_url='', date=None):
        self._file_url = file_url
        self._date = date

    @property
    def file_url(self):
        return self._file_url

    @file_url.setter
    def file_url(self, file_url):
        self._file_url = file_url

    @property
    def file_hash(self):
        return hash(self)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date

    def __hash__(self):
        file_hash = int(hashlib.sha1(self.file_url.encode(
            'utf-8')).hexdigest(), 16) % (10 ** 16)

        return file_hash

    def __repr__(self):
        return '''meta_data = (file_url = {file_url},
        file_hash = {file_hash},
        date = {date})
        '''.format(
            file_url=self.file_url,
            file_hash=self.file_hash,
            date=self.date
        )
