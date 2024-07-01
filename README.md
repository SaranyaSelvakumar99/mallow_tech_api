# mallow_tech_api
Mallowtech Store
Django rest framework

Installation
First ensure you have python globally installed in your computer. 

Install IDE
Install VisualStudio Code in your computer. 

Setup
After doing this, confirm that you have installed virtualenv globally as well.

$ pip install virtualenv
Create a virtual environment
$ python -m venv env
& source .\env\Scripts\activate

Then, Git clone this repo to your PC
$ git clone https://github.com/SaranyaSelvakumar99/mallow_tech_api.git
$ cd mallow_tech_api

Install dependancies
$ pip install -r requirements.txt

Add configuration file in project main directory with name .env (will shre the separately)

Make migrations & migrate
$ python manage.py makemigrations app_name && python manage.py migrate app_name

Create Super user
$ python manage.py createsuperuser

Launching the app
$ python manage.py runserver

Run Tests
$ python manage.py test
