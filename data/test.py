import psycopg2

conn = psycopg2.connect(
    host='localhost',
    port='5432',
    database='hh_project',
    user='postgres',
    password='1234'
)

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
        company_id INTEGER NOT NULL REFERENCES companies(id),
        name VARCHAR(255) NOT NULL,
        salary_from INTEGER,
        salary_to INTEGER,
        currency VARCHAR(10),
        url VARCHAR(255),
        requirement TEXT
    )
""")

conn.commit()

cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
tables = cur.fetchall()
print(tables)

cur.close()
conn.close()
