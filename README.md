# Дипломный проект на Django и Django Rest Framework с моделью "Образовательные модули"

## Описание


Написать небольшой проект на Django и Django Rest Framework с моделью "Образовательные модули". В них есть:

- порядковый номер
- название
- описание

## Задача

<aside>
👾 При создании проекта  нужно:

1. реализовать для модели (моделей) все методы CRUD

2. Полностью покрыть автоматизированными юнит-тестами все модели, сериализаторы, виды.

</aside>

## Требуемый стэк

- python 3.11
- Docker
- Django

### Условия приемки

- код размещен в открытом репозитории
- доступна документация
- код покрыт автоматизированными юнит-тестами
- код оформлен согласно pep8
- оформлен Readme файл
- в проекте использован Docker

## Установка и запуск проекта:

1. клонировать репозиторий: `git clone https://github.com/morusgit/Diplom` 
2. установить виртуальную среду: `python -m venv .venv`
3. активировать виртуальную среду(Windows): `.venv\Scripts\Activate.ps1`
4. активировать виртуальную среду(Linux): `source .venv/bin/activate`
5. установить зависимости: `pip install -r requirements.txt`
6. используйте `.env.example` как образец для создания `.env` , чтобы настроить переменные окружения
7. установить PostgreSQL: `sudo apt-get install postgresql postgresql-contrib` и `sudo systemctl start postgresql`
8. создать базу данных: `sudo -u postgres psql -c "CREATE DATABASE ${POSTGRES_DB};"`
9. выполнить миграцию: `python manage.py makemigrations && python manage.py migrate`
10. запустить проект: `python manage.py runserver`
11. создать суперпользователя: `python manage.py createsuperuser`
12. создать суперпользователя (кастомная конфигурация):`python manage.py create_su`
13. в консоли запустить celery: `celery -A config worker -l INFO`
14. в консоли запустить celery beat: `celery -A config beat -l INFO`
15. используйте `docker-compose up --build` для запуска проекта через Docker

## Документация API
Документация API доступна после запуска сервера по адресу: http://localhost:8000/redoc/ или http://localhost:8000/swagger/
