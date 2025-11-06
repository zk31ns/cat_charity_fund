# QRKot

Приложение собирает пожертвования в воображаемый фонд QRKot на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается. Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.


## 🛠 Технологии

### Backend Framework
[![FastAPI](https://img.shields.io/badge/FastAPI-0.78.0-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Starlette](https://img.shields.io/badge/Starlette-0.19.1-FF5500?logo=fastapi&logoColor=white)](https://www.starlette.io/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-0.17.6-5A9E4D?logo=uvicorn&logoColor=white)](https://www.uvicorn.org/)

### База данных
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4.36-D71F00?logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/Alembic-1.7.7-000000?logo=alembic&logoColor=white)](https://alembic.sqlalchemy.org/)
[![aiosqlite](https://img.shields.io/badge/aiosqlite-0.17.0-003B57?logo=sqlite&logoColor=white)](https://github.com/omnilib/aiosqlite)

### Аутентификация и пользователи
[![FastAPI Users](https://img.shields.io/badge/FastAPI_Users-10.0.4-009688?logo=fastapi&logoColor=white)](https://fastapi-users.github.io/fastapi-users/)
[![PyJWT](https://img.shields.io/badge/PyJWT-2.3.0-000000?logo=jsonwebtokens&logoColor=white)](https://pyjwt.readthedocs.io/)

### Валидация данных
[![Pydantic](https://img.shields.io/badge/Pydantic-1.9.1-3776AB?logo=python&logoColor=white)](https://pydantic-docs.helpmanual.io/)

### Тестирование
[![Pytest](https://img.shields.io/badge/Pytest-7.1.3-EA3D0D?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![pytest-asyncio](https://img.shields.io/badge/pytest--asyncio-0.23.4-3776AB?logo=python&logoColor=white)](https://pytest-asyncio.readthedocs.io/)

### Интеграции
[![Google Sheets API](https://img.shields.io/badge/Google_Sheets_API-v4-34A853?logo=googlesheets&logoColor=white)](https://developers.google.com/sheets/api)
[![Aiogoogle](https://img.shields.io/badge/Aiogoogle-4.2.0-4285F4?logo=google&logoColor=white)](https://github.com/omarryhan/aiogoogle)

## 🚀 Локальный запуск проекта

Клонировать репозиторий и перейти в директорию проекта:

```bash
git clone git@github.com:zk31ns/cat_charity_fund.git
```

```bash
cd cat_charity_fund
```

Создать `.env` файл с переменными окружения:

```
CAT_FUND_SECRET = '...'
CAT_FUND_FIRST_SUPERUSER_EMAIL = '...'
CAT_FUND_FIRST_SUPERUSER_PASSWORD = '...'
CAT_FUND_DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
```

Cоздать и активировать виртуальное окружение:

```bash
python -m venv venv
```

```bash
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

Выполнить миграции:

```bash
alembic upgrade head
```

Запустить приложение:

```bash
uvicorn app.main:app --reload
```

## Подключение отчёта в Google Sheets

### 🚀 Создать проект для работы с API платформы Google Cloud
[Перейдите на консоль разработчика](https://console.cloud.google.com/projectselector2/home/dashboard) (дашборд) → Нажмите кнопку `Create Project` → Задайте имя проекту → Нажмите кнопку `Create`

### 🔌 Подключить Google Drive API и Google Sheets API к созданному проекту
- На плитке `APIs` нажмите `Go to APIs` overview
- Нажмите `Enabled APIs and services` или выберите в меню слева пункт `Library`
- В открывшемся окне выберите по очереди Google Drive API и Google Sheets API

### 👤 Создать сервисный аккаунт
- Перейдите в раздел `Credentials`
- Нажмите `Create credentials` и выберите пункт `Service account`
- Заполните поля `Service account name`, `Service account ID`, `Service account description`
- Выберите роль для сервисного аккаунта
- Назначьте права администратора вашему пользовательскому аккаунту

### 🔑 Получить JSON-файл с ключом доступа к сервисному аккаунту
Перейдите на экран `Credentials/<название вашего сервисного аккаунта>` → Нажмите `Keys` → `Add Key` → `Create New Key` → Выберите формат JSON → Нажмите `Create`

### ⚙️ Добавить ключ и email Google-аккаунта в переменные окружения
- Сохраните `JSON-файл` в корне проекта
- Заполните файл `.env` следующими данными из JSON-файла:

```
CAT_FUND_TYPE='...'
CAT_FUND_PROJECT_ID='...'
CAT_FUND_PRIVATE_KEY_ID='...'
CAT_FUND_PRIVATE_KEY='...'
CAT_FUND_CLIENT_EMAIL='...'
CAT_FUND_CLIENT_ID='...'
CAT_FUND_AUTH_URI='...'
CAT_FUND_TOKEN_URI='...'
CAT_FUND_AUTH_PROVIDER_X509_CERT_URL='...'
CAT_FUND_CLIENT_X509_CERT_URL='...'
CAT_FUND_EMAIL='...'
```

## 📡 Примеры запросов к API
С примерами запросов можно ознакомиться после запуска проект по **ссылкам**:

[![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)](http://127.0.0.1:8000/docs/)
[![ReDoc](https://img.shields.io/badge/-ReDoc-%23000000?style=for-the-badge&logo=read-the-docs&logoColor=white)](http://127.0.0.1:8000/redoc/)


## 📞 Контакты
**Автор:** [Давыдов Александр](https://github.com/zk31ns)

[![GitHub](https://img.shields.io/badge/GitHub-%23000000?style=flat&logo=github&logoColor=white)](https://github.com/zk31ns)
[![Telegram](https://img.shields.io/badge/Telegram-%2300A9E0?style=flat&logo=telegram&logoColor=white)](https://t.me/zk31ns)