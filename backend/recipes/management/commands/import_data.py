"""Импорт данных в базу данных из CSV и JSON файлов."""
import csv
import json
import os

from django.core.management import BaseCommand
from django.db import IntegrityError

from recipes.models import Ingredient

FILES_CLASSES = {
    'ingredients': Ingredient,
}

FIELDS = {
    'name': ('name', Ingredient),
    'measurement_unit': ('measurement_unit', Ingredient),
}


def open_data_file(file_name, file_type, project_root):
    """Менеджер контекста для открытия файлов."""
    file_path = os.path.join(
        project_root, '..', 'data', f'{file_name}.{file_type}')
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


def change_foreign_values(data):
    """Изменяет значения."""
    data_copy = data.copy()
    for field_key, field_value in data.items():
        if field_key in FIELDS.keys():
            field_key0 = FIELDS[field_key][0]
            if field_key0 == 'measurement_unit':
                continue
            data_copy[field_key0] = field_value
            if ('measurement_unit' in data and
                    FIELDS['measurement_unit'][0] == field_key0):
                data_copy['measurement_unit'] = data['measurement_unit']
    return data_copy


def load_data(file_name, class_name, file_type, project_root):
    """Осуществляет загрузку данных."""
    table_not_loaded = f'Таблица {class_name.__qualname__} не загружена.'
    table_loaded = f'Таблица {class_name.__qualname__} загружена.'
    data = open_data_file(file_name, file_type, project_root)

    if data is None:
        print(f'Пропуск загрузки данных для {file_name}.{file_type}')
        return

    if file_type == 'csv':
        rows = data[1:]
        for row in rows:
            data_csv = change_foreign_values(
                {key: value for key, value in zip(data[0], row)})
            try:
                table = class_name(**data_csv)
                table.save()
            except (ValueError, IntegrityError) as error:
                print(
                    f'Ошибка в загружаемых данных.'
                    f'{error}. {table_not_loaded}')
                break
        print(table_loaded)
    elif file_type == 'json':
        for item in data:
            item = change_foreign_values(item)
            try:
                table = class_name(**item)
                table.save()
            except (ValueError, IntegrityError) as error:
                print(
                    f'Ошибка в загружаемых данных.'
                    f'{error}. {table_not_loaded}')
                break
        print(table_loaded)


class Command(BaseCommand):
    """Класс загрузки информации в базу данных."""

    def handle(self, *args, **options):
        project_root = os.getcwd()
        for key, value in FILES_CLASSES.items():
            print(f'Загрузка таблицы {value.__qualname__}')
            load_data(key, value, 'csv', project_root)
            load_data(key, value, 'json', project_root)
