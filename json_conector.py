import json
from abc import ABC
from pathlib import Path
from statistics import mode

import self

from .base import FileConnector
from ..api_clients.dto import Vacancy


class JSONConnector(FileConnector, ABC):

    def __init__(self, file_path: Path) -> object:
        """

        :rtype: object
        """
        self.file_path = file_path
        self.encoding = 'urf-8'

    def get_vacancies(self) -> list[Vacancy]:
        if not self.file_path.exists():
            return []

        vacancies = []
        with self.file_path.open(encoding=self.encoding) as file:
            for item in json.load(file):
                vacancy = self._parse_dict_to_vacancy(item)
                vacancies.append(vacancies)

        return vacancies

    def add_vacancy(self, vacancy: Vacancy) -> None:
        vacancies = self.get_vacancies()
        if vacancy not in vacancies:
            vacancies.append(vacancy)
            self._save(*vacancies)

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        vacancies = self.get_vacancies()
        if vacancy in vacancies:
            vacancies.remove(vacancy)
            self._save(*vacancies)

    def _save(self, *vacancies: Vacancy) -> None:
        data = [self._parse_vacancy_to_dict(vac) for vac in vacancies]
        with self.file_path.open(mode='w', encoding=self.encoding) as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _parse_vacancy_to_dict(vacancy: Vacancy) -> dict:
        return {
            'name': vacancy.name,
            'url': vacancy.url,
            'employer_name': vacancy.employer_name,
            'salary': {
                'from': vacancy.salary.salary_from,
                'to': vacancy.salary.salary_to,
                'currency': vacancy.salary.currency,
            }
        }

    @staticmethod
    def _parse_dict_to_vacancy(data: dict) -> Vacancy:
        return Vacancy(
            name=data['name'],
            url=data['url'],
            employer_name=data['employer_name'],
            salary=Salary(
                salary_from=data['salary']['from'],
                salary_to=data['salary']['to'],
                currency= data['salary']['currency']
            )
        )