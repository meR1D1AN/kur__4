import pytest
import requests
from src.api.hh_api import HeadHunterAPI
from src.api.vacancy_api import VacancyAPI
from src.vacancy.vacancy import Vacancy
from src.storage.json_vacancy_storage import JSONVacancyStorage
from src.storage.vacancy_storage import VacancyStorage
from src.utils.filter_vacancies import filter_vacancies
from src.utils.get_top_vacancies import get_top_vacancies
from src.utils.get_vacancies_by_salary import get_vacancies_by_salary
from src.utils.sort_vacancies import sort_vacancies
from unittest.mock import MagicMock


# Тесты для класса VacancyAPI
def test_vacancy_api_init():
    base_url = "http://test.com"
    vacancy_api = VacancyAPI(base_url)
    assert vacancy_api.base_url == base_url


def test_vacancy_api_get_vacancies():
    vacancy_api = VacancyAPI("http://test.com")
    with pytest.raises(NotImplementedError):
        vacancy_api.get_vacancies("Test")


# Тесты для класса HeadHunterAPI
def test_get_vacancies(monkeypatch):
    def mock_get(*args, **kwargs):
        return MagicMock(json=lambda: {"items": [{"id": 1, "name": "Test Vacancy"}]})

    monkeypatch.setattr(requests, "get", mock_get)

    hh_api = HeadHunterAPI()
    vacancies = hh_api.get_vacancies("Test")
    assert vacancies == {"items": [{"id": 1, "name": "Test Vacancy"}]}


# Тесты для класса Vacancy
def test_vacancy_init():
    vacancy = Vacancy("Test Vacancy", "http://test.com", "Нижний Новгород", 100000, 0, "Test description")
    assert vacancy.title == "Test Vacancy"
    assert vacancy.url == "http://test.com"
    assert vacancy.area_name == "Нижний Новгород"
    assert vacancy.salary_from == 100000
    assert vacancy.salary_to == 0
    assert vacancy.description == "Test description"


def test_vacancy_str():
    vacancy = Vacancy("Test Vacancy", "http://test.com", "Москва", 100000, 0, "Test description")
    assert str(
        vacancy) == ("Ссылка на вакансию: http://test.com -> Город: Москва\nВакансия: Test Vacancy"
                     "\nЗарплата: от 100000\nОписание: Test description...")


def test_vacancy_lt():
    vacancy1 = Vacancy("Test Vacancy", "http://test.com", "Москва", 100000, 0, "Test description")
    vacancy2 = Vacancy("Test Vacancy", "http://test.com", "Москва", 100000, 200000, "Test description")
    assert vacancy1 < vacancy2


@pytest.mark.parametrize("salary_from, salary_to, expected_average_salary", [
    (100000, 200000, 150000),
    (None, None, 0),
    (100000, 0, 100000),
    (0, 150000, 150000),
    (0, 0, 0),
    (150000, 0, 150000)
])
def test_get_average_salary(salary_from, salary_to, expected_average_salary):
    vacancy = Vacancy("Test Vacancy", "http://test.com", "Москва", salary_from, salary_to, "Test description")
    assert vacancy.get_average_salary() == expected_average_salary


@pytest.mark.parametrize("salary_from, salary_to, expected_salary_string", [
    (100000, 200000, "от 100000 до 200000"),
    (100000, 0, "от 100000"),
    (0, 200000, "до 200000"),
    (None, None, "Не указана")
])
def test_get_salary_string(salary_from, salary_to, expected_salary_string):
    vacancy = Vacancy("Test Vacancy", "http://test.com", "Москва", salary_from, salary_to, "Test description")
    assert vacancy.get_salary_string() == expected_salary_string


def test_salary_to_int_string_range():
    vacancy = Vacancy("Test Vacancy", "http://test.com", "Москва", 100000, 200000, "Test description")
    assert vacancy.get_average_salary() == 150000


def test_salary_to_int_none():
    vacancy = Vacancy("Test Vacancy", "http://test.com", "Москва", None, None, "Test description")
    assert vacancy.get_average_salary() == 0


