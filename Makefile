# Переменные
DOCKER_COMPOSE = docker compose -f docker-compose.production.yml
DOCKER_EXEC = $(DOCKER_COMPOSE) exec backend
OS := $(shell uname)
# Если операционная система - Linux, добавляем sudo
ifeq ($(OS),Linux)
    DOCKER_COMPOSE = sudo docker compose -f docker-compose.production.yml
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
	@echo "  static            Скопировать статические файлы бэкенда"
	@echo "  down              Остановить контейнеры"
	@echo "  clean             Очистить неиспользуемые контейнеры и образы"

run:
	$(DOCKER_COMPOSE) up --build -d

migrate:
	$(DOCKER_EXEC) python manage.py migrate

createsuperuser:
	$(DOCKER_EXEC) python manage.py createsuperuser

import:
	$(DOCKER_EXEC) python manage.py import_data

static:
	$(DOCKER_EXEC) python manage.py collectstatic --noinput
	$(DOCKER_EXEC) cp -r /app/collected_static/. /backend_static/static/

down:
	$(DOCKER_COMPOSE) down

clean:
	$(DOCKER_COMPOSE) down --rmi all
