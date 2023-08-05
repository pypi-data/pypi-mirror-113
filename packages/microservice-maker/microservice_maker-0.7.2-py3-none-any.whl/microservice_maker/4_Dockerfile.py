FROM python:[python_version]
ENV PYTHONUNBUFFERED 1

RUN mkdir /[app_name]
WORKDIR /[app_name]

RUN apk add --no-cache --virtual .build-deps \
    ca-certificates gcc postgresql-dev linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev tzdata

COPY requirements.txt /[app_name]/
RUN pip install -r requirements.txt
COPY . /[app_name]/
CMD ["ash", "docker-entrypoint.sh"]
