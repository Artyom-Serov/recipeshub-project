# Переменные
DOCKER_COMPOSE = docker compose -f docker-compose.production.yml
DOCKER_EXEC = $(DOCKER_COMPOSE) exec backend
OS := $(shell uname)
# Если операционная система - Linux, добавляем sudo
ifeq ($(OS),Linux)
    DOCKER_COMPOSE = sudo docker compose -f docker-compose.production.yml
    DOCKER_EXEC = sudo $(DOCKER_COMPOSE) exec backend
    DOCKER_COMPOSE_TEST = sudo docker compose -f backend/docker-compose.database.yml
    DOCKER_COMPOSE_FRONTEND_TEST = sudo docker compose -f frontend/docker-compose.tests.yml
else
    DOCKER_COMPOSE_TEST = docker compose -f backend/docker-compose.database.yml
    DOCKER_COMPOSE_FRONTEND_TEST = docker compose -f frontend/docker-compose.tests.yml
endif
# Цели
.PHONY: help run migrate createsuperuser import static down clean test_backend test_frontend

help:
	@echo "Доступные команды:"
	@echo "  run               Запустить контейнеры Docker"
	@echo "  migrate           Применить миграции Django"
	@echo "  createsuperuser   Создать суперпользователя Django"
	@echo "  import            Запустить импорт ингредиентов и тэгов"
	@echo "  static            Скопировать статические файлы бэкенда"
	@echo "  down              Остановить контейнеры"
	@echo "  test_backend      Запустить тесты бэкенда с PostgreSQL в контейнере"
	@echo "  test_frontend     Запустить тесты фронтенда в контейнере"
	@echo "  clean             Очистить неиспользуемые контейнеры и образы"

run:
	$(DOCKER_COMPOSE) up --build -d

migrate:
	$(DOCKER_EXEC) python manage.py makemigrations && python manage.py migrate

createsuperuser:
	$(DOCKER_EXEC) python manage.py createsuperuser

import:
	$(DOCKER_EXEC) python manage.py import_data

static:
	$(DOCKER_EXEC) python manage.py collectstatic --noinput
	$(DOCKER_EXEC) cp -r /app/collected_static/. /backend_static/static/

test_backend:
	@echo "Запуск контейнера с тестовой БД..."
	$(DOCKER_COMPOSE_TEST) up -d --wait
	@echo "Запуск миграций и тестов..."
	@cd backend && \
		export $$(grep -v '^\s*#' .env.tests | xargs) && \
		python manage.py migrate && \
		python -m pytest; \
		status=$$?; \
		cd .. && $(DOCKER_COMPOSE_TEST) down; \
		exit $$status

test_frontend:
	@echo "Запуск тестов фронтенда..."
	$(DOCKER_COMPOSE_FRONTEND_TEST) run --rm frontend-tests

down:
	$(DOCKER_COMPOSE) down

clean:
	$(DOCKER_COMPOSE) down --rmi all
