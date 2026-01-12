import psycopg
# from psycopg.rows import dict_row
import pytest
from helpers.file_helpers import API_SERIES_STATUS_TO_DB_MAPPING

@pytest.fixture
def add_episodes():
    # Настройки подключения к базе данных
    conn_params = {
        'dbname': 'my-shows-rating',
        'user': 'postgres',
        'password': '123456',
        'host': 'localhost',
        'port': '5432',
    }



    # Тестовые данные - на входе статус в API-значении
    test_series = [
        {"id": 6, "name": "Наруто", "photo": "https://media.myshows.me/shows/760/3/e8/3e8e697187b0fdb49941ecf22db5b9b3.jpg", "rating": 9, "status": "Смотрю","review": "Отличный сериал"},
        {"id": 7, "name": "Мандалорец", "photo": "https://media.myshows.me/shows/760/6/61/66124cb92abfa1ae993d66f2e80463fc.jpg", "rating": 9, "status": "Посмотрел", "review": "Эпично"},
        {"id": 8, "name": "Союз спасения. Время гнева", "photo": "https://media.myshows.me/shows/760/c/64/c6463ee65ae3aeaf071af0f502befc04.jpg", "rating": 8, "status": "Буду смотреть", "review": "Интересный сюжет"}
    ]


    with psycopg.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            # Очищаем полностью таблицу series
            cur.execute("DELETE FROM series;")
            # Вставляем тестовые данные с переводом статуса в базу
            for s in test_series:
                cur.execute("""
                     INSERT INTO series (id, name, photo, rating, status, review) 
                     VALUES (%s, %s, %s, %s, %s, %s);
                 """, (s["id"], s["name"], s["photo"], s["rating"], API_SERIES_STATUS_TO_DB_MAPPING[s["status"]],
                       s["review"]))
            conn.commit()
        yield test_series
        # После теста очищаем таблицу
        with conn.cursor() as cur:
            # cur.execute("DELETE FROM series;")
            conn.commit()