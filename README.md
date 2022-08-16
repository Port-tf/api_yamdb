# YaMDb | REST API Service 

### Team:
- Igor Skoda - @Port-tf (team-lead, developer) 

- Vladislav Khizhnyak - @cortin34 (developer)

- Vadim Volkovsky - @VadimVolkovsky (developer)

### Description:
YaMDb project collects user's reviews on films, music, books.

Users can post reviews on title, rate it (from 1 to 10) and discusss it in comments. 

Current averrage rating is automatically calucatulating in each title.

Lists of categories and genres are definated by admin, but it could be increased in a future.

### Key features:
- User's registration with verification via confirmation code (send on e-mail)
- Custom user's roles, such as: user, moderator, admin
- Custom filters by genre and category
- Custom JWT Authenctication

### How to start:

Clone the repository:
```
git clone git@github.com:Port-tf/api_yamdb.git
```

Change your present working directory (pwd):
```
cd /api_yamdb/
```

Create and activate virtual enviroment:

```
python -m venv venv
```

```
source venv/scripts/activate
```

Update your pip:
```
python3 -m pip install --upgrade pip
```

Install requirements from requirements.txt:

```
pip install -r requirements.txt
```

Make migrations:

```
python manage.py migrate
```

Run the project:

```
python manage.py runserver
```


### Endpoints:

| Endpoint                                   |Request method  | Body                                                  | Response           | Comment               |
|--------------------------------------------|----------------|-------------------------------------------------------|--------------------|-----------------------|
|api/v1/auth/signup/                         |POST            |```{"username": "me","email": "me@mail.ru"}```         | User's information |User's registatration  |
|api/v1/auth/token/                          |POST            |```{"username": "string","confirmation_code": "string"}|``` {"token":eyJ0eXOi}```|                  |
|api/v1/titles/                              |GET             |                                                       | List of titles     |Show list of titles    |
|api/v1/titles/{title_id}/reviews/           |POST            |```{"text": "string","score": 1}```                    |Reviews's info      |Post review and rate a title|


