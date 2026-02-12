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
energy-api-master/
├── app/
│   ├── app.py                    # Точка входа Flask-приложения
│   ├── models.py                 # SQLAlchemy-модели таблиц базы данных
│   ├── error_handlers.py         # Обработчик ошибок
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
├── README.md                      # Документация проекта
├── ERROR_HANDLING_GUIDE.md        # Руководство по обработке ошибок
└── MIGRATION_SUMMARY.md           # Сводка изменений системы ошибок

```
## Валидация данных

API автоматически валидирует все входные данные:

### Компании
- **name** (обязательно) - название компании
- **registration_date** (обязательно) - дата в формате YYYY-MM-DD
- **status** (обязательно) - может быть `active`, `inactive`, `pending`

### Точки поставки
- **name** (обязательно) - название точки
- **company_id** (обязательно) - ID существующей компании
- **connection_date** (обязательно) - дата в формате YYYY-MM-DD
- **max_power_kw** (обязательно) - число (> 0)

### Аренда мощности
- **company_name** (обязательно) - название компании-клиента
- **quantity_power** (обязательно) - число (> 0)

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

Ожидаемый ответ:
```json
{
  "status": "healthy",
  "message": "Energy Supply API is running"
}
```

### 3. Остановка проекта

```bash
docker-compose down
```

## Доступ к инструментам

- **API**: ```http://localhost:5000/api/{endpoint}```
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

**Ответ:**
```json
{
  "status": "healthy",
  "message": "Energy Supply API is running"
}
```

## Запросы, связанные с компаниями

### Получить все компании
```bash
curl http://localhost:5000/api/companies
```

**Ответ:**
```json
[
  {
    "id": 1,
    "name": "ЭнергоПром",
    "registration_date": "2020-01-15",
    "status": "active"
  }
]
```

### Получить компанию по ID
```bash
curl http://localhost:5000/api/companies/1
```

**Ответ (успех):**
```json
{
  "id": 1,
  "name": "ЭнергоПром",
  "registration_date": "2020-01-15",
  "status": "active"
}
```

**Ответ (ошибка):**
```json
{
  "error": "Company with ID 9999 not found",
  "type": "NotFoundError"
}
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

**Ответ (успех):**
```json
{
  "id": 4,
  "name": "Электро+",
  "registration_date": "2024-01-15",
  "status": "active"
}
```

**Ответ (ошибка - отсутствуют поля):**
```json
{
  "error": "Missing required fields: registration_date, status",
  "missing_fields": ["registration_date", "status"]
}
```

**Ответ (ошибка - неверный статус):**
```json
{
  "error": "Invalid status. Must be one of: active, inactive, pending",
  "valid_statuses": ["active", "inactive", "pending"]
}
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

**Ответ (успех):**
```json
{
  "id": 1,
  "name": "ЭнергоПром Обновленный",
  "registration_date": "2020-01-15",
  "status": "active"
}
```

### Удалить компанию
```bash
curl -X DELETE http://localhost:5000/api/companies/1
```

**Ответ (успех):**
```json
{
  "message": "Company deleted successfully",
  "company_id": 1
}
```

**Ответ (ошибка):**
```json
{
  "error": "Company with ID 9999 not found",
  "type": "NotFoundError"
}
```

### Получить статистику компании (хранимая функция)
```bash
curl http://localhost:5000/api/companies/1/statistics
```

**Ответ:**
```json
{
  "company_id": 1,
  "company_name": "ЭнергоПром",
  "total_points": 3,
  "total_power_kw": 3500.0
}
```

## Запросы, связанные с точками поставки

### Получить все точки поставки
```bash
curl http://localhost:5000/api/energy-supply-points
```

**Ответ:**
```json
[
  {
    "id": 1,
    "name": "Точка А1",
    "company_id": 1,
    "connection_date": "2021-03-15",
    "max_power_kw": 1000.0
  }
]
```

### Получить точку поставки по ID
```bash
curl http://localhost:5000/api/energy-supply-points/1
```

**Ответ (успех):**
```json
{
  "id": 1,
  "name": "Точка А1",
  "company_id": 1,
  "connection_date": "2021-03-15",
  "max_power_kw": 1000.0
}
```

**Ответ (ошибка):**
```json
{
  "error": "Energy supply point with ID 9999 not found",
  "type": "NotFoundError"
}
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

**Ответ (успех):**
```json
{
  "id": 6,
  "name": "Точка Г1",
  "company_id": 1,
  "connection_date": "2024-03-15",
  "max_power_kw": 3000.0
}
```

**Ответ (ошибка - отсутствуют поля):**
```json
{
  "error": "Missing required fields: connection_date, max_power_kw",
  "missing_fields": ["connection_date", "max_power_kw"]
}
```

**Ответ (ошибка - неверная мощность):**
```json
{
  "error": "max_power_kw must be greater than 0"
}
```

**Ответ (ошибка - компания не найдена):**
```json
{
  "error": "Company with ID 9999 not found",
  "type": "NotFoundError"
}
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

**Ответ (успех):**
```json
{
  "id": 1,
  "name": "Точка А1 Обновленная",
  "company_id": 1,
  "connection_date": "2021-03-15",
  "max_power_kw": 1200.0
}
```

### Удалить точку поставки
```bash
curl -X DELETE http://localhost:5000/api/energy-supply-points/1
```

**Ответ (успех):**
```json
{
  "message": "Energy supply point deleted successfully",
  "point_id": 1
}
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

**Ответ:**
```json
[
  {
    "id": 1,
    "name": "Точка А1",
    "company_id": 1,
    "connection_date": "2021-03-15",
    "max_power_kw": 1000.0
  }
]
```

## Запросы, связанные с клиентами

### Получить всех клиентов
```bash
curl http://localhost:5000/api/company-clients
```

**Ответ:**
```json
[
  {
    "id": 1,
    "company_name": "Клиент 1",
    "quantity_power": 200.0,
    "energy_supply_point_id": 1
  }
]
```

### Получить клиента по ID
```bash
curl http://localhost:5000/api/company-clients/1
```

**Ответ (успех):**
```json
{
  "id": 1,
  "company_name": "Клиент 1",
  "quantity_power": 200.0,
  "energy_supply_point_id": 1
}
```

**Ответ (ошибка):**
```json
{
  "error": "Company client with ID 9999 not found",
  "type": "NotFoundError"
}
```

### Удалить клиента
```bash
curl -X DELETE http://localhost:5000/api/company-clients/1
```

**Ответ (успех):**
```json
{
  "message": "Company client deleted successfully",
  "client_id": 1
}
```

## Запросы, связанные с функцией аренды мощности

### Успешная аренда мощности (хранимая функция)
```bash
curl -X POST http://localhost:5000/api/energy-supply-points/1/rentals \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "клиент",
    "quantity_power": 100
  }'
```

**Ответ (успех):**
```json
{
  "success": true,
  "message": "Energy successfully rented",
  "client_id": 5,
  "rented_power": 100.0,
  "available_power": 900.0
}
```

**Ответ (ошибка - отсутствуют поля):**
```json
{
  "error": "Missing required fields: quantity_power",
  "missing_fields": ["quantity_power"]
}
```

**Ответ (ошибка - неверная мощность):**
```json
{
  "error": "quantity_power must be greater than 0"
}
```

### Попытка аренды с превышением доступной мощности
```bash
curl -X POST http://localhost:5000/api/energy-supply-points/1/rentals \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "клиент",
    "quantity_power": 10000
  }'
```

**Ответ:**
```json
{
  "error": "Insufficient available power",
  "success": false,
  "message": "Insufficient available power",
  "requested_power": 10000.0,
  "available_power": 800.0
}
```

## Обработка ошибок

API использует централизованную систему обработки ошибок с ответами, в которых содержится описание ошибки.

### Коды ответов

- `200` - Успешный запрос
- `201` - Ресурс успешно создан
- `400` - Неверный запрос (ошибка валидации)
- `404` - Ресурс не найден
- `405` - Метод не разрешен
- `500` - Внутренняя ошибка сервера

### Формат ошибок

Все ошибки возвращаются в едином JSON формате:

#### Базовая ошибка
```json
{
  "error": "Error message",
  "type": "ErrorType"
}
```

#### ValidationError (ошибка валидации)
```json
{
  "error": "Missing required fields: name, status",
  "missing_fields": ["name", "status"]
}
```

#### NotFoundError (ресурс не найден)
```json
{
  "error": "Company with ID 123 not found",
  "type": "NotFoundError"
}
```

#### IntegrityError (нарушение целостности БД)
```json
{
  "error": "Record with this data already exists",
  "type": "IntegrityError",
  "status_code": 400
}
```

#### DatabaseError (ошибка базы данных)
```json
{
  "error": "Database operation failed",
  "type": "DatabaseError",
  "status_code": 500
}
```

### Примеры ошибок

#### Несуществующий ресурс (404)
```bash
curl http://localhost:5000/api/companies/9999
```

**Ответ:**
```json
{
  "error": "Company with ID 9999 not found",
  "type": "NotFoundError"
}
```

#### Отсутствуют обязательные поля (400)
```bash
curl -X POST http://localhost:5000/api/companies \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Тест"
  }'
```

**Ответ:**
```json
{
  "error": "Missing required fields: registration_date, status",
  "missing_fields": ["registration_date", "status"]
}
```

#### Неверный формат даты (400)
```bash
curl -X POST http://localhost:5000/api/companies \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Тест",
    "registration_date": "неверная-дата",
    "status": "active"
  }'
```

**Ответ:**
```json
{
  "error": "Invalid date format. Use YYYY-MM-DD",
  "type": "ValueError",
  "status_code": 400
}
```

#### Неверный статус компании (400)
```bash
curl -X POST http://localhost:5000/api/companies \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Тест",
    "registration_date": "2024-01-15",
    "status": "unknown"
  }'
```

**Ответ:**
```json
{
  "error": "Invalid status. Must be one of: active, inactive, pending",
  "valid_statuses": ["active", "inactive", "pending"]
}
```

#### Мощность должна быть больше нуля (400)
```bash
curl -X POST http://localhost:5000/api/energy-supply-points \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Тест",
    "company_id": 1,
    "connection_date": "2024-01-15",
    "max_power_kw": -100
  }'
```

**Ответ:**
```json
{
  "error": "max_power_kw must be greater than 0"
}
```

#### Нет данных в запросе (400)
```bash
curl -X POST http://localhost:5000/api/companies \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Ответ:**
```json
{
  "error": "No data provided"
}
```
## Лицензия

Этот проект распространяется под лицензией GPL-3. См. файл LICENSE для подробностей.
