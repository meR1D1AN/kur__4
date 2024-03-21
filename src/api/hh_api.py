from src.api.vacancy_api import VacancyAPI
import requests


# Класс для работы с API платформы hh.ru
class HeadHunterAPI(VacancyAPI):
    def __init__(self):
        super().__init__("https://api.hh.ru/")

    def get_vacancies(self, search_query, area=None, page=0):
        url = f"{self.base_url}vacancies"
        params = {
            "text": search_query,
            "area": area,
            "page": page,
            "per_page": 100
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
