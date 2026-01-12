import os


class Config:
    my_shows_postgres_db = "my-shows-rating"
    my_shows_postgres_user = os.getenv("MY_SHOWS_POSTGRES_USER")
    my_shows_postgres_password = os.getenv("MY_SHOWS_POSTGRES_PASSWORD")
    my_shows_postgres_host = "localhost"
    my_shows_postgres_port = 5432