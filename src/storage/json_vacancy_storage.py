from src.vacancy.vacancy import Vacancy
from src.storage.vacancy_storage import VacancyStorage
import json


class JSONVacancyStorage(VacancyStorage):
    """
    Класс для сохранения вакансий в JSON файл
    """

    def __init__(self, filepath):
        self.filepath = filepath

    def _load_vacancies(self):
        """
        Загружает данные из файла
        """
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        return data

    def _save_vacancies(self, data):
        """
        Сохраняет данные в файл
        """
        with open(self.filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def add_vacancy(self, vacancy):
        """
        Добавляет вакансию в список
        """
        data = self._load_vacancies()
        vacancy_dict = {
            "title": vacancy.title,
            "url": vacancy.url,
            "area_name": vacancy.area_name,
            "salary_from": vacancy.salary_from,
            "salary_to": vacancy.salary_to,
            "description": vacancy.description
        }
        data.append(vacancy_dict)
        self._save_vacancies(data)

    def get_vacancies(self, filters=None):
        """
        Возвращает список вакансий
        """
        data = self._load_vacancies()
        vacancies = [Vacancy(**item) for item in data]
        if filters:
            vacancies = [v for v in vacancies if all(filter(v) for filter in filters)]
        return vacancies

    def delete_vacancy(self, vacancy):
        """
        Удаляет вакансию из списка
        """
        data = self._load_vacancies()
        data = [item for item in data if item["title"] != vacancy.title]
        self._save_vacancies(data)
