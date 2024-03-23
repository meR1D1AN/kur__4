from typing import List
from src.vacancy.vacancy import Vacancy


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """
    Сортирует вакансии по зарплате
    """
    return sorted(vacancies, reverse=True)
