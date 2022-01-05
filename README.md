#PGS_STORE
Web App for selling stuff for employees.</br>
Making with Django 3 framework with python 3.7 and Bootstrap 5 library.

##Installation
1. Type in cmd "python3 -m venv ./venv"
2. .\venv\Scripts\activate
3. git clone "https://github.com/River213/PGS_STORE.git"
4. pip install -r .\requirements.txt
5. cd .\PGS_STORE\
6. py .\manage.py makemigrations 
7. create file local_setting.py <br/>
   DEBUG = True<br/>
   SECRET_KEY = 'django-insecure-\<write secret key\>'
   
8. py .\manage.py migrate
9. py .\manage.py runserver
10. Go to http://127.0.0.1:8000/ to check that everything is fine

Voilà, project is ready!