class VacancyAPI:
    """
    Абстрактный класс для работы с API сервиса с вакансиями
    """

    def __init__(self, base_url):
        self.base_url = base_url

    def get_vacancies(self, search_query):
        """
        Получить список вакансий с API
        """
        raise NotImplementedError()
