# Проект YaMDb
Проект собирает отзывы пользователей на кино, фильмы и музыку. Написан в рамках учебного курса Яндекс Практикума.

Проект позволяет управлять постами, комментариями, подписками и группами.

### Технологии
- Библиотека Django REST Framework
- Аутендификация по JWT токену

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Port-tf/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/scripts/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```


## тест внесения изменений VadimVolkovsky