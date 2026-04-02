import sys
from pathlib import Path

# Добавляем путь к корню проекта
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.db_utils import create_database, create_tables, save_companies_to_db, save_vacancies_to_db


class TestDBUtils:
    """Тесты для db_utils."""

    @patch('src.db_utils.psycopg2.connect')
    def test_create_database(self, mock_connect):
        """Тест создания базы данных."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        create_database()

        mock_cursor.execute.assert_called()
        mock_conn.close.assert_called()

    @patch('src.db_utils.psycopg2.connect')
    def test_create_tables(self, mock_connect):
        """Тест создания таблиц."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        create_tables()

        assert mock_cursor.execute.call_count >= 2
        mock_conn.commit.assert_called()
        mock_conn.close.assert_called()

    @patch('src.db_utils.psycopg2.connect')
    def test_save_companies_to_db(self, mock_connect):
        """Тест сохранения компаний в БД."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        companies = [
            {'id': 1, 'name': 'Яндекс', 'description': 'Описание', 'site_url': 'https://yandex.ru'},
            {'id': 2, 'name': 'Сбер', 'description': '', 'site_url': ''}
        ]

        save_companies_to_db(companies)

        assert mock_cursor.execute.call_count == 2
        mock_conn.commit.assert_called()
        mock_conn.close.assert_called()

    @patch('src.db_utils.psycopg2.connect')
    def test_save_vacancies_to_db(self, mock_connect):
        """Тест сохранения вакансий в БД."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        vacancies = [
            {
                'id': 1,
                'employer': {'id': 1740},
                'name': 'Python разработчик',
                'salary': {'from': 100000, 'to': 150000, 'currency': 'RUR'},
                'alternate_url': 'https://hh.ru/1',
                'snippet': {'requirement': 'Знание Python'}
            }
        ]

        save_vacancies_to_db(vacancies)

        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called()
        mock_conn.close.assert_called()