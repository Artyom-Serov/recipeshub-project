# Переменные
DOCKER_COMPOSE = docker compose
DOCKER_EXEC = $(DOCKER_COMPOSE) exec backend
OS := $(shell uname)
# Если операционная система - Linux, добавляем sudo
ifeq ($(OS),Linux)
    DOCKER_COMPOSE = sudo docker compose
    DOCKER_EXEC = sudo $(DOCKER_COMPOSE) exec backend
endif
# Цели
.PHONY: help run migrate createsuperuser import clean

help:
	@echo "Доступные команды:"
	@echo "  run               Запустить контейнеры Docker"
	@echo "  migrate           Применить миграции Django"
	@echo "  createsuperuser   Создать суперпользователя Django"
	@echo "  import            Запустить импорт ингредиентов и тэгов"
	@echo "  clean             Очистить неиспользуемые контейнеры и образы"

run:
	$(DOCKER_COMPOSE) up --build

migrate:
	$(DOCKER_EXEC) python manage.py migrate

createsuperuser:
	$(DOCKER_EXEC) python manage.py createsuperuser

import:
	$(DOCKER_EXEC) python manage.py import_data

clean:
	$(DOCKER_COMPOSE) down --rmi all
