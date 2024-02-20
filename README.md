## Проект Foodgram
***На данном этапе находиться в стадии разработки.**

 Foodgram - продуктовый помощник с базой кулинарных рецептов. Позволяет публиковать рецепты, сохранять избранные, а также формировать список покупок для выбранных рецептов. Можно подписываться на любимых авторов.

## Технологии:
* [Python 3.10](https://docs.python.org/3.10/)
* [Django 4.2.7](https://www.djangoproject.com/)
* [Django REST Framework 3.14.0](https://www.django-rest-framework.org/)
* [gunicorn 21.2.0](https://docs.gunicorn.org/en/stable/)
* [Nginx](https://nginx.org/)
* [Docker](https://www.docker.com/)

## Запуск проекта локально
Клонировать репозиторий и перейти в него:

```
git clone https://github.com/Artyom-Serov/foodgram-project-react.git
```
```
cd foodgram-project-react
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* *Если у вас Linux/macOS*

    ```
    source venv/bin/activate
    ```

* *Если у вас Windows*

    ```
    source venv/scripts/activate
    ```
Обновить систему pip, установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
```
cd backend
```
```
pip install -r requirements.txt
```
Заполните файл ```.env.example``` и переименуйте его в ```.env```

Запустите контейнер с базой данных PostgreSQL:
```
make run
```
Выполнить миграции:

```
make migrate
```
Выполнить импорт ингредиентов и тегов базу данных:

```
make import
```
- Запустите проект:
```
make runserver
```

### * *в разработке - настройка контейнеризации Docker*
