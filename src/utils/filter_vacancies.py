from typing import List
from src.vacancy.vacancy import Vacancy


def filter_vacancies(vacancies: List[Vacancy], filter_words: List[str]) -> List[Vacancy]:
    """
    Фильтрует вакансии по ключевым словам
    """

    def filter_func(vacancy):
        description = (vacancy.description or '').lower()
        return any(word.lower() in description for word in filter_words)

    return list(filter(filter_func, vacancies))
