# Django Blog
Simple blog app created with Django. The main purpose of this project 
was to consolidate knowledge about Django
and learn something about Bootstrap, JavaScript, Redis and PostgreSQL.

[Live version](https://rcybulski.herokuapp.com/)

## Features
* Display posts with infinite scroll
* Filter posts by category
* Markdown editor
* Syntax highlighting
* Posts ranking
* Like and comment posts
* Count views
* Full text search

## Technologies
* Python 3.8
* Django 3
* Bootstrap 4
* Redis
* PostgreSQL

## Setup
To run this project you'll need redis and postgresql server with installed
`pg_trgm` extension.
1. Clone the repository
```
git clone https://github.com/rcybulski1122012/django_blog.git
```
2. Create virtual environment, activate it and install dependencies
```
cd django_blog
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Configure your database and redis connection in `django_blog/setting.py` 
   
4. Run migrations and create superuser
```
python manage.py migrate
python manage.py createsuperuser
```

5. That's all. Now you can run the application
```
python manage.py runserver
```