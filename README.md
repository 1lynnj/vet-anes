# Veterinary Anesthesia Protocol BACKEND

A web application to reduce drug calculation errors with veterinary anesthetic protocols. 

Popular tools currently in use:
- blank forms where medical staff manually write in and calculate drug dosages using a calculator
- excel spreadsheets where some calculations can be automated but are prone to user error through spreadsheet interference 

The app goes further by pulling drug interactions from the National Institutes of Health drug interactions API to warn the anesthetist of possible drug interactions. Includes all drugs administered within 12 hours of the anesthetic event and are present in the NIH Database.

## Features

- Allows custom protocols for cats and dogs by entering each required drug and the required dose individually. 
 - Auto populates protocols for healthy cats and dogs with the click of a button.
 - Drug Interactions check from the National Institutes Of Health drug interactions API.
 - Calculates drug dosages for anesthesia, Fentanyl (pain) continuous rate infusion, fluid rates, and emergency drugs.

## Setup and Dependencies

**Create project directory**
```
mkdir <projectname>
cd <projectname>
```
**Create and activate a virtual environment**
```
python3 -m venv ~/venvs/project_venv_name
source ~/venvs/project_name/bin/activate
```
**Create a database**

This project uses postgreSQL but any database can be used with the frontend.

```
psql
create database <databasename>_development;
create user <username> with password '<password>';
alter database <databasename>_development owner to <username>;
\q
```
**Install dependencies**
- Django
- Django Rest Framework
- Django CORS Headers
- Python Dotenv
- Psycopg2pi
- DJ Database URL
- Whitenoise
  
```
pip install django djangorestframework django-cors-headers python-dotenv psycopg2 dj-database-url whitenoise
```
**Start the django project**
```
django-admin startproject <project_name>
```
**Create a Django app in same directory as manage.py**
```
python manage.py startapp <app_name>
```

**Database setup**

On same level as manage.py, creates a .env file and paste the following into it.
```
DATABASE_URL=‘postgres://postgres:postgres@127.0.0.1:5432/<database_name>’
```

In <project_name>/settings.py, update the following to use PostgresSQL
```
import os
import dj-database-url
from dotenv import load_dotenv

load_dotenv()

DATABASES = {
 'default': dj_database_url.config(default=os.environ['DATABASE_URL'], conn_max_age=600)
}
```

**Add CORS**
1. Install library
`pip install django-cors-headers`

2. Add in proper place in your INSTALLED_APPS in settings.py - after the rest_framework and before your application myapp
```
'rest_framework',
'corsheaders',
'myapp.apps.MyAppConfig',
```

3. Allow the origins for your api (inside settings.py)
`CORS_ORIGIN_WHITELIST = ('http://localhost:3000',  # for localhost (REACT Default))`

4. In settings.py, update MIDDLEWARE at top of the list
`'corsheaders.middleware.CorsMiddleware',`

5. In settings.py, confirm 
`CORS_ALLOWED_ORIGINS = ['http://localhost:3000',]`

## Frontend

[Veterinary Anesthesia Protocol - Frontend](https://github.com/1lynnj/vet-anes-front-end)
  
## Future Versions

- Ability by user to add standard protocols to autopopulate form.
- Ability by user to store protocols for individual patients to recall for reference or usage at a later time.
- Ability by user to add drugs to the database.
- User login and authentication to allow above actions.
- Printable document with generated protocol and monitoring grid for use by anesthetist on the medical floor.