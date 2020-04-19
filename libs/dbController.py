import logging
import os
import sqlite3

from libs.logger import Logger
from libs.defaults import ROOT_DIR

logger = Logger('dbController', level=logging.INFO).logger

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
        try:
            db = os.path.join(ROOT_DIR, 'app.db')
            self._conn = sqlite3.connect(db)
            self.create_table_if_not_exist()
        except Exception as err:
            logger.error(f"Database failed to be connected: {err}")
        finally:
            self.close_db()

    def close_db(self):
        self._conn.close()

    def create_table_if_not_exist(self):
        self._conn.execute(CREATE_TABLE_IF_NOT_EXIST)

    def check_file_update(self, file_metadata):
        is_updated = False
        file_url = file_metadata.file_url
        file_hash = file_metadata.file_hash
        date = file_metadata.date

        try:
            cursor = self._conn.execute('SELECT * FROM DOCUMENT')
            record = cursor.fetchone()
        except Exception as err:
            logger.error(f"Database querying failed: {err}")
            return False

        if record:
            if record[1] != file_hash:
                try:
                    self._conn.execute('UPDATE DOCUMENT SET URL=?, HASH=?, DATE=? WHERE ROWID=1',
                                       (file_url, file_hash, date))
                    self._conn.commit()
                    is_updated = True
                except Exception as err:
                    logger.error(f"Database updating failed: {err}")
                    return False
        else:
            try:
                self._conn.execute('INSERT INTO DOCUMENT (URL, HASH, DATE) VALUES(?,?,?)',
                                   (file_url, file_hash, date))
                self._conn.commit()
                is_updated = True
            except Exception as err:
                logger.error(f"Database inserting failed: {err}")
                return False

        return is_updated
