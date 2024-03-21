from src.api.hh_api import HeadHunterAPI
from src.storage.json_vacancy_storage import JSONVacancyStorage
from src.utils.filter_vacancies import filter_vacancies
from src.utils.get_top_vacancies import get_top_vacancies
from src.utils.get_vacancies_by_salary import get_vacancies_by_salary
from src.utils.sort_vacancies import sort_vacancies
from src.vacancy.vacancy import Vacancy
import requests


# Функции для взаимодействия с пользователем
def get_search_query():
    """
    Запрашивает у пользователя поисковый запрос
    """
    return input("Введите поисковый запрос: ")


def get_area():
    """
    Запрашивает у пользователя название города и возвращает его id
    """
    while True:
        city_name = input("Введите название города (например, Москва, Санкт-Петербург): ")
        if city_name:
            url = "https://api.hh.ru/areas"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            area_id = None
            for area in data:
                area_id = find_area_id(area, city_name)
                if area_id:
                    break

            if area_id:
                return area_id
            else:
                print(f"Город '{city_name}' не найден. Попробуйте еще раз.")
        else:
            return None  # Если пользователь не ввел город, вернуть None


def find_area_id(area, city_name):
    """
    Функция для поиска id города внутри области
    """
    if area["name"].lower() == city_name.lower():
        return area["id"]
    else:
        for subarea in area["areas"]:
            area_id = find_area_id(subarea, city_name)
            if area_id:
                return area_id
    return None


def get_top_n():
    """
    Запрашивает у пользователя количество вакансий для вывода в топ
    """
    while True:
        user_input = input("Введите количество вакансий для вывода в топ N: ")
        if user_input:
            try:
                value = int(user_input)
                if value < 0:
                    print("Не принимается отрицательное значение. Пожалуйста, введите целое положительное число.")
                else:
                    return value
            except ValueError:
                print("Введите целое число.")
        else:
            print("Поле не может быть пустым.")


def get_filter_words():
    """
    Запрашивает у пользователя ключевые слова для фильтрации вакансий
    """
    return input("Введите ключевые слова для фильтрации вакансий (через запятую): ").split(",")


def get_salary_range():
    """
    Запрашивает у пользователя диапазон зарплат
    """
    salary_range = input("Введите диапазон зарплат (через дефис) или оставьте поле пустым: ")
    if not salary_range:
        return "Не указана"
    elif "-" not in salary_range:
        print("Указан только один диапазон зарплаты. Пожалуйста, введите оба диапазона через дефис.")
        return get_salary_range()
    else:
        return salary_range


def print_vacancies(vacancies):
    """
    Выводит вакансии на экран
    """
    for vacancy in vacancies:
        print(vacancy)
        print(">" * 50)


def user_interaction():
    """
    Функция для взаимодействия с пользователем
    """
    hh_api = HeadHunterAPI()
    json_storage = JSONVacancyStorage("data/vacancies.json")

    search_query = get_search_query()
    area = get_area()
    vacancies_data = hh_api.get_vacancies(search_query, area)
    vacancies = Vacancy.cast_to_object_list(vacancies_data)

    for vacancy in vacancies:
        json_storage.add_vacancy(vacancy)

    top_n = get_top_n()
    filter_words = get_filter_words()
    salary_range = get_salary_range()

    filtered_vacancies = filter_vacancies(vacancies, filter_words)
    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    if top_vacancies:
        print_vacancies(top_vacancies)
    else:
        print("По вашему запросу не найдено подходящих вакансий.")


if __name__ == "__main__":
    user_interaction()
