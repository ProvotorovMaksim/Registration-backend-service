# Registration Backend — регистрация и JWT

## Назначение проекта

Предоставляет регистрацию и вход для приложений, которым нужна единая учётная запись и проверяемый токен.

## Функциональность

Регистрация, вход по email и паролю, чтение текущего профиля и отправка служебных сообщений Kafka.

## Архитектура

`main.py` принимает запросы FastAPI. `db_provider.py` и SQLAlchemy обращаются к PostgreSQL, `my_token.py` выпускает и проверяет JWT, `kafkaproducer.py` пишет служебные сообщения в `multi-partition`.

### С чего начать чтение кода

- [`main.py`](main.py)
- [`my_token.py`](my_token.py)
- [`tests.py`](tests.py)

[Граф связей Graphify](graphify-out/graph.html) · [Отчёт Graphify](graphify-out/GRAPH_REPORT.md)

Для поиска по графу из корня репозитория выполните `graphify god-nodes --top 5` или `graphify query "имя функции или модуля"`.

## Технологический стек

Python 3.11, FastAPI, Pydantic, bcrypt, python-jose, SQLAlchemy, asyncpg, PostgreSQL, Alembic, Confluent Kafka, Docker Compose, TestClient.

## Технические решения

Пароли хешируются bcrypt. Токен содержит `sub`, срок задаётся настройками. Схема БД обновляется стартовым скриптом.

## Запуск проекта

Задайте `DATABASE_URL` как хост и порт PostgreSQL, а также `DATABASE_DRIVER` и параметры `POSTGRES_*`, `JWT_SECRET_KEY`, `ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES`, `KAFKA_BOOTSTRAP_SERVERS` и согласуйте Kafka-настройки с `settings.py`. Подключите Kafka и сеть `saas_network`. Запустите `docker compose up --build`. Хост-порт 8007 проброшен на 8001. Миграции выполняет `entry.sh`.

## Примеры API

`GET /`, `POST /register` с полями username, email, password, `POST /login` с email и password, `GET /me` с Bearer JWT.

```bash
curl -i http://localhost:8007/
```

Следующий запрос предназначен для тестового окружения с подготовленными данными.

```bash
curl -i http://localhost:8007/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"demo@example.test","password":"replace-with-test-password"}'
```

## Тестирование

Команда `python -m pytest tests.py` запускает TestClient-проверки корня, регистрации и входа. Установите pytest и httpx для TestClient. В доступном локальном окружении сборка тестов остановилась из-за отсутствия httpx. Используйте отдельную PostgreSQL и Kafka. Проверка входа ожидает старую форму ответа, тогда как обработчик возвращает структуру LoginResponse.

## Ограничения и дальнейшее развитие

Нужны независимые тестовые данные, негативные сценарии JWT и согласованный формат событий регистрации.

## Мой вклад

TODO — описать свою роль, реализованные компоненты и принятые технические решения.

[Технический обзор проекта](PROJECT_REVIEW.md)
