[![Django-app workflow](https://github.com/johnny-the-dev/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/johnny-the-dev/yamdb_final/actions/workflows/yamdb_workflow.yml)

# yamdb_final
API для работы с сервисом YAMDB, в котором пользователи оставляют свои отзывы о различных произведениях (книги, фильмы, музыка).

## Задействованные технологии

- Python
- Django
- Django Rest Framework
- PostgreSQL
- Docker
- Docker-compose
- Nginx

## Документация по работе с API

Для просмотра документации используйте ендпоинт ```redoc/```

## Старт проекта:
Переменные в файле.env:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<название БД>
POSTGRES_USER=<ваше имя пользователя>
POSTGRES_PASSWORD= <пароль для доступа к БД>
DB_HOST=db
DB_PORT=5432
```
## Автор
**Иван Архипов** - студент курса Python-разработчик на платформе Яндекс.Практикум. Проект является учебным.