API_SERIES_STATUS_TO_DB_MAPPING = {
    "Смотрю": "watching",
    "Посмотрел": "watched",
    "Буду смотреть": "will_watch"
}

EXPECTED_SERIES = [
    {"name": "Тоннель",
     "photo": "https://media.myshows.me/shows/760/e/5a/e5a5fd3587da0300f44d530c323021d5.jpg",
     "rating": 9,
     "status": "Смотрю",
     "review": "Супер"},

    # {"name": "Берлинская жара",
    #  "photo": "https://media.myshows.me/shows/760/b/0c/b0ce3a94a79ec38d994a2d551b5e515f.jpg",
    #  "rating": 9,
    #  "status": "Посмотрел",
    #  "review": "Нечто"},
    #
    # {"name": "Странные дела",
    #  "photo": "https://media.myshows.me/shows/760/9/15/915b56d169568a7431e671770d426f60.jpg",
    #  "rating": 8,
    #  "status": "Буду смотреть",
    #  "review": "Держит в напряжении"}
]

FIELDS_TO_TEST = [
    ("name", "Наруто"),
    ("photo", "https://media.myshows.me/shows/760/3/e8/3e8e697187b0fdb49941ecf22db5b9b3.jpg"),
    ("rating", 9),
    ("status", "Смотрю"),
    ("review", "Отзыв")
]
