import logging
import os
import sqlite3

from libs.logger import Logger
from libs.defaults import ROOT_DIR

logger = Logger('dbController', level=logging.INFO).logger

# Query statement for creating table in database
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
        """
            Connect to the database and try to create the database table
        """

        try:
            db = os.path.join(ROOT_DIR, 'app.db')
            self._conn = sqlite3.connect(db)
            self.create_table_if_not_exist()
        except Exception as err:
            self.close_db()
            logger.error(f"Database failed to be connected: {err}")
            logger.info(f"Close database")

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
            # Query the database and ge the first record
            cursor = self._conn.execute('SELECT * FROM DOCUMENT')
            record = cursor.fetchone()
        except Exception as err:
            logger.error(f"Database querying failed: {err}")
            return False

        if record:
            # If hash changed, update the record in database and
            # mark indicator as true
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
            # If this is the first time downloading file,
            # add one record with metadata to database
            try:
                self._conn.execute('INSERT INTO DOCUMENT (URL, HASH, DATE) VALUES(?,?,?)',
                                   (file_url, file_hash, date))
                self._conn.commit()
                is_updated = True
            except Exception as err:
                logger.error(f"Database inserting failed: {err}")
                return False

        return is_updated
