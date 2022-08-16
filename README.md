# YaMDb | REST API Service 

### Team:
Igor Skoda - @Port-tf (team-lead, developer) 

Vadim Volkovsky - @VadimVolkovsky (developer)

Vladislav Khizhnyak - @cortin34 (developer)

### Description:
YaMDb project colletct user's reviews on films, music, books, and allows to discuss it in comments.

Lists of categories and genres are definated by admin, but it could be increased in a future 

### Key features:
User's registration with verification via confirmation code (send on e-mail)
Custom user's roles, such as: user, moderator, admin
Custom filters by genre and category
Custom JWT Authenctication

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



