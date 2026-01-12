from dotenv import load_dotenv
load_dotenv() # эти две строки нужны чтобы подгрузился перед тестами файл .env иначе не находит его автоматом

pytest_plugins = ["fixtures.api_fixtures"]
