version: '3'

services:
  db:
    image: postgres
    container_name: db_[app_name]
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - ./postgres-data:/var/lib/postgresql/data
    ports:
      - "[db_port]:5432"

  django:
    build: ./[app_name]
    env_file: .env
    container_name: django_[app_name]
    volumes:
      - ./[app_name]:/[app_name]
    ports:
      - [app_port]:8000
    depends_on:
      - db
