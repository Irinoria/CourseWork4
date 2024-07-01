from pathlib import Path

from src.api_clients import HeadHunterAPI
from src.api_clients.base import VacancyApiClient
from src.file_connector import JSONConnector
from src.file_connector.base import FileConnector

BASE_PATH = Path(__file__).parent
VACANCIES_PATH_FILE = BASE_PATH.joinpath('vacancies.json')

api_client: VacancyApiClient = HeadHunterAPI()
json_connector: FileConnector = JSONConnector(VACANCIES_PATH_FILE)


welcome_message = """
    Добро пожаловать в программу, выберите действия:
    1. Загрузить вакансии в файл по ключевому слову
    2. Вывести топ 10 вакансий из файла
    0. Выйти
    """


def main():
    while True:
        print(welcome_message)
        user_input = input()
        if not user_input.isdigit():
            continue

        user_choice = int(user_input)

        if user_choice == 1:
            search_word = input('Введите ключевое слово для поиска:')
            vacancies = api_client.get_vacancies(search_word.lower())
            for vac in vacancies:
                json_connector.add_vacancy(vac)
        elif user_choice == 2:
            vacancies = json_connector.get_vacancies()
            for vac in sorted(vacancies, key=lambda x: x.salary, reverse=True)[:10]:
                print(vac)
        elif user_choice == 0:
            break


if __name__ == '__main__':
    main()
