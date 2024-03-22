def filter_vacancies(vacancies, filter_words):
    """
    Фильтрует вакансии по ключевым словам
    """

    def filter_func(vacancy):
        description = (vacancy.description or '').lower()
        return any(word.lower() in description for word in filter_words)

    return list(filter(filter_func, vacancies))
