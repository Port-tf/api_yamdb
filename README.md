# YaMDb | REST API Service 

### Команда:
- Игорь Шкода - @Port-tf (Тим-лид, разработчик) 

- Владислав Хижняк - @cortin34 (разработчик)

- Вадим Волковский - @VadimVolkovsky (разработчик)

### Описание:
Проект YaMDb собирает отзывы пользователей на фильмы, музыку, книги (произведения)

Пользователя могут публиковать отзывы на произведения, оценивать их (по шкале от 1 до 10), и обсуждать отзывы в комментариях

Средний рейтинг каждого произведения рассчитывается автоматически

Список категорий и жанров определен администратором, но может быть расширен в будущем.

### Ключевые особенности:
- Регистрация пользователей происходит путем отправки проверочного кода на e-mail
- Кастомные пользовательские роли: пользователь, модератор, админ
- Кастомная фильтрация по жанру и категориям
- Кастомная аутентификация по JWT токену

### Как запустить проект:

Клонируйте репозиторий:
```
git clone git@github.com:Port-tf/api_yamdb.git
```

Измените свою текущую рабочую дерикторию:
```
cd /api_yamdb/
```

Создайте и активируйте виртуальное окружение

```
python -m venv venv
```

```
source venv/scripts/activate
```

Обновите pip:
```
python3 -m pip install --upgrade pip
```

Установите зависимости из requirements.txt:

```
pip install -r requirements.txt
```

Создайте миграции:

```
python manage.py migrate
```
Запустите сервер:

```
python manage.py runserver
```
Полная документация прокта (redoc) доступна по адресу http://127.0.0.1:8000/redoc/


### Как зарегистрировать пользователя
1. Сделайте POST запрос, укаказав в теле "username" и "email" на эндпоинт "api/v1/auth/signup/"
2. YaMDb отправит проверочный код на указанный email 
3. Сделайте POST запрос указав "email" и "confirmation_code" в теле запроса на эндпоинт  "api/v1/auth/token/"/,в ответе вы получите JWT-токен


### API YaMDb ресурсы:
- AUTH: Аутентификация.
- USERS: Регистрация пользователей/редактирование информации
- TITLES: Произведения и информация о них
- CATEGORIES: Категории произведений (фильмы, музыка, книги)
- GENRES: Жанры. Одно произведение может иметь несколько жанров
- REVIEWS: Отзывы на произведения. Каждый отзыв относится к определенному произведению.
- COMMENTS: Комментарии к отзывам на произведения.


### Эндпоинты:

| Эндпоинт                                   |Тип запроса | Тело запроса                                                  | Ответ           | Комментарий               |
|--------------------------------------------|----------------|-------------------------------------------------------|--------------------|-----------------------|
|api/v1/auth/signup/                         |POST            |```{"username": "me","email": "me@mail.ru"}```         | Информация о пользователе |                |
|api/v1/auth/token/                          |POST            |```{"username": "string","confirmation_code": "string"}|``` {"token":eyJ0eXOi}```|                  |
|api/v1/titles/                              |GET             |                                                       |Список произведения    |Показать список произведений    |
|api/v1/titles/{title_id}/reviews/           |POST            |```{"text": "string","score": 1}```                    |Информация об отзывах     |Разместить отзыв|


