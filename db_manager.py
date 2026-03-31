import psycopg2
from config import Config

class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(Config.get_db_url())
    
    def close(self):
        self.conn.close()
    
    def get_companies_and_vacancies_count(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, COUNT(v.id)
                FROM companies c
                LEFT JOIN vacancies v ON c.id = v.company_id
                GROUP BY c.id
                ORDER BY COUNT(v.id) DESC
            """)
            return cur.fetchall()
    
    def get_all_vacancies(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, v.name, 
                       COALESCE(v.salary_from, v.salary_to, 0),
                       v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.id
            """)
            return cur.fetchall()
    
    def get_avg_salary(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG(
                    CASE 
                        WHEN salary_from IS NOT NULL AND salary_to IS NOT NULL 
                        THEN (salary_from + salary_to) / 2.0
                        WHEN salary_from IS NOT NULL THEN salary_from
                        WHEN salary_to IS NOT NULL THEN salary_to
                        ELSE NULL
                    END
                )
                FROM vacancies
                WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL
            """)
            result = cur.fetchone()[0]
            return result if result else 0
    
    def get_vacancies_with_higher_salary(self):
        avg = self.get_avg_salary()
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, v.name,
                       CASE 
                           WHEN salary_from IS NOT NULL AND salary_to IS NOT NULL 
                           THEN (salary_from + salary_to) / 2.0
                           WHEN salary_from IS NOT NULL THEN salary_from
                           WHEN salary_to IS NOT NULL THEN salary_to
                           ELSE 0
                       END as salary,
                       v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.id
                WHERE (salary_from > %s OR salary_to > %s)
                ORDER BY salary DESC
            """, (avg, avg))
            return cur.fetchall()
    
    def get_vacancies_with_keyword(self, keyword):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT c.name, v.name,
                       COALESCE(v.salary_from, v.salary_to, 0),
                       v.url
                FROM vacancies v
                JOIN companies c ON v.company_id = c.id
                WHERE v.name ILIKE %s
            """, (f'%{keyword}%',))
            return cur.fetchall()