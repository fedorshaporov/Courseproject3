from api_manager import APIManager
from db_manager import DBManager
from vacancy_manager import VacancyManager

def main():
    db_config = {
        'dbname': 'databaseHH',
        'password': '0608',
        'host': 'localhost',
        'port': '5432'
    }

    db_manager = DBManager(db_config)

    # Создание базы данных
    db_manager.create_database('databaseHH')  # Замените на ваше название БД

    # Создание таблиц
    db_manager.create_tables()

    api_manager = APIManager()
    vacancy_manager = VacancyManager(api_manager, db_manager)

    # Пример интересных компаний
    employers_list = [
        {"name": "Компания A", "id": "123456"},
        {"name": "Компания B", "id": "234567"},
        {"name": "Компания C", "id": "345678"},
        {"name": "Компания D", "id": "456789"},
        {"name": "Компания E", "id": "567890"},
        {"name": "Компания F", "id": "678901"},
        {"name": "Компания G", "id": "789012"},
        {"name": "Компания H", "id": "890123"},
        {"name": "Компания I", "id": "901234"},
        {"name": "Компания J", "id": "012345"},
    ]

    # Заполнение базы данных
    vacancy_manager.populate_database(employers_list)

    # Получение данных
    companies_and_vacancies = db_manager.get_companies_and_vacancies_count()
    print(companies_and_vacancies)

    all_vacancies = db_manager.get_all_vacancies()
    print(all_vacancies)

    avg_salary = db_manager.get_avg_salary()
    print(f'Average Salary: {avg_salary}')

    higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
    print(higher_salary_vacancies)

    keyword_vacancies = db_manager.get_vacancies_with_keyword("Python")
    print(keyword_vacancies)

    db_manager.close()

if __name__ == "__main__":
    main()
