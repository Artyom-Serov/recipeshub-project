## Проект Foodgram
***На данном этапе находиться в стадии разработки.**

 Foodgram - продуктовый помощник с базой кулинарных рецептов. Позволяет публиковать рецепты, сохранять избранные, а также формировать список покупок для выбранных рецептов. Можно подписываться на любимых авторов.

## Технологии:
* Python 3.10
* Django REST Framework 3.14.0
* Django 4.2.7
* gunicorn 21.2.0
* Docker

## Запуск проекта
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

* *Если у вас windows*

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
Выполнить миграции:

```
python3 manage.py migrate
```
Выполнить импорт ингредиентов и тегов базу данных:

```
python3 manage.py import_data
```
- Запустите проект:
```
python manage.py runserver
```
### * *в разработке - настройка контейнеризации Docker*
