"""Модуль для импорта данных в базу данных из CSV и JSON файлов.

Настроен импорт ингредиентов из папки data.
Запускается из директории backend
командой `python manage.py import_data`.
"""
import csv
import json
import os
from typing import Any

from django.core.management import BaseCommand
from django.db import IntegrityError
from recipes.models import Ingredient, Tag

FILES_CLASSES: dict[str, type] = {
    'ingredients': Ingredient,
}

FIELDS: dict[str, tuple[str, type]] = {
    'name': ('name', Ingredient),
    'measurement_unit': ('measurement_unit', Ingredient),
}


def get_file_type(file_name: str, project_root: str) -> str | None:
    """Определяет формат файла для загрузки."""
    csv_path = os.path.join(project_root, 'data', f'{file_name}.csv')
    json_path = os.path.join(project_root, 'data', f'{file_name}.json')

    csv_exists = os.path.isfile(csv_path)
    json_exists = os.path.isfile(json_path)

    if csv_exists and json_exists:
        print(f'Найдены два файла данных: {file_name}.csv и {file_name}.json')
        print('Выберите, файл какого формата загрузить:')
        print('1 - CSV')
        print('2 - JSON')
        while True:
            choice = input('Введите номер (1 или 2): ').strip()
            if choice == '1':
                return 'csv'
            elif choice == '2':
                return 'json'
            print('Неверный выбор. Введите 1 или 2.')
    elif csv_exists:
        return 'csv'
    elif json_exists:
        return 'json'
    return None


def open_data_file(
    file_name: str,
    file_type: str,
    project_root: str
) -> list[list[str]] | list[dict[str, Any]] | None:
    """Менеджер контекста для открытия файлов."""
    file_path = os.path.join(
        project_root, 'data', f'{file_name}.{file_type}')
    try:
        with open(file_path, encoding='utf-8') as file:
            if file_type == 'csv':
                return list(csv.reader(file))
            elif file_type == 'json':
                return json.load(file)
    except FileNotFoundError:
        print(f'Файл {file_name}.{file_type} не найден.')
        return None
    except Exception as e:
        print(f'Ошибка при открытии файла {file_name}.{file_type}: {e}')
        return None


def change_foreign_values(data: dict[str, Any]) -> dict[str, Any]:
    """Изменяет значения."""
    data_copy = data.copy()
    for field_key, field_value in data.items():
        if field_key in FIELDS.keys():
            field_key0 = FIELDS[field_key][0]
            if field_key0 == 'measurement_unit':
                continue
            data_copy[field_key0] = field_value
            if ('measurement_unit' in
                    data and FIELDS['measurement_unit'][0] == field_key0):
                data_copy['measurement_unit'] = data['measurement_unit']
    return data_copy


def load_data(
    file_name: str,
    class_name: type,
    file_type: str,
    project_root: str
) -> None:
    """Загружает данные ингредиентов из файлов ingredients.json или
    ingredients.csv."""
    table_not_loaded = (f'Информация в таблицу'
                        f'{class_name.__qualname__} не загружена.')
    table_loaded = f'Информация в таблицу {class_name.__qualname__} загружена.'
    data = open_data_file(file_name, file_type, project_root)

    if data is None:
        print(f'Пропуск загрузки данных для {file_name}.{file_type}')
        return

    loaded_count = 0
    if file_type == 'csv':
        rows = data
        header = rows[0]
        for row in rows[1:]:
            data_csv = change_foreign_values(
                {key: value for key, value in zip(header, row)})
            try:
                _, created = class_name.objects.get_or_create(
                    name=data_csv['name'],
                    measurement_unit=data_csv.get('measurement_unit', ''),
                    defaults=data_csv
                )
                if created:
                    loaded_count += 1
            except (ValueError, IntegrityError) as error:
                print(
                    f'Ошибка в загружаемых данных.'
                    f'{error}. {table_not_loaded}')
                break
    elif file_type == 'json':
        for item in data:
            if not isinstance(item, dict):
                continue
            item = change_foreign_values(item)
            try:
                _, created = class_name.objects.get_or_create(
                    name=item['name'],
                    measurement_unit=item.get('measurement_unit', ''),
                    defaults=item
                )
                if created:
                    loaded_count += 1
            except (ValueError, IntegrityError) as error:
                print(
                    f'Ошибка в загружаемых данных.'
                    f'{error}. {table_not_loaded}')
                break

    print(f'Загружено {loaded_count} записей.')
    print(table_loaded)


def load_tags(project_root: str) -> None:
    """Загружает данные тегов из файла tags.json."""
    file_name = 'tags'
    file_type = 'json'
    class_name = Tag

    data = open_data_file(file_name, file_type, project_root)

    if data is None:
        print(f'Пропуск загрузки данных для {file_name}.{file_type}')
        return

    loaded_count = 0
    tags_data: list[dict[str, Any]] = [
        item for item in data if isinstance(item, dict)
    ]
    for item in tags_data:
        try:
            _, created = class_name.objects.get_or_create(
                slug=item['slug'],
                defaults=item
            )
            if created:
                print(f'Тег {item["name"]} загружен.')
                loaded_count += 1
        except (ValueError, IntegrityError) as error:
            print(f'Ошибка в загружаемых данных. {error}.')
            break

    print(f'Загружено {loaded_count} тегов.')
    print(f'Информация в таблицу {class_name.__qualname__} загружена.')


class Command(BaseCommand):
    """Класс загрузки информации в базу данных."""

    def handle(self, *args, **options):
        project_root = os.getcwd()
        for key, value in FILES_CLASSES.items():
            print(f'Загрузка информации в таблицу {value.__qualname__}')
            file_type = get_file_type(key, project_root)
            if file_type:
                load_data(key, value, file_type, project_root)
            else:
                print(f'Файл для {key} не найден. Пропуск.')

        print('Загрузка тегов')
        load_tags(project_root)
