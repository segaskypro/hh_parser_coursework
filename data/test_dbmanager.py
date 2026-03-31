from src.db_manager import DBManager

db = DBManager()

print("=== Компании и количество вакансий ===")
for company, count in db.get_companies_and_vacancies_count():
    print(f"  {company}: {count}")

print("\n=== Средняя зарплата ===")
print(f"  {int(db.get_avg_salary()):,} руб.")

print("\n=== Вакансии с зарплатой выше средней (первые 5) ===")
for company, name, salary, url in db.get_vacancies_with_higher_salary()[:5]:
    print(f"  {company} — {name} ({int(salary):,} руб.)")

print("\n=== Поиск вакансий с ключевым словом 'python' ===")
for company, name, salary, url in db.get_vacancies_with_keyword('python'):
    print(f"  {company} — {name}")

db.close()
