import requests
from typing import Dict

class APIManager:
   BASE_URL = 'https://api.hh.ru'

   @staticmethod
   def get_vacancies(employer_id: str) -> Dict:
       """Получает список вакансий для заданного работодателя по ID."""
       url = f'{APIManager.BASE_URL}/vacancies?employer_id={employer_id}&per_page=100'
       try:
           response = requests.get(url, timeout=10)  # Добавлен таймаут
           response.raise_for_status()  # Проверка на наличие ошибок
           print(f"Запрос к API выполнен: {url}")
           return response.json()
       except requests.exceptions.Timeout:
           print("Ошибки: превышено время ожидания запроса.")
       except requests.exceptions.RequestException as e:
           print(f"Ошибка при выполнении запроса: {e}")
           return {"items": [], "found": 0}  # Возвращаем пустой ответ в случае ошибки
