#PGS_STORE
Web App for selling stuff for employees.</br>
Making with Django 3 framework with python 3.7 and Bootstrap 5 library.

##Installation
Follow commends in cmd
1. python3 -m venv ./venv
2. .\venv\Scripts\activate
3. git clone "https://github.com/River213/PGS_STORE.git"
4. pip install -r .\requirements.txt
5. cd .\PGS_STORE\
6. create file local_setting.py <br/>
   ```
   #local_setting.py
   DEBUG = True
   SECRET_KEY = 'django-insecure-<write secret key>'
   ```

7. py .\manage.py makemigrations
8. py .\manage.py migrate
9. pre-commit install
10. py .\manage.py runserver
11. Go to http://127.0.0.1:8000/ to check that everything is fine

##Hints

- create admin account via 'python manage.py createsuperuser'


Voilà, project is ready!
