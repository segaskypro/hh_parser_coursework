from typing import List, Dict, Any
import psycopg2
from src.config import Config


def create_database() -> None:
    """Создаёт базу данных, если она не существует."""
    conn = psycopg2.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database='postgres'
    )
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (Config.DB_NAME,))
    if not cur.fetchone():
        cur.execute(f"CREATE DATABASE {Config.DB_NAME}")
        print(f"База данных {Config.DB_NAME} создана")
    else:
        print(f"База данных {Config.DB_NAME} уже существует")

    cur.close()
    conn.close()


def create_tables() -> None:
    """Создаёт таблицы companies и vacancies, если они не существуют."""
    conn = psycopg2.connect(Config.get_db_url())
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            url VARCHAR(255)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS vacancies (
            id INTEGER PRIMARY KEY,
            company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
            name VARCHAR(255) NOT NULL,
            salary_from INTEGER,
            salary_to INTEGER,
            currency VARCHAR(10),
            url VARCHAR(255),
            requirement TEXT
        )
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Таблицы созданы")


def save_companies_to_db(companies: List[Dict[str, Any]]) -> None:
    """Сохраняет список компаний в базу данных.

    Args:
        companies: Список словарей с данными компаний
    """
    conn = psycopg2.connect(Config.get_db_url())
    cur = conn.cursor()

    for company in companies:
        cur.execute("""
            INSERT INTO companies (id, name, description, url)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (
            company['id'],
            company['name'],
            company.get('description', ''),
            company.get('site_url', '')
        ))

    conn.commit()
    cur.close()
    conn.close()
    print(f"Сохранено компаний: {len(companies)}")


def save_vacancies_to_db(vacancies: List[Dict[str, Any]]) -> None:
    """Сохраняет список вакансий в базу данных.

    Args:
        vacancies: Список словарей с данными вакансий
    """
    conn = psycopg2.connect(Config.get_db_url())
    cur = conn.cursor()

    count = 0
    for vac in vacancies:
        salary = vac.get('salary')
        salary_from = salary.get('from') if salary else None
        salary_to = salary.get('to') if salary else None
        currency = salary.get('currency') if salary else None
        requirement = vac.get('snippet', {}).get('requirement', '')

        if requirement and len(requirement) > 500:
            requirement = requirement[:500]

        try:
            cur.execute("""
                INSERT INTO vacancies (id, company_id, name, salary_from, salary_to, currency, url, requirement)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (
                vac['id'],
                vac['employer']['id'],
                vac['name'],
                salary_from,
                salary_to,
                currency,
                vac.get('alternate_url', ''),
                requirement
            ))
            count += 1
        except Exception:
            pass

    conn.commit()
    cur.close()
    conn.close()
    print(f"Сохранено вакансий: {count}")