import sqlite3


CREATE_TABLE_IF_NOT_EXIST = '''
                            CREATE TABLE IF NOT EXISTS DOCUMENT
                            (
                                URL    TEXT     PRIMARY KEY     NOT NULL,
                                HASH   INT                      NOT NULL,
                                DATE   TEXT
                            );
                            '''


class DBController(object):
    def __init__(self):
        self._conn = sqlite3.connect('app.db')
        self.create_table_if_not_exist()

    def get_conn_instance(self):
        return self._conn

    def close_db(self):
        self._conn.close()

    def create_table_if_not_exist(self):
        self._conn.execute(CREATE_TABLE_IF_NOT_EXIST)

    def check_file_update(self, file_metadata):
        is_updated = False
        file_url = file_metadata.file_url
        file_hash = file_metadata.file_hash
        date = file_metadata.date

        cursor = self._conn.execute('SELECT * FROM DOCUMENT')
        record = cursor.fetchone()

        if record:
            if record[2] != file_hash:
                self._conn.execute('UPDATE DOCUMENT SET URL=?, HASH=?, DATE=? WHERE ROWID=1',
                                   (file_url, file_hash, date))
                self._conn.commit()
                is_updated = True
        else:
            self._conn.execute('INSERT INTO DOCUMENT (URL, HASH, DATE) VALUES(?,?,?)',
                               (file_url, file_hash, date))
            self._conn.commit()
            is_updated = True

        return is_updated
