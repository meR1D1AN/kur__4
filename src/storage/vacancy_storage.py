from typing import List, Optional
from src.vacancy.vacancy import Vacancy


class VacancyStorage:
    """
    Абстрактный класс для сохранения вакансий
    """

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Добавить вакансию в хранилище
        """
        raise NotImplementedError()

    def get_vacancies(self, filters: Optional[List[callable]] = None) -> List[Vacancy]:
        """
        Получить вакансии из хранилища с применением фильтров
        """
        raise NotImplementedError()

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """
        Удалить вакансию из хранилища
        """
        raise NotImplementedError()
