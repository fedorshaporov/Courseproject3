import os
from dotenv import load_dotenv
from api_manager import APIManager
from db_manager import DBManager
from vacancy_manager import VacancyManager

# Загружаем переменные окружения из .env файла
load_dotenv()

def main():
    db_config = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')
    }

    print(db_config)  # Для диагностики

    db_manager = DBManager(db_config)

    # Создание базы данных
    db_manager.create_database('databaseHH')

    # Создание таблиц
    db_manager.create_tables()

    api_manager = APIManager()
    vacancy_manager = VacancyManager(api_manager, db_manager)

    # Здесь список интересных компаний с актуальными ID
    employers_list = [
        {"name": "Яндекс", "id": "1740"},
        {"name": "Сбер", "id": "3529"},
        {"name": "Т-Банк", "id": "178638"},
        {"name": "Рускон", "id": "1068805"},
        {"name": "Пятерочка", "id": "1942330"},
        {"name": "Азбука вкуса", "id": "2120"},
        {"name": "Северсталь", "id": "6041"},
        {"name": "Адвирос", "id": "2765"},
        {"name": "ООО PepsiCo", "id": "581458"},
        {"name": "DPD в России", "id": "399"}
    ]

    # Заполнение базы данных
    vacancy_manager.populate_database(employers_list)

    # Получение данных
    companies_and_vacancies = db_manager.get_companies_and_vacancies_count()
    print("Компании и количество вакансий:", companies_and_vacancies)

    all_vacancies = db_manager.get_all_vacancies()
    print("Все вакансии:", all_vacancies)

    avg_salary = db_manager.get_avg_salary()
    print(f'Средняя зарплата: {avg_salary}')

    higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
    print("Вакансии с зарплатой выше средней:", higher_salary_vacancies)

    keyword_vacancies = db_manager.get_vacancies_with_keyword("Python")
    print("Вакансии по ключевому слову 'Python':", keyword_vacancies)

    db_manager.close()

if __name__ == "__main__":
    main()