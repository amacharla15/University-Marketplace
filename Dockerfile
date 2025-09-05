
FROM python:3.12.6


ENV DJANGO_SETTINGS_MODULE=university_marketplace.settings_gcp


ENV DB_HOST=34.168.133.231 \
    DB_NAME=my_django_db \
    DB_USER=my_django_user \
    DB_PASSWORD=Akshay@1524 \
    DB_PORT=5432


WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt



COPY . .



EXPOSE 80

ENTRYPOINT ["./docker_run_server.sh"]
