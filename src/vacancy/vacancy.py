import html2text
from typing import Optional


# Класс для работы с вакансиями
class Vacancy:
    """
    Класс для работы с вакансиями
    """

    __slots__ = ("title", "url", "area_name", "salary_from", "salary_to", "description")

    def __init__(self, title: str, url: str, area_name: str,
                 salary_from: Optional[int], salary_to: Optional[int], description: str):
        self.title = title
        self.url = url
        self.area_name = area_name
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.description = description

    def __str__(self):
        salary_str = self.get_salary_string()
        return (f"Ссылка на вакансию: {self.url} -> Город: {self.area_name}\n"
                f"Вакансия: {self.title}\n"
                f"Зарплата: {salary_str}\n"
                f"Описание: {self.description[:150]}...")

    def __lt__(self, other):
        """Магический метод для сравнения вакансий по зарплате"""
        return self.get_average_salary() < other.get_average_salary()

    def get_salary_string(self):
        """Получение строкового представления зарплаты"""
        if self.salary_from and self.salary_to:
            return f"от {self.salary_from} до {self.salary_to}"
        elif self.salary_from:
            return f"от {self.salary_from}"
        elif self.salary_to:
            return f"до {self.salary_to}"
        else:
            return "Не указана"

    def get_average_salary(self):
        """Получение средней зарплаты"""
        if self.salary_from and self.salary_to:
            return (self.salary_from + self.salary_to) // 2
        elif self.salary_from:
            return self.salary_from
        elif self.salary_to:
            return self.salary_to
        else:
            return 0

    @staticmethod
    def cast_to_object_list(vacancy_data):
        """Преобразование данных из API в список объектов Vacancy"""
        vacancy_list = []
        for item in vacancy_data["items"]:
            title = item["name"]
            url = item["alternate_url"]
            area_name = item["area"].get("name")
            salary_from = item["salary"].get("from", None) if item.get("salary") else None
            salary_to = item["salary"].get("to", None) if item.get("salary") else None
            description = ""
            if item.get("snippet") and item["snippet"].get("requirement"):
                description = html2text.html2text(item["snippet"]["requirement"])
            vacancy_list.append(Vacancy(title, url, area_name, salary_from, salary_to, description))
        return vacancy_list
