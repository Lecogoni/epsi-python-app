# EPSI-Learning Python

## Launch image et container

le code du dockerfile ayant peremis la création de l'image : epsi-python:1.0, est en bas de cette doc. 
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
certifi==2022.12.7
charset-normalizer==3.0.1
Django==4.1.6
idna==3.4
Pillow==9.4.0
requests==2.28.2
sqlparse==0.4.3
urllib3==1.26.14

```

## code d'accès au BO

```
Username : admin
Email address: admin@yopmail.com
Password : Epsipython1
```



API 
https://iexcloud.io/console/
https://iexcloud.io/console/home
https://iexcloud.io/documentation/getting-started/getting-started-with-apperate.html#setting-up-your-workspace

-> worspace name : epsipython


API.GOUV A
https://api.gouv.fr/les-api/base-adresse-nationale
https://api.gouv.fr/les-api/api-geo


Dockerfile :

```
FROM python:3.10

# Add ssh private key into container
ARG ssh_prv_key
ARG ssh_pub_key

# Authorize SSH Host
RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh && \
    ssh-keyscan github.com > /root/.ssh/known_hosts

# Add the keys and set permissions
RUN echo "$ssh_prv_key" > /root/.ssh/id_rsa && \
    echo "$ssh_pub_key" > /root/.ssh/id_rsa.pub && \
    chmod 600 /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa.pub

# set Workdir
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
```


