from api_manager import APIManager
from db_manager import DBManager
from typing import List, Dict

class VacancyManager:
    """Класс для управления вакансиями и работодателями."""

    def __init__(self, api_manager: APIManager, db_manager: DBManager):
        """
        Инициализирует менеджер вакансий.

        :param api_manager: Экземпляр класса APIManager для работы с API.
        :param db_manager: Экземпляр класса DBManager для работы с БД.
        """
        self.api_manager = api_manager
        self.db_manager = db_manager

    def populate_database(self, employers_list: List[Dict[str, str]]) -> None:
        """Заполняет базу данных данными о работодателях и их вакансиях."""
        for employer in employers_list:
            self.db_manager.insert_employer(employer['id'], employer['name'])
            data = self.api_manager.get_vacancies(employer['id'])
            print(f"Данные о вакансиях для {employer['name']}: {data}")  # Отладочная информация

            # Проходим по всем вакансиям
            for vacancy in data.get('items', []):
                if vacancy:  # Проверяем, что vacancy не равен None
                    salary_low = vacancy.get('salary', {}).get('from')  # Значение по умолчанию - None
                    salary_high = vacancy.get('salary', {}).get('to')  # Значение по умолчанию - None

                    self.db_manager.insert_vacancy(
                        employer['id'],
                        vacancy['name'],
                        salary_low,
                        salary_high,
                        vacancy.get('alternate_url')
                    )
                else:
                    print(f"Ошибка: вакансия недоступна для работодателя {employer['name']}.")