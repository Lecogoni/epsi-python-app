# EPSI-Learning Python

Dans ce fichier les infos de ce que nous avons utiliser comme coker, cmd d'install pour créerr notre projet.

## Launch image et container

le code du dockerfile ayant permis la création de l'image : epsi-python:1.0, est en bas de cette doc. 
```
docker build --build-arg ssh_prv_key="$(cat ~/.ssh/id_ed25519)" -t epsi-python:1.0 .

docker run -tid --name epsi-python-app -p 8080:80 -v /Users/nico/www/EPSI/python-learning/python-app:/usr/src/app epsi-python:1.0
```

## install faite pour build le projet

```
pip install --upgrade pip
pip install django
django-admin startproject project
pip install requests
pip install django-chartjs
pip install matplot
```


## Dockerfile :

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


