
## ✅ `README.md`

# 🌦 Weather — Django-приложение прогноза погоды с кэшированием и API

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0-green?logo=django)
![PostgreSQL](https://img.shields.io/badge/Postgres-16-blue?logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-cache-red?logo=redis)
![Docker](https://img.shields.io/badge/Docker-ready-blue?logo=docker)

Это Django-приложение, которое:

- Получает актуальный погодный прогноз с помощью API Open-Meteo
- Сохраняет данные о поиске (город, IP, user agent, сессия)
- Использует Redis для кэширования погоды
- Предоставляет REST API для автодополнения и статистики
- Запускается через Docker и PostgreSQL
- Покрыто юнит-тестами

---

## 🚀 Стек технологий

- Python 3.12
- Django 5.x
- Django REST Framework
- PostgreSQL 16
- Redis
- Docker + Docker Compose
- Pytz + Babel (формат даты/времени)
- Unittest + Mock для тестирования

---

## 📦 Установка через Docker

```bash
git clone https://github.com/wpotoke/weather.git
cd app
docker-compose up --build
````

После запуска приложение будет доступно по адресу:
👉 [http://localhost:8000](http://localhost:8000)

---

## ⚙️ Переменные окружения

Создай `.env` в корне проекта:

```env
SQL_USER=postgres
SQL_PASSWORD=yourpassword
SQL_DATABASE=weather_db
DJANGO_SECRET_KEY=your_secret_key
DEBUG=True
```

---

## 🔗 Основные маршруты

### 🌍 Главная страница

```http
GET /
```

Позволяет ввести название города, получить прогноз и отображает погоду.

---

### 🔍 API: Автодополнение

```http
GET /api/autocomplete/?query=mos
```

Ответ:

```json
["Moscow", "Mostar"]
```

---

### 📊 API: Статистика поиска

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

## 🧠 Кэширование (Redis)

* Используется Redis как кэш-бэкенд
* Ключи вида `weather:<город>` хранят прогноз на 5 минут
* Настройка в `settings.py`:

---

## 🧪 Тестирование

```bash
docker-compose exec web python manage.py test
```

Тестируются:

* Модель `CitySearch`
* Отображение шаблонов
* Поведение при запросах API (успешные, ошибочные, кэш)
* Обработка ошибок внешнего API

---

> Тестовое задание выполнено кандидатом **Морозов Данила**


