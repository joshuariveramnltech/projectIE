# Students Information System for the Department of Industrial Engineering College of Engineering PUP Main Campus
## Database Management System Final Project


### Installing Dependencies
1. Install  [Python 3.6.X](https://www.python.org/downloads/)
2. Make sure Python 3 is included in your System's Path.
3. Install XAMPP.
4. Create a database and name it `dbie`.
5. Open a terminal inside the project directory and run the following command : 

   `pip install -r requirements.txt`   
   Wait for it to finish installing the dependencies needed..

6. Migrate the databases 

   Run the following commands:   
   `python manage.py makemigrations account`   
   `python manage.py makemigrations administrator`   
   `python manage.py makemigrations grading_system`   
   `python manage.py migrate`

7. When everything is done and dusted, you can now test if it works..

   Run the command: `python manage.py runserver`
   
8. Create your superuser account 
   `python manage.py createsuperuser`   
   This will prompt you to enter your credentials, fill it up completely then   
   go to your localhost:8000.

<br> <br>
---
### Developers:
* ##### [Aira Yllana](https://gitlab.com/AiraYllana)
* ##### Genesis Edano
* ##### Christian Gregorio
* ##### [Joshua Kim Rivera ](https://www.gitlab.com/joshuakimrivera)
* ##### [Kim Sunga](https://gitlab.com/sungakim816)
* ##### [Cristian Umali ](https://gitlab.com/cristianumali.a99)


<br>

---

# Powered by:
## [Django 2.1.2 ](https://www.djangoproject.com/)
## [Materialize 1.0.0](https://materializecss.com/about.html)
# Visit:
## https://project-sis-ie.herokuapp.com/