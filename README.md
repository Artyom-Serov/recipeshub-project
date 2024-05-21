# Проект Foodgram

«Фудграм» — это сайт, на котором можно публиковать собственные рецепты, добавлять чужие рецепты в избранное, подписываться на других авторов и создавать список покупок для заданных блюд.

Вот, что было сделано в ходе работы над проектом:
* настроено взаимодействие Python-приложения с внешними API-сервисами;
* создан собственный API-сервис на базе проекта Django;
* подключено SPA к бэкенду на Django через API;
* созданы образы и запущены контейнеры Docker;
* созданы, развёрнуты и запущены на сервере мультиконтейнерные приложения;

## Технологии:
<img height="32" width="32" src="https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/python.svg" /> <img height="32" width="32" src="https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/django.svg" /> 
<img height="32" width="32" src="https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/dotenv.svg" />
<img height="32" width="32" src="https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/postgresql.svg" />
<img height="32" width="32" src="https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/gunicorn.svg" />
<img height="32" width="32" src="https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/nginx.svg" />
<img height="32" width="32" src="https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/docker.svg" />
<img height="32" width="32" src="https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/git.svg" />
<img height="32" width="32" src="https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/make.svg" />
<img height="32" width="32" src="https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/react.svg" />
<img height="32" width="32" src="https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/json.svg" />
<img height="32" width="32" src="https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/linux.svg" />
<img height="32" width="32" src="https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/postman.svg" />
* [Python 3.10](https://docs.python.org/3.10/)
* [Django 4.2.7](https://www.djangoproject.com/)
* [Django REST Framework 3.14.0](https://www.django-rest-framework.org/)
* [PostgreSQL](https://www.postgresql.org/)
* [gunicorn 21.2.0](https://docs.gunicorn.org/en/stable/)
* [Nginx](https://nginx.org/)
* [Docker](https://www.docker.com/)
* [React](https://ru.react.js.org/)
* [JSON](https://www.json.org)
* [Postman](https://www.postman.com/)


## Размещение и запуск проекта на сервере.
### Клонировать репозиторий и перейти в него <img height="32" width="32" src="https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/git.svg" />:
```
git clone https://github.com/Artyom-Serov/foodgram-project-react.git
```
```
cd foodgram-project-react
```
Внести данные в файл `.env.example` и переименовать его в `.env` <img height="32" width="32" src="https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/dotenv.svg" />.

Выполнить установку и настройку nginx и файрвола <img height="32" width="32" src="https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/linux.svg" />:
* `sudo apt install nginx -y`
* `sudo systemctl start nginx`
* `sudo ufw allow 'Nginx Full'`
* `sudo ufw allow OpenSSH`
* `sudo ufw enable`

### Настраиваем конфигурации nginx на сервере <img height="32" width="32" src="https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/nginx.svg" />:
выполнив команду `sudo nano /etc/nginx/sites-enabled/default` в файле оставляем только следующие параметры
```
server {
    listen 80;
    listen [::]:80;
    server_tokens off;

    server_name <IP-адрес сервера> <доменное имя>;

    location / {
        proxy_pass http://127.0.0.1:8000;

        proxy_set_header Upgrade           $http_upgrade;
        proxy_set_header Connection        "upgrade";
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host  $host;
        proxy_set_header X-Forwarded-Port  $server_port;
    }
}
```
Сохраняем изменения (`Ctrl+s`), выходим из редактора (`Ctrl+x`) и проверяем корректность настроек:
```
sudo nginx -t
```
Перезапускаем nginx для применения изменений:
```
sudo systemctl reload nginx
```
### Устанавливаем и настраиваем Docker <img height="32" width="32" src="https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/docker.svg" />:
* `sudo apt update`
* `sudo apt install curl`
* `curl -fSL https://get.docker.com -o get-docker.sh`
* `sudo sh ./get-docker.sh`
* `sudo apt-get install docker-compose-plugin`

Запускаем проект <img height="32" width="32" src="https://cdn.jsdelivr.net/npm/simple-icons@v11/icons/make.svg" />:
```
make run
```

После выполнения команды проект запустится в docker-контейнерах, создадутся таблицы в базе данных и база данных заполнится интгредиентами и тэгами
* Примечание: можно ознакомиться со списком доступных команд выполнив `make help`

Проект будет доступен по адресу 
```
http://localhost:8000/
```
Ознакомительная версия проекта доступна по адресу:

[Продуктовый помошник](https://foodgramm-react.sytes.net)

##### Не забудьте поставить "звездочку" :wink:
