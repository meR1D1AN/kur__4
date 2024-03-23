from src.api.vacancy_api import VacancyAPI
import requests


# Класс для работы с API платформы hh.ru
class HeadHunterAPI(VacancyAPI):
    def __init__(self):
        super().__init__("https://api.hh.ru/")
        self._url = self.base_url

    @property
    def url(self):
        return self._url

    def get_vacancies(self, search_query, area=None, page=0):
        url = f"{self.base_url}vacancies"
        params = {
            "text": search_query,
            "area": area,
            "page": page,
            "per_page": 100
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при выполнении запроса к API hh.ru: {e}")
            return None
