def filter_vacancies(vacancies, filter_words):
    """
    Фильтрует вакансии по ключевым словам
    """
    filters = [lambda v: all(word.lower() in (v.description or '').lower() for word in filter_words)]
    return [v for v in vacancies if all(filter(v) for filter in filters)]
