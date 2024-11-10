FROM python:3.13-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    libpcre3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./django_server /app/

RUN rm -r ./database
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir uwsgi

COPY entrypoint.sh /app/
RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]