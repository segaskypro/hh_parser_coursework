import sys
from pathlib import Path

# Добавляем путь к корню проекта
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.db_manager import DBManager


class TestDBManager:
    """Тесты для DBManager."""

    @patch('src.db_manager.psycopg2.connect')
    def test_get_companies_and_vacancies_count(self, mock_connect):
        """Тест получения компаний и количества вакансий."""
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [('Яндекс', 100), ('Сбер', 50)]
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DBManager()
        result = db.get_companies_and_vacancies_count()

        assert result == [('Яндекс', 100), ('Сбер', 50)]
        mock_cursor.execute.assert_called_once()

    @patch('src.db_manager.psycopg2.connect')
    def test_get_avg_salary(self, mock_connect):
        """Тест получения средней зарплаты."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (100000.0,)
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DBManager()
        result = db.get_avg_salary()

        assert result == 100000.0

    @patch('src.db_manager.psycopg2.connect')
    def test_get_avg_salary_no_data(self, mock_connect):
        """Тест получения средней зарплаты когда нет данных."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (None,)
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DBManager()
        result = db.get_avg_salary()

        assert result == 0.0

    @patch('src.db_manager.DBManager.get_avg_salary')
    @patch('src.db_manager.psycopg2.connect')
    def test_get_vacancies_with_higher_salary(self, mock_connect, mock_get_avg):
        """Тест получения вакансий с зарплатой выше средней."""
        mock_get_avg.return_value = 100000.0

        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            ('Яндекс', 'Python разработчик', 200000.0, 'https://hh.ru/1'),
            ('Сбер', 'Java разработчик', 150000.0, 'https://hh.ru/2'),
        ]
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DBManager()
        result = db.get_vacancies_with_higher_salary()

        assert len(result) == 2
        assert result[0][1] == 'Python разработчик'

    @patch('src.db_manager.psycopg2.connect')
    def test_get_vacancies_with_keyword(self, mock_connect):
        """Тест поиска вакансий по ключевому слову."""
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            ('Яндекс', 'Python разработчик', 200000, 'https://hh.ru/1'),
            ('Сбер', 'Python бэкенд', 150000, 'https://hh.ru/2'),
        ]
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DBManager()
        result = db.get_vacancies_with_keyword('python')

        assert len(result) == 2
        mock_cursor.execute.assert_called_once()

    @patch('src.db_manager.psycopg2.connect')
    def test_get_all_vacancies(self, mock_connect):
        """Тест получения всех вакансий."""
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            ('Яндекс', 'Python разработчик', 200000, 'https://hh.ru/1'),
            ('Сбер', 'Java разработчик', 150000, 'https://hh.ru/2'),
        ]
        mock_conn = MagicMock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        db = DBManager()
        result = db.get_all_vacancies()

        assert len(result) == 2
        mock_cursor.execute.assert_called_once()

    @patch('src.db_manager.psycopg2.connect')
    def test_close_connection(self, mock_connect):
        """Тест закрытия соединения."""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        db = DBManager()
        db.close()

        mock_conn.close.assert_called_once()
