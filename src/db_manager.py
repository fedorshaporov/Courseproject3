import psycopg2
from psycopg2 import sql
from typing import List, Tuple, Dict

class DBManager:
    """Класс для работы с базой данных PostgreSQL."""

    def __init__(self, db_config: Dict[str, str]):
        """
        Инициализирует соединение с базой данных.

        :param db_config: Словарь с параметрами подключения к БД.
        """
        self.connection = psycopg2.connect(**db_config)

    def create_database(self, db_name: str) -> None:
        """
        Создает базу данных, если она не существует.

        :param db_name: Название базы данных.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql.SQL("SELECT 1 FROM pg_catalog.pg_database WHERE datname = {}").format(sql.Identifier(db_name)))
            exists = cursor.fetchone()
            if not exists:
                cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
                print(f"Database {db_name} created.")
            else:
                print(f"Database {db_name} already exists.")
        self.connection.commit()

    def create_tables(self) -> None:
        """Создает необходимые таблицы в базе данных."""
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employers (
                    id SERIAL PRIMARY KEY,
                    hh_id VARCHAR(100) NOT NULL UNIQUE,
                    name VARCHAR(255) NOT NULL
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    id SERIAL PRIMARY KEY,
                    employer_id INT REFERENCES employers(id),
                    title VARCHAR(255) NOT NULL,
                    salary_low INT,
                    salary_high INT,
                    link VARCHAR(255) NOT NULL
                );
            """)
            print("Tables created or already exist.")
        self.connection.commit()

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """Получает список всех компаний и количество вакансий у каждой компании."""
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT e.name, COUNT(v.id) 
                FROM employers e
                LEFT JOIN vacancies v ON e.id = v.employer_id 
                GROUP BY e.name
            """)
            return cursor.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, int, int, str]]:
        """Получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию."""
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT e.name, v.title, v.salary_low, v.salary_high, v.link 
                FROM vacancies v 
                JOIN employers e ON v.employer_id = e.id
            """)
            return cursor.fetchall()

    def get_avg_salary(self) -> float:
        """Получает среднюю зарплату по вакансиям."""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT AVG((salary_low + salary_high) / 2) FROM vacancies")
            return cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, str, int, int]]:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        avg_salary = self.get_avg_salary()
        with self.connection.cursor() as cursor:
            cursor.execute("""
                SELECT e.name, v.title, v.salary_low, v.salary_high 
                FROM vacancies v 
                JOIN employers e ON v.employer_id = e.id 
                WHERE (salary_low + salary_high) / 2 > %s
            """, (avg_salary,))
            return cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[str, str, int, int]]:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        with self.connection.cursor() as cursor:
            query = f"%{keyword}%"
            cursor.execute("""
                SELECT e.name, v.title, v.salary_low, v.salary_high 
                FROM vacancies v 
                JOIN employers e ON v.employer_id = e.id 
                WHERE v.title ILIKE %s
            """, (query,))
            return cursor.fetchall()

    def close(self) -> None:
        """Закрывает соединение с базой данных."""
        self.connection.close()