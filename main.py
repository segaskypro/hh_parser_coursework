from src.api_hh import HHAPI
from src.db_utils import create_database, create_tables, save_companies_to_db, save_vacancies_to_db
from src.db_manager import DBManager

EMPLOYER_IDS = [1740, 3529, 39305, 80, 15478, 3776, 2748, 3127, 907345, 2381]


def main():
    print("=" * 50)
    print("КУРСОВАЯ РАБОТА: Парсер вакансий с hh.ru")
    print("=" * 50)

    print("\n1. Создание базы данных и таблиц...")
    create_database()
    create_tables()

    print("\n2. Получение данных с hh.ru...")
    api = HHAPI(EMPLOYER_IDS)
    companies, vacancies = api.load_all_data()

    print("\n3. Сохранение данных в базу...")
    save_companies_to_db(companies)
    save_vacancies_to_db(vacancies)

    print("\n4. Анализ данных:")
    print("-" * 40)

    db = DBManager()

    print("\nКомпании и количество вакансий:")
    for company, count in db.get_companies_and_vacancies_count():
        print(f"  • {company}: {count}")

    avg_salary = db.get_avg_salary()
    print(f"\nСредняя зарплата: {int(avg_salary):,} руб.")

    print("\nВакансии с зарплатой выше средней (первые 5):")
    for company, name, salary, url in db.get_vacancies_with_higher_salary()[:5]:
        print(f"  • {company} — {name} ({int(salary):,} руб.)")

    keyword = input("\nВведите ключевое слово для поиска вакансий: ")
    if keyword:
        results = db.get_vacancies_with_keyword(keyword)
        print(f"\nНайдено вакансий со словом '{keyword}': {len(results)}")
        for company, name, salary, url in results[:10]:
            print(f"  • {company} — {name}")

    db.close()

    print("\n" + "=" * 50)
    print("Работа завершена!")
    print("=" * 50)


if __name__ == "__main__":
    main()