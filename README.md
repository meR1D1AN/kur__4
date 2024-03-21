# Поиск вакансий с использованием API HeadHunter

Это Python-проект, который позволяет искать вакансии через API HeadHunter, фильтровать их по ключевым словам и зарплате,
сортировать и выводить лучшие вакансии.

## Возможности

- Поиск вакансий по введенному запросу
- Фильтрация вакансий по ключевым словам в описании
- Фильтрация вакансий по диапазону зарплаты
- Сортировка вакансий по зарплате
- Вывод топ-N лучших вакансий

## Структура проекта

- `src/api/hh_api.py`: Класс для работы с API HeadHunter
- `src/api/vacancy_api.py`: Абстрактный класс для работы с API сервиса вакансий
- `src/storage/json_vacancy_storage.py`: Класс для сохранения вакансий в JSON файл
- `src/storage/vacancy_storage.py`: Абстрактный класс для хранения вакансий
- `src/utils/filter_vacancies.py`: Функция для фильтрации вакансий по ключевым словам
- `src/utils/get_top_vacancies.py`: Функция для получения топ-N вакансий
- `src/utils/get_vacancies_by_salary.py`: Функция для фильтрации вакансий по зарплате
- `src/utils/sort_vacancies.py`: Функция для сортировки вакансий
- `src/vacancy/vacancy.py`: Класс для работы с вакансиями
- `main.py`: Главный модуль для запуска программы и взаимодействия с пользователем

## Использование

1. Клонируйте репозиторий
2. Установите необходимые зависимости
3. Запустите `main.py`
4. Следуйте инструкциям в терминале

При запуске программа запросит:

- Поисковый запрос для вакансий
- Город в котором нужно искать
- Количество вакансий для вывода в топ-N
- Ключевые слова для фильтрации вакансий (через запятую)
- Диапазон зарплат (через дефис) или оставьте поле пустым

После этого программа выведет список лучших вакансий, отфильтрованных и отсортированных по заданным критериям.

## Примечания

- Вакансии сохраняются в файл `data/vacancies.json`
- Используется библиотека `requests` для работы с API
- Используется библиотека `html2text` для преобразования HTML-описания вакансий в текст