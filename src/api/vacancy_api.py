from abc import ABC, abstractmethod


class VacancyAPI(ABC):
    """
    Абстрактный класс для работы с API сервиса с вакансиями
    """

    def __init__(self, base_url):
        self.base_url = base_url

    @abstractmethod
    def get_vacancies(self, search_query, area=None, page=0):
        """
        Получить список вакансий с API
        """
        raise NotImplementedError()
