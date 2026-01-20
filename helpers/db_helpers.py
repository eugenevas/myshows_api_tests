import psycopg
from psycopg.rows import dict_row
from config.bd_config import Config


class DbConnection:
    def __init__(self, config: Config):
        self.dbname = config.my_shows_postgres_db
        self.user = config.my_shows_postgres_user
        self.password = config.my_shows_postgres_password
        self.host = config.my_shows_postgres_host
        self.port = config.my_shows_postgres_port
        self.connection = None


    def execute(self, sql, params=None):
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql)
        except Exception as err:
            self.connection.rollback()
            print(err)
            raise
        else:
            self.connection.commit()
            return cursor


    def executemany(self, sql):
        cursor = self.connection.cursor()
        try:
            cursor.executemany(sql)
        except Exception as err:
            print(err)
        else:
            self.connection.commit()


    def __enter__(self):
        try:
            self.connection = psycopg.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                row_factory=dict_row,
                connect_timeout=5,
            )
            return self
        except Exception as e:
            print(f"Database connection error: {e}")
            raise


    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()