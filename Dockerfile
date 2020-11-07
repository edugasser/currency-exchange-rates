FROM python:3.8-alpine

# Install deps necessary for uvloop and postgres
RUN apk add --no-cache build-base postgresql-dev

# Install pipenv
RUN pip3 install pipenv

# Create app directory
RUN mkdir -p /www
WORKDIR /www

# Install app dependencies
COPY requeriments.txt /www/
RUN pip3 install -r requeriments.txt

ENV PYTHONPATH "${PYTHONPATH}:/www/"

COPY . /www

EXPOSE 8000

ENTRYPOINT ["/www/entrypoint.sh"]
