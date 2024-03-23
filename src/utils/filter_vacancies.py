from typing import List
from src.vacancy.vacancy import Vacancy


def filter_vacancies(vacancies: List[Vacancy], filter_words: List[str]) -> List[Vacancy]:
    """
    Фильтрует вакансии по ключевым словам
    """
    filters = [lambda v: all(word.lower() in (v.description or '').lower() for word in filter_words)]
    return [v for v in vacancies if all(filter(v) for filter in filters)]
