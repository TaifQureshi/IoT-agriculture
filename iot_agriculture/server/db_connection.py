from typing import Dict
import psycopg2
import logging

logger = logging.getLogger("db_connection")


class DbConnection(object):
    def __init__(self, db_config: Dict) -> None:
        self.db_config = db_config
        self.connection = None
        self.cursor = None

    def connect(self) -> bool:
        try:
            self.connection = psycopg2.connect(**self.db_config)
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            return True
        except Exception as e:
            logger.error(f"Timescale connection Error: {e}")
            return False

    def commit_query(self, query) ->bool:
        try:
            self.cursor.execute(query)
            return True
        except Exception as e:
            logger.error(f"PSQL commit_query failed: {query}")
            logger.error(f"PSQL commit_query Error: {e}")
            return False
