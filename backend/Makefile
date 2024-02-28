# Переменные
DOCKER_COMPOSE = docker compose compose -f docker-compose.database.yml
OS := $(shell uname)
# Если операционная система - Linux, добавляем sudo
ifeq ($(OS),Linux)
    DOCKER_COMPOSE = sudo docker compose -f docker-compose.database.yml
    DOCKER_EXEC = sudo $(DOCKER_COMPOSE) exec backend
endif
# Цели
.PHONY: help migrate createsuperuser import clean

help:
	@echo "Доступные команды:"
	@echo "  run               Запустить контейнер с базой данных"
	@echo "  down              Остановить контейнер с базой данных"
	@echo "  migrate           Применить миграции Django"
	@echo "  createsuperuser   Создать суперпользователя Django"
	@echo "  import            Запустить импорт ингредиентов и тэгов"
	@echo "  runserver         Запустить проект локально"

run:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down --rmi all

migrate:
	python3 manage.py migrate

createsuperuser:
	python3 manage.py createsuperuser

import:
	python3 manage.py import_data

runserver:
	python3 manage.py runserver
