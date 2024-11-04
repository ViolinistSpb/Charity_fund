Заполни меня![![Python](https://img.shields.io/badge/-Python_3.9.10-464646??style=flat-square&logo=Python)](https://www.python.org/downloads/)

#  Сервис QRKot


## Используемые технологии
- [FastAPI](https://fastapi.tiangolo.com/)
- [Python 3.10](https://docs.python.org/3.10/)

## Задачи приложения:
- Сервис создания благотворительных целевых проектов и пожертвований.

## Ключевые возможности сервиса:

- Автоматическое распределение пожертвований на открытые проекты;
- Возможность авторизации, обзора своих пожертвований и всех открытых проектов.

## Примеры API запросов Проекта:

- /charity_project/ — POST-запрос на создание нового благотворительного проекта;
- /donation/my — GET-запрос на получение данных о всех пожертвованиях пользователя.

## Инструкция по запуску:
- Клонируйте репозиторий cat_charity_fund к себе на компьютер. 

    ```bash
    git clone git@github.com:ViolinistSpb/cat_charity_fund.git
    ```
- Создайте, активируйте виртуальное окружение в корне проекта.

    ```bash
    python3 -m venv venv
    source venv/bin/activate 
    ```
- Обновите pip. Установите зависимости из файла requirements.txt

    ```bash
    pip install --upgrade pip 
    pip install -r requirements.txt 
    ```


- Выполните комманды миграций поочередно

    ```bash
    alembic revision --autogenerate -m "First migration"  
    alembic upgrade head 
    ```

- Запустите сервис на локальном сервере

    ```bash
    uvicorn app.main:app --reload
    ```

## Документация OPEN Api:
http://127.0.0.1:8000/docs


### Авторы:
[Виталий Мальков](https://github.com/ViolinistSpb)
[Яндекс Практикум](https://github.com/yandex-praktikum)