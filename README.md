# Energy Supply API (ES API)

REST API для управления точками поставок энергии. 
Реализован на Python с применением принципов CRUD и ORM.

## Стек проекта

- Python
  - blinker
  - click
  - Flask
  - Flask-SQLAlchemy
  - greenlet
  - itsdangerous
  - Jinja2
  - MarkupSafe
  - psycopg2-binary
  - SQLAlchemy
  - typing_extensions
  - Werkzeug
- PostgreSQL
- Docker

## Структура проекта

```
energy-api/
├── app/
│   ├── app.py                    # Точка входа Flask-приложения
│   ├── models.py                 # SQLAlchemy-модели таблиц базы данных
│   │
│   ├── repositories/             # Абстракция БД
│   │   ├── base.py                # Базовые интерфейсы репозиториев
│   │   ├── company_repository.py  # Репозиторий компаний
│   │   ├── company_client_repository.py
│   │   │                           # Репозиторий клиентов компаний
│   │   └── energy_supply_point_repository.py
│   │                               # Репозиторий точек поставки энергии
│   │
│   ├── services/                 # Бизнес-логика приложения
│   │   ├── company_service.py     # Логика работы с компаниями
│   │   ├── company_client_service.py
│   │   │                           # Логика работы с клиентами компаний
│   │   └── energy_supply_point_service.py
│   │                               # Логика работы с точками поставки 
│   │
│   ├── routes/                   # HTTP-роуты (REST API)
│   │   ├── companies.py           # Эндпоинты для компаний
│   │   ├── company_clients.py     # Эндпоинты для клиентов компаний
│   │   └── energy_supply_points.py
│   │                               # Эндпоинты для точек поставки энергии
│   │
│   └── __init__.py                # Инициализация Python-пакета
│
├── db/
│   └── init.sql                  # SQL-скрипт инициализации БД
│
├── docker-compose.yml             # Конфигурация Docker Compose
├── Dockerfile                     # Docker-образ Flask-приложения
├── requirements.txt               # Python-зависимости проекта
└── README.md                      # Документация проекта

```

## Хранимые функции PostgreSQL

### 1. get_company_statistics
Возвращает статистику по компании: количество точек поставки и суммарную мощность.

### 2. rent_energy
Функция реализует аренду энергии по следующему алгоритму:
1. Проверяет доступную мощность
2. Создает запись о клиенте
3. Возвращает результат операции

### 3. search_energy_supply_points
Возвращает список точек поставки энергии и может искать их по диапазону дат.

## Быстрый старт

### 1. Запуск проекта

```bash
docker-compose up -d
```

### 2. Проверка работоспособности

API доступен по адресу: `http://localhost:5000`

Проверка здоровья:
```bash
curl http://localhost:5000/api/health
```

### 3. Остановка проекта

```bash
docker-compose down
```

## Доступ к инструментам

- **API**: ```http://localhost:5000```
- **pgAdmin**: ```http://localhost:5050``` (admin@admin.com / admin)
- **PostgreSQL**: ```psql -h localhost -U postgres``` (postgres)

## API Endpoints

### Компании

- `GET /api/companies` - список компаний
- `GET /api/companies/{id}` - компания по ID
- `POST /api/companies` - создать компанию
- `PUT /api/companies/{id}` - обновить компанию
- `DELETE /api/companies/{id}` - удалить компанию
- `GET /api/companies/{id}/statistics` - статистика компании

### Точки поставки

- `GET /api/energy-supply-points` - список точек
- `GET /api/energy-supply-points/{id}` - точка по ID
- `POST /api/energy-supply-points` - создать точку
- `PUT /api/energy-supply-points/{id}` - обновить точку
- `DELETE /api/energy-supply-points/{id}` - удалить точку
- `GET /api/energy-supply-points/search?date_from=YYYY-MM-DD&date_to=YYYY-MM-DD` - поиск

### Клиенты

- `GET /api/company-clients` - список клиентов
- `GET /api/company-clients/{id}` - клиент по ID
- `DELETE /api/company-clients/{id}` - удалить клиента

### Аренда мощности

- `POST /api/energy-supply-points/{id}/rentals` - арендовать мощность

## Примеры запросов

### Проверка здоровья API

```bash
curl http://localhost:5000/api/health
```

## Запросы, связанные с компаниями


### Получить все компании
```bash
curl http://localhost:5000/api/companies
```

### Получить компанию по ID
```bash
curl http://localhost:5000/api/companies/1
```

### Создать новую компанию
```bash
curl -X POST http://localhost:5000/api/companies \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Электро+",
    "registration_date": "2024-01-15",
    "status": "active"
  }'
```

### Обновить компанию
```bash
curl -X PUT http://localhost:5000/api/companies/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ЭнергоПром Обновленный",
    "status": "active"
  }'
```

### Удалить компанию
```bash
curl -X DELETE http://localhost:5000/api/companies/1
```

### Получить статистику компании (хранимая функция)
```bash
curl http://localhost:5000/api/companies/1/statistics
```

## Запросы, связанные с точками поставки

### Получить все точки поставки
```bash
curl http://localhost:5000/api/energy-supply-points
```

### Получить точку поставки по ID
```bash
curl http://localhost:5000/api/energy-supply-points/1
```

### Создать новую точку поставки
```bash
curl -X POST http://localhost:5000/api/energy-supply-points \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Точка Г1",
    "company_id": 1,
    "connection_date": "2024-03-15",
    "max_power_kw": 3000
  }'
```

### Обновить точку поставки
```bash
curl -X PUT http://localhost:5000/api/energy-supply-points/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Точка А1 Обновленная",
    "max_power_kw": 1200
  }'
```

### Удалить точку поставки
```bash
curl -X DELETE http://localhost:5000/api/energy-supply-points/1
```

### Поиск точек поставки (хранимая функция)

По всем датам:
```bash
curl "http://localhost:5000/api/energy-supply-points/search"
```

С фильтром по дате от:
```bash
curl "http://localhost:5000/api/energy-supply-points/search?date_from=2020-01-01"
```

С фильтром по диапазону дат:
```bash
curl "http://localhost:5000/api/energy-supply-points/search?date_from=2020-01-01&date_to=2021-12-31"
```

## Запросы, связанные с клиентами

### Получить всех клиентов
```bash
curl http://localhost:5000/api/company-clients
```

### Получить клиента по ID
```bash
curl http://localhost:5000/api/company-clients/1
```

### Удалить клиента
```bash
curl -X DELETE http://localhost:5000/api/company-clients/1
```

## Запросы, связанные с функцией аренды мощности

### Успешная аренда мощности (хранимая функция)
```bash
curl -X POST http://localhost:5000/api/energy-supply-points/1/rentals \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Новый клиент",
    "quantity_power": 100
  }'
```

### Попытка аренды с превышением доступной мощности
```bash
curl -X POST http://localhost:5000/api/energy-supply-points/1/rentals \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Требовательный клиент",
    "quantity_power": 10000
  }'
```

## Запросы для проверки ошибок

### Несуществующий ресурс (404)
```bash
curl http://localhost:5000/api/companies/9999
```

### Неверный формат данных (400)
```bash
curl -X POST http://localhost:5000/api/companies \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Тест"
  }'
```

### Неверный формат даты (400)
```bash
curl -X POST http://localhost:5000/api/companies \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Тест",
    "registration_date": "неверная-дата",
    "status": "active"
  }'
```

## Обработка ошибок

API возвращает JSON с описанием ошибок:

- `400` - неверный запрос
- `404` - ресурс не найден
- `500` - ошибка сервера

Пример:
```json
{
  "error": "Company not found"
}
```
