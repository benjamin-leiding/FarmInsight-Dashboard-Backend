FROM python:3.13-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./django_server /app/
RUN rm -r ./database

RUN pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /app/
RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]