def test_salary_to_int():
    vacancy1 = Vacancy("Test Vacancy 1", "http://test.com", "Москва", 100000, 200000, "Test description")
    vacancy2 = Vacancy("Test Vacancy 2", "http://test.com", "Москва", 0, 150000, "Test description")
    vacancy3 = Vacancy("Test Vacancy 3", "http://test.com", "Москва", 0, 0, "Test description")
    assert vacancy1.get_average_salary() == 150000
    assert vacancy2.get_average_salary() == 150000
    assert vacancy3.get_average_salary() == 0


def test_salary_to_int_string_single_value():
    vacancy = Vacancy("Test Vacancy", "http://test.com", "Москва", 100000, 0, "Test description")
    assert vacancy.get_average_salary() == 100000


def test_salary_to_int_int():
    vacancy = Vacancy("Test Vacancy", "http://test.com", "Москва", 150000, 0, "Test description")
    assert vacancy.get_average_salary() == 150000


def test_cast_to_object_list():
    vacancy_data = {
        "items": [
            {
                "name": "Test Vacancy 1",
                "alternate_url": "http://test.com",
                "area": {"name": "Москва"},
                "salary": {"from": 100000, "to": 100000},
                "snippet": {"requirement": "<p>Test description 1</p>"}
            },
            {
                "name": "Test Vacancy 2",
                "alternate_url": "http://test.com",
                "area": {"name": "Москва"},
                "salary": {"from": 0, "to": 0},
                "snippet": {"requirement": "<p>Test description 2</p>"}
            },
            {
                "name": "Test Vacancy 3",
                "alternate_url": "http://test.com",
                "area": {"name": "Москва"},
                "salary": {"from": 100000, "to": 150000},
                "snippet": {"requirement": "<p>Test description 3</p>"}
            }
        ]
    }
    vacancies = Vacancy.cast_to_object_list(vacancy_data)
    assert len(vacancies) == 3
    assert vacancies[0].title == "Test Vacancy 1"
    assert vacancies[0].salary_from == 100000
    assert vacancies[0].salary_to == 100000
    assert vacancies[0].description == "Test description 1\n\n"
    assert vacancies[1].title == "Test Vacancy 2"
    assert vacancies[1].salary_from == 0
    assert vacancies[1].salary_to == 0
    assert vacancies[1].description == "Test description 2\n\n"
    assert vacancies[2].title == "Test Vacancy 3"
    assert vacancies[2].salary_from == 100000
    assert vacancies[2].salary_to == 150000
    assert vacancies[2].description == "Test description 3\n\n"


# Тесты для класса JSONVacancyStorage
def test_json_vacancy_storage(tmp_path):
    storage = JSONVacancyStorage(tmp_path / "test.json")
    vacancy1 = Vacancy("Test Vacancy 1", "http://test.com", "Москва", 100000, 0, "Test description 1")
    vacancy2 = Vacancy("Test Vacancy 2", "http://test.com", "Москва", 200000, 0, "Test description 2")

    storage.add_vacancy(vacancy1)
    storage.add_vacancy(vacancy2)

    vacancies = storage.get_vacancies()
    assert len(vacancies) == 2
    assert vacancies[0].title == "Test Vacancy 1"
    assert vacancies[1].title == "Test Vacancy 2"

    storage.delete_vacancy(vacancy1)
    vacancies = storage.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0].title == "Test Vacancy 2"


def test_json_vacancy_storage_load_vacancies_file_not_found(tmp_path):
    storage = JSONVacancyStorage(tmp_path / "nonexistent.json")
    vacancies = storage._load_vacancies()
    assert vacancies == []


