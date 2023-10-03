Приложение для Благотворительного фонда поддержки котиков QRKot — фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

Плюс есть возможность формировать таблицу в google sheets

Стек
- python = 3.10.6
- fastapi = 0.78.0
- alembic = 1.7.7
- SQLAlchemy = 1.4.36
- aiogoogle = 4.2.0

Клонировать репозиторий и перейти в него в командной строке:

```
https://github.com/maks-pavlenkov/cat_charity_fund.git
```

```
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* сли у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Запуск проекта
```
uvicorn app.main:app --reload 
```

У проекта есть API для регистрации
- auth/register - POST запрос для регистрации

Тело - 
{
  "email": "user@example.com",
  "password": "string",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}

Ответ апи -
{
  "id": "string",
  "email": "user@example.com",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}

После регистрации можно сделать пожертвование с помощью запроса к
- /donation/ - POST запрос с телом
{
  "comment": "string",
  "full_amount": 0
}

Так же можно выполнить GET запрос для получения всех донатов, которые сделал пользователь

- /donation/my

В ответе будет список из одного или более донатов

[
  {
    "comment": "string",
    "full_amount": 0,
    "id": 0,
    "create_date": "2023-09-29T19:13:13.916Z"
  }
]

Отправить get запрос по endpoint /google/

В результате сформируется ссылка на гугл таблицу
В таблице должны быть закрытые проекты, отсортированные по скорости сбора средств — от тех, что закрылись быстрее всего, до тех, что долго собирали нужную сумму