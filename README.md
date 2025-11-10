# Перед началом работы:

Создайте свой API_KEY в env.prod

# REST-API приложение для справочника.

1. `make start` - Формирование Docker - образа + запуск.
2. `make stop` - Остановка.
3. `make venv` - Создание виртуального окружения
4. `source venv/bin/activate` - Активация виртуального окружения
5. `make install` - Установка зависимостей проекта.
6. `make test` - Тестирование проекта.

## [Документация](http://localhost:8000/docs)

### 1. Поиск всех организаций находящихся в конкретном здании.

```
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/organizations/by-building/<building_id>' \
  -H 'accept: application/json' \
  -H 'X-API-Key: <API_KEY>'
```

### 2. Поиск всех организаций, которые относятся к указанному виду деятельности без вложенности дочерних видов.

```
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/organizations/by-activity/exact?activity_name=<Название вида деятельности>' \
  -H 'accept: application/json' \
  -H 'X-API-Key: <API_KEY>'
```

### 3. Поиск всех организаций, которые относятся к указанному с родительскими и дочерними видами.

```
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/organizations/by-activity/tree?activity_name=<Название вида деятельности>' \
  -H 'accept: application/json' \
  -H 'X-API-Key: <API_KEY>'
```

### 4. Поиск организаций, которые находятся в заданном радиусе относительно указанной точки на карте.

```
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/organizations/search/radius?latitude=<LATITUDE>&longitude=<LONGITUDE>&radius_meters=<РАДИУС В МЕТРАХ>' \
  -H 'accept: application/json' \
  -H 'X-API-Key: <API_KEY>'
```

### 5. Поиск организаций, которые находятся в заданной прямоугольной области относительно указанной точки на карте. список зданий.

```
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/organizations/search/rectangle?min_latitude=<MIN LATITUDE>&min_longitude=<MIN LONGITUDE>&max_latitude=<MAX LONTITUDE>&max_longitude=<MAX LONGITUDE>' \
  -H 'accept: application/json' \
  -H 'X-API-Key: <API_KEY>'
```

### 6. Поиск организации по названию.

```
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/organizations/by-name?organization_name=<ИМЯ ОРГАНИЗАЦИИ>' \
  -H 'accept: application/json' \
  -H 'X-API-Key: <API_KEY>'
```

### 7. Поиск информации об организации по её идентификатору.

```
curl -X 'GET' \
  'http://127.0.0.1:8000/api/v1/organizations/<ORGANIZATION UUID>' \
  -H 'accept: application/json' \
  -H 'X-API-Key: <API_KEY>'
```

# Примеры ответов:

## Поиск организаций по зданиям, по видам деятельности, возвращает JSON ответ в котором только название и номер организации.

```
[
  {
    "title": "Обувной магазин \"Комфорт\"",
    "phones": [
      "+7-999-888-99-00"
    ]
  }
]
```

## Геопоиск возвращает JSON ответ в котором название, здание в котором находится эта организация и номер организации.

```
{
  "organizations": [
    {
      "title": "Мясной дом",
      "phones": [
        "+7-999-111-22-33"
      ],
      "building": {
        "id": "8f36005c-dce1-4e35-9cef-3c96534300f2",
        "address": "ул. Ленина, 1",
        "latitude": 55.7558,
        "longitude": 37.6176
      }
    },
    {
      "title": "Сырная лавка",
      "phones": [
        "+7-999-111-44-55"
      ],
      "building": {
        "id": "8f36005c-dce1-4e35-9cef-3c96534300f2",
        "address": "ул. Ленина, 1",
        "latitude": 55.7558,
        "longitude": 37.6176
      }
    },
```

## Поиск по имени и идентификатору организации возвращает JSON ответ с полной информацией об организации.

```
[
  {
    "id": "6104d295-ec06-4dff-bb9f-38216258a764",
    "title": "Мясной дом",
    "building_id": "8f36005c-dce1-4e35-9cef-3c96534300f2",
    "building": {
      "id": "8f36005c-dce1-4e35-9cef-3c96534300f2",
      "address": "ул. Ленина, 1",
      "latitude": 55.7558,
      "longitude": 37.6176
    },
    "activities": [
      {
        "id": 1,
        "name": "Еда",
        "parent_id": null
      },
      {
        "id": 2,
        "name": "Мясная продукция",
        "parent_id": 1
      },
      {
        "id": 3,
        "name": "Колбасы",
        "parent_id": 2
      }
    ],
    "phones": [
      {
        "id": "31b99416-296c-440f-8713-9144e672f66f",
        "phone_number": "+7-999-111-22-33"
      }
    ]
  }
]
```