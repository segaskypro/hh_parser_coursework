import psycopg2
import requests
import time

# Подключаемся к БД
conn = psycopg2.connect(
    host='localhost',
    port='5432',
    database='hh_project',
    user='postgres',
    password='1234'
)
cur = conn.cursor()

# Получаем список компаний из БД
cur.execute("SELECT id FROM companies")
companies = cur.fetchall()

vacancy_count = 0

for (company_id,) in companies:
    print(f"Загружаем вакансии для компании ID {company_id}...")
    
    # Получаем вакансии с hh.ru
    url = "https://api.hh.ru/vacancies"
    params = {
        'employer_id': company_id,
        'per_page': 100
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    vacancies = data.get('items', [])
    
    for vac in vacancies:
        # Получаем зарплату
        salary = vac.get('salary')
        salary_from = salary.get('from') if salary else None
        salary_to = salary.get('to') if salary else None
        currency = salary.get('currency') if salary else None
        
        # Получаем требования
        requirement = vac.get('snippet', {}).get('requirement', '')
        if requirement:
            requirement = requirement[:500]  # Ограничиваем длину
        
        # Сохраняем вакансию
        cur.execute("""
            INSERT INTO vacancies (id, company_id, name, salary_from, salary_to, currency, url, requirement)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (
            vac['id'],
            company_id,
            vac['name'],
            salary_from,
            salary_to,
            currency,
            vac.get('alternate_url', ''),
            requirement
        ))
        vacancy_count += 1
    
    print(f"  Загружено {len(vacancies)} вакансий")
    time.sleep(0.5)  # Пауза, чтобы не нагружать API

conn.commit()
print(f"\nВсего загружено вакансий: {vacancy_count}")

# Проверяем
cur.execute("SELECT COUNT(*) FROM vacancies")
total = cur.fetchone()[0]
print(f"Вакансий в БД: {total}")

cur.close()
conn.close()
