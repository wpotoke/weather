# 🌦 Weather — Django-приложение прогноза погоды с кэшированием и API

![Python](https://img.shields.io/badge/Python-3.11.9-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0-green?logo=django)
![PostgreSQL](https://img.shields.io/badge/Postgres-16-blue?logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-cache-red?logo=redis)
![Docker](https://img.shields.io/badge/Docker-ready-blue?logo=docker)

**Weather** — это Django-приложение, которое:

- Получает актуальный прогноз погоды через API Open-Meteo
- Сохраняет информацию о поисках (город, IP, user agent, сессия)
- Использует Redis для кэширования результатов
- Предоставляет REST API для автодополнения и статистики
- Запускается через Docker с PostgreSQL и Redis
- Покрыто юнит-тестами

---

## Стек технологий

- Python 3.11.9
- Django 5.x
- Django REST Framework
- PostgreSQL 16
- Redis
- Docker + Docker Compose
- Pytz + Babel (форматирование даты/времени)
- Unittest + Mock (тестирование)

---

## Установка через Docker

1. **Клонируйте репозиторий:**

```bash
git clone https://github.com/wpotoke/weather.git
cd weather
````

2. **Создайте файл переменных окружения:**

```bash
cp .env.example .env
```

3. **Сгенерируйте SECRET\_KEY (если необходимо):**

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
- вставьте его в .env

4. **Создайте пользователя и базу данных, также передайте права на пользование и укажите кодировку**

```pqsl
CREATE USER your_username WITH PASSWORD 'your_password';
CREATE DATABASE your_databasename OWNER your_username ENCODING 'UTF8' LC_COLLATE 'ru_RU.UTF8' LC_CTYPE 'ru_RU.UTF8' TEMPLATE=template0;
```


5. **Соберите и запустите контейнеры:**

```bash
cd app
docker-compose up --build
```

Приложение будет доступно по адресу: [http://localhost:8000](http://localhost:8000)

---

## 🔗 Основные маршруты

### Главная страница

```http
GET /
```

Позволяет ввести название города и получить прогноз.

---

### API: Автодополнение

```http
GET /api/autocomplete/?query=mos
```

Ответ:

```json
["Moscow", "Mostar"]
```

---

### API: Статистика поиска

```http
GET /api/stats/
```

Ответ:

```json
[
  {"city": "Moscow", "count": 12},
  {"city": "London", "count": 7}
]
```

---

## Кэширование (Redis)

* Используется Redis как кэш-бэкенд
* Ключи вида `weather:<город>` хранят прогноз на **5 минут**
* Настройки кэша можно найти в `settings.py`

---

## Тестирование

```bash
docker-compose exec web python manage.py test
```

Тестируются:

* Модель `CitySearch`
* Рендеринг шаблонов
* API-запросы (успешные, ошибочные, кэшированные)
* Обработка ошибок внешнего API

---


> Тестовое задание выполнено кандидатом **Морозов Данила**
