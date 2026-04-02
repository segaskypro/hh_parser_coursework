from typing import List, Dict, Any
import time
import requests


class HHAPI:
    """Класс для работы с API hh.ru."""

    def __init__(self, employer_ids: List[int]) -> None:
        """Инициализирует список ID компаний.

        Args:
            employer_ids: Список ID компаний для поиска
        """
        self.employer_ids = employer_ids
        self.base_url = "https://api.hh.ru"

    def get_employer_info(self, employer_id: int) -> Dict[str, Any]:
        """Получает информацию о компании по ID.

        Args:
            employer_id: ID компании

        Returns:
            Dict[str, Any]: Словарь с данными о компании
        """
        url = f"{self.base_url}/employers/{employer_id}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_vacancies_by_employer(self, employer_id: int) -> List[Dict[str, Any]]:
        """Получает все вакансии компании.

        Args:
            employer_id: ID компании

        Returns:
            List[Dict[str, Any]]: Список вакансий
        """
        all_vacancies = []
        page = 0
        per_page = 100

        while True:
            url = f"{self.base_url}/vacancies"
            params = {
                'employer_id': employer_id,
                'page': page,
                'per_page': per_page
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            all_vacancies.extend(data.get('items', []))

            if page >= data.get('pages', 1) - 1:
                break
            page += 1
            time.sleep(0.2)

        return all_vacancies

    def load_all_data(self) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Загружает данные о всех компаниях и их вакансиях.

        Returns:
            tuple: (список_компаний, список_вакансий)
        """
        companies = []
        all_vacancies = []

        for employer_id in self.employer_ids:
            company = self.get_employer_info(employer_id)
            companies.append(company)

            vacancies = self.get_vacancies_by_employer(employer_id)
            all_vacancies.extend(vacancies)

            print(f"  Загружено: {company['name']} - {len(vacancies)} вакансий")
            time.sleep(0.3)

        return companies, all_vacancies