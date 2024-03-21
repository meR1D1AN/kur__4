class VacancyStorage:
    """
    Абстрактный класс для сохранения вакансий
    """

    def add_vacancy(self, vacancy):
        """
        Добавить вакансию в хранилище
        """
        raise NotImplementedError()

    def get_vacancies(self, filters=None):
        """
        Получить вакансии из хранилища с применением фильтров
        """
        raise NotImplementedError()

    def delete_vacancy(self, vacancy):
        """
        Удалить вакансию из хранилища
        """
        raise NotImplementedError()