def test_json_vacancy_storage_get_vacancies_with_filters(tmp_path):
    storage = JSONVacancyStorage(tmp_path / "test.json")
    vacancy1 = Vacancy("Test Vacancy 1", "http://test.com", "Москва", 100000, 0, "Test description python")
    vacancy2 = Vacancy("Test Vacancy 2", "http://test.com", "Москва", 200000, 0, "Test description java")
    storage.add_vacancy(vacancy1)
    storage.add_vacancy(vacancy2)

    filters = [lambda v: "python" in v.description]
    filtered_vacancies = storage.get_vacancies(filters)
    assert len(filtered_vacancies) == 1
    assert filtered_vacancies[0].title == "Test Vacancy 1"


def test_vacancy_storage_add_vacancy():
    storage = VacancyStorage()
    vacancy = Vacancy("Test Vacancy", "http://test.com", "Москва", 100000, 0, "Test description")
    with pytest.raises(NotImplementedError):
        storage.add_vacancy(vacancy)


def test_vacancy_storage_delete_vacancy():
    storage = VacancyStorage()
    vacancy = Vacancy("Test Vacancy", "http://test.com", "Москва", 100000, 0, "Test description")
    with pytest.raises(NotImplementedError):
        storage.delete_vacancy(vacancy)


def test_vacancy_storage_get_vacancies():
    storage = VacancyStorage()
    vacancy = Vacancy("Test Vacancy", "http://test.com", "Москва", 100000, 0, "Test description")
    with pytest.raises(NotImplementedError):
        storage.get_vacancies(vacancy)


# Тесты для функций взаимодействия с пользователем
def test_filter_vacancies():
    vacancy1 = Vacancy("Test Vacancy 1", "http://test.com", "Москва", 100000, 0, "Test description python")
    vacancy2 = Vacancy("Test Vacancy 2", "http://test.com", "Москва", 200000, 0, "Test description java")
    vacancies = [vacancy1, vacancy2]
    filtered_vacancies = filter_vacancies(vacancies, ["python"])
    assert len(filtered_vacancies) == 1
    assert filtered_vacancies[0].title == "Test Vacancy 1"


def test_get_vacancies_by_salary():
    vacancy1 = Vacancy("Test Vacancy 1", "http://test.com", "Москва", 100000, 0, "Test description")
    vacancy2 = Vacancy("Test Vacancy 2", "http://test.com", "Москва", 200000, 0, "Test description")
    vacancy3 = Vacancy("Test Vacancy 3", "http://test.com", "Москва", None, None, "Test description")
    vacancies = [vacancy1, vacancy2, vacancy3]

    # Тест для случая, когда salary_range равен "Не указана"
    ranged_vacancies = get_vacancies_by_salary(vacancies, "Не указана")
    assert len(ranged_vacancies) == 3
    assert ranged_vacancies == vacancies

    # Тест для случая, когда salary_range указан диапазоном
    ranged_vacancies = get_vacancies_by_salary(vacancies, "150000-250000")
    assert len(ranged_vacancies) == 1
    assert ranged_vacancies[0].title == "Test Vacancy 2"

    # Тест для случая, когда ни одна вакансия не попадает в указанный диапазон
    ranged_vacancies = get_vacancies_by_salary(vacancies, "300000-400000")
    assert len(ranged_vacancies) == 0


def test_sort_vacancies():
    vacancy1 = Vacancy("Test Vacancy 1", "http://test.com", "Москва", 100000, 0, "Test description")
    vacancy2 = Vacancy("Test Vacancy 2", "http://test.com", "Москва", 200000, 0, "Test description")
    vacancies = [vacancy1, vacancy2]
    sorted_vacancies = sort_vacancies(vacancies)
    assert sorted_vacancies[0].title == "Test Vacancy 2"
    assert sorted_vacancies[1].title == "Test Vacancy 1"


def test_get_top_vacancies():
    vacancy1 = Vacancy("Test Vacancy 1", "http://test.com", "Москва", 100000, 0, "Test description")
    vacancy2 = Vacancy("Test Vacancy 2", "http://test.com", "Москва", 200000, 0, "Test description")
    vacancies = [vacancy1, vacancy2]
    top_vacancies = get_top_vacancies(vacancies, 1)
    assert len(top_vacancies) == 1
    assert top_vacancies[0].title == "Test Vacancy 1"
