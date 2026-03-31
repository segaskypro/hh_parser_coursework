import psycopg2

class DBManager:
    def __init__(self, host='localhost', port='5432', database='hh_project', user='postgres', password='1234'):
        self.conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
    
    def close(self):
        self.conn.close()
    
    def get_companies_and_vacancies_count(self):
        """Список компаний и количество вакансий у каждой"""
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
        """Список всех вакансий с названием компании, зарплатой и ссылкой"""
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
        """Средняя зарплата по всем вакансиям"""
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
            return cur.fetchone()[0]
    
    def get_vacancies_with_higher_salary(self):
        """Вакансии с зарплатой выше средней"""
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
        """Вакансии, в названии которых есть ключевое слово"""
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
