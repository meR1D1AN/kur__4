from typing import Dict, List, Optional
from abc import ABC, abstractmethod


class VacancyAPI(ABC):
    """
    Абстрактный класс для работы с API сервиса с вакансиями
    """

    def __init__(self, base_url: str):
        self.base_url = base_url

    @abstractmethod
    def get_vacancies(self, search_query: str, area: Optional[str] = None, page: int = 0) -> List[Dict]:
        """
        Получить список вакансий с API
        """
        raise NotImplementedError()
