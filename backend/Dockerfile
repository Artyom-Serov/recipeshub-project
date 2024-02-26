FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY . ./

#RUN python manage.py collectstatic --noinput
#RUN cp -r /app/collected_static/. /backend_static/static/
#RUN python manage.py migrate

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "foodgram.wsgi:application"]
