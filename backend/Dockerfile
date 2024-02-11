FROM python:3.9

WORKDIR /app

COPY . .
#COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

#RUN python manage.py migrate
RUN python manage.py collectstatic --noinput
#RUN cp -r /app/collected_static/. /app/static/

CMD ["gunicorn", "--bind", "0.0.0.0:7000", "foodgram.wsgi:application"]
