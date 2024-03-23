from typing import List
from src.vacancy.vacancy import Vacancy


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """
    Возвращает первые top_n вакансий
    """
    return vacancies[:top_n]
