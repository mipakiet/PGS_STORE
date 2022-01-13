# PGS_STORE
Web App for selling stuff for employees.</br>
Making with Django 3 framework with python 3.7 and Bootstrap 5 library.

## Installation
Follow commends in cmd
1. python3 -m venv ./venv
2. .\venv\Scripts\activate
3. git clone "https://github.com/River213/PGS_STORE.git"
4. cd .\PGS_STORE\
5. pip install -r .\requirements.txt
6. create file local_setting.py <br/>
   ```
   #local_setting.py
   DEBUG = True
   SECRET_KEY = 'django-insecure-<write secret key>'
   INTERNAL_IPS = ["127.0.0.1"]
   ```
7. py .\manage.py makemigrations
8. py .\manage.py migrate --run-syncdb
9. py .\manage.py runserver
10. Go to http://127.0.0.1:8000/ to check that everything is fine

## Hints

- create admin account via 'python manage.py createsuperuser'


Voilà, project is ready!
