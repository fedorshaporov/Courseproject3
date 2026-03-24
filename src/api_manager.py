import requests
from typing import Dict, List

class APIManager:
    """Класс для взаимодействия с API hh.ru для получения вакансий."""

    BASE_URL = 'https://api.hh.ru'

    @staticmethod
    def get_vacancies(employer_id: str) -> Dict:
        """
        Получает список вакансий для заданного работодателя по ID.

        :param employer_id: ID работодателя в API.
        :return: Словарь с данными о вакансиях.
        """
        url = f'{APIManager.BASE_URL}/vacancies?employer_id={employer_id}&per_page=100'
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки
        return response.json()
