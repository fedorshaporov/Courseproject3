from typing import List, Dict
import requests

class VacancyManager:
    """Класс для управления вакансиями и работодателями."""

    def __init__(self, api_manager: 'APIManager', db_manager: 'DBManager'):
        """
        Инициализирует менеджер вакансий.

        :param api_manager: Экземпляр класса APIManager для работы с API.
        :param db_manager: Экземпляр класса DBManager для работы с БД.
        """
        self.api_manager = api_manager
        self.db_manager = db_manager

    def populate_database(self, employers_list: List[Dict[str, str]]) -> None:
        """
        Заполняет базу данных данными о работодателях и их вакансиях.

        :param employers_list: Список работодателей с ID и именами.
        """
        for employer in employers_list:
            self.db_manager.insert_employer(employer['id'], employer['name'])
            data = self.api_manager.get_vacancies(employer['id'])
            for vacancy in data['items']:
                self.db_manager.insert_vacancy(
                    employer['id'],
                    vacancy['name'],
                    vacancy.get('salary', {}).get('from'),
                    vacancy.get('salary', {}).get('to'),
                    vacancy['alternate_url']
                )