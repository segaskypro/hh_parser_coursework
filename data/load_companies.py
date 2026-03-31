import psycopg2
import requests

# Список ID компаний (10 штук)
employer_ids = [1740, 3529, 39305, 80, 15478, 3776, 2748, 3127, 907345, 2381]

# Подключаемся к БД
conn = psycopg2.connect(
    host='localhost',
    port='5432',
    database='hh_project',
    user='postgres',
    password='1234'
)
cur = conn.cursor()

# Получаем данные о каждой компании и сохраняем
for employer_id in employer_ids:
    # Запрашиваем данные с hh.ru
    url = f"https://api.hh.ru/employers/{employer_id}"
    response = requests.get(url)
    company = response.json()
    
    # Сохраняем в таблицу companies
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
    print(f"Добавлена компания: {company['name']}")

# Сохраняем изменения
conn.commit()

# Проверяем, что добавилось
cur.execute("SELECT id, name FROM companies")
companies = cur.fetchall()
print("\nСписок компаний в БД:")
for id, name in companies:
    print(f"  {id}: {name}")

cur.close()
conn.close()
