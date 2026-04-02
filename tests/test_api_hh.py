import sys
from pathlib import Path

# Добавляем путь к корню проекта
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.api_hh import HHAPI


class TestHHAPI:
    """Тесты для HHAPI."""

    @patch('src.api_hh.requests.get')
    def test_get_employer_info(self, mock_get):
        """Тест получения информации о компании."""
        mock_response = Mock()
        mock_response.json.return_value = {'id': 1740, 'name': 'Яндекс'}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        api = HHAPI([1740])
        result = api.get_employer_info(1740)

        assert result['id'] == 1740
        assert result['name'] == 'Яндекс'
        mock_get.assert_called_once_with('https://api.hh.ru/employers/1740')

    @patch('src.api_hh.requests.get')
    def test_get_vacancies_by_employer_one_page(self, mock_get):
        """Тест получения вакансий (одна страница)."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'items': [{'id': 1, 'name': 'Вакансия 1'}],
            'pages': 1
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        api = HHAPI([1740])
        result = api.get_vacancies_by_employer(1740)

        assert len(result) == 1
        assert result[0]['id'] == 1

    @patch('src.api_hh.requests.get')
    def test_get_vacancies_by_employer_multiple_pages(self, mock_get):
        """Тест получения вакансий (несколько страниц)."""
        mock_response1 = Mock()
        mock_response1.json.return_value = {
            'items': [{'id': 1, 'name': 'Вакансия 1'}],
            'pages': 2
        }
        mock_response1.raise_for_status = Mock()

        mock_response2 = Mock()
        mock_response2.json.return_value = {
            'items': [{'id': 2, 'name': 'Вакансия 2'}],
            'pages': 2
        }
        mock_response2.raise_for_status = Mock()

        mock_get.side_effect = [mock_response1, mock_response2]

        api = HHAPI([1740])
        result = api.get_vacancies_by_employer(1740)

        assert len(result) == 2

    @patch('src.api_hh.HHAPI.get_employer_info')
    @patch('src.api_hh.HHAPI.get_vacancies_by_employer')
    def test_load_all_data(self, mock_get_vacancies, mock_get_employer):
        """Тест загрузки всех данных."""
        mock_get_employer.return_value = {'id': 1740, 'name': 'Яндекс'}
        mock_get_vacancies.return_value = [
            {'id': 1, 'name': 'Вакансия 1'},
            {'id': 2, 'name': 'Вакансия 2'}
        ]

        api = HHAPI([1740, 3529])
        companies, vacancies = api.load_all_data()

        assert len(companies) == 2
        assert len(vacancies) == 4
