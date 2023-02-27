# EPSI-Learning Python

## Launch image et container


```
docker build --build-arg ssh_prv_key="$(cat ~/.ssh/id_ed25519)" -t epsi-python:1.0 .

docker run -tid --name epsi-python-app -p 8080:80 -v /Users/nico/www/EPSI/python-learning/python-app:/usr/src/app epsi-python:1.0
```

## Inside the container - install Fest.

```
pip install --upgrade pip
pip install django
django-admin startproject project
pip install requests
pip install django-chartjs
```

## Test environnement / launch stack

```
cd project
python manage.py runserver

python manage.py createsuperuser
python manage.py makemigrations
python manage.py migrate

```

## app version

```
asgiref==3.6.0
Django==4.1.7
sqlparse==0.4.3

```

```
Username : admin
Email address: admin@yopmail.com
Password : Epsipython1
```


TUTO 

creation d'une app 
quotes => data


app (quotes) va accueillir nos data, a ses routes, son front

API 
https://iexcloud.io/console/
https://iexcloud.io/console/home
https://iexcloud.io/documentation/getting-started/getting-started-with-apperate.html#setting-up-your-workspace

-> worspace name : epsipython


API.GOUV A
https://api.gouv.fr/les-api/base-adresse-nationale
https://api.gouv.fr/les-api/api-geo





git config --global user.name "Lecogoni"
git config --global user.email "giraud.nicolas@me.com"

git clone git@gitlab.com:epsi-learning/python-django-api-data-app.git
git remote add origin git@gitlab.com:epsi-learning/python-django-api-data-app.git



# API public key
# pk_77e5f670937e4fe78c2e49097f8c49c6 