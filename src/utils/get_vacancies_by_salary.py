def get_vacancies_by_salary(vacancies, salary_range):
    """
    Фильтрует вакансии по зарплате
    """
    if salary_range == "Не указана":
        return vacancies
    else:
        min_salary, max_salary = map(int, salary_range.split("-"))
        return [v for v in vacancies if min_salary <= v.get_average_salary() <= max_salary]
