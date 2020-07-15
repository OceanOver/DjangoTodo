# DjangoTodo

Todo demo built with Django (rest api with Django REST Framework)

## Requirements

- Python3
- Pipenv
- Docker

## Getting started

1. clone the project

   ```bash
   git clone https://github.com/OceanOver/DjangoTodo.git
   cd DjangoTodo
   ```

2. create the virtual environment

   ```bash
   pipenv --three
   pipenv shell
   ```

3. install the dependencies

   ```bash
   pipenv install
   ```

## Run the application

```bash
# start docker services
docker-compose -f docker-compose.dev.yml up -d

# init databash
cd ./init.d
python initdb.py
python manage.py migrate

# run server
python manage.py runserver_plus 0.0.0.0:7009
```
