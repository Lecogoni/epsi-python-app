# EPSI PYTHON DJANGO APP

## Présentation

Ceci est le repo du groupe composé de : 

Samir BESSOLTANE
Jeremy BRUZAC 
Thierry FERCHICHI
Nicolas GIRAUD


Notre projet constiste en une petite application en python developpé avec le framework Django. 
Le but de ce projet est de nous initier à la manipulation de data, la connexion a une API et le stockage de données en base de données.

<<<<<<< HEAD
## code d'accès au BO

cd project
python manage.py runserver


http://127.0.0.1:8000

## code d'accès au BO

```
Username : admin ET root
Email address: admin@yopmail.com
Password : Epsipython1 (même password pour les deux)
```
=======
## Installation du projet

> Afin d'installer le projet de notre groupe vous avez besoin de suivre les instructions suivantes:

- Pensez tout d'abord à être dans un répertoire où vous avez les droits conséquents à la lecture et écriture

- Commencez par installer docker sur votre machine, au besoin voici un lien pour la documentation de l'installation de docker [lien]

- Une fois docker installé, créer un fichier Dockerfile avec les informations suivantes :

```docker
FROM python:latest

RUN mkdir ~/python
WORKDIR ~/python/

RUN apt update && apt install -y git

RUN pip install django

WORKDIR ~/python/

EXPOSE 8000
```

- Executer la commande docker suivante, dans votre terminal dans le répertoire où se trouve le fichier Dockerfile :

```bash
docker build -t epsi-B3C1-py-nGtFsBjB:1.0 .
```

- Puis executer la commande suivante pour lancer le container python :

```bash
docker run -dti --name epsi_python_B3C1_nGtFsBjB -p 8000:8000 epsi-B3C1-py-nGtFsBjB:1.0
```
- Une fois le container en route, il vous sera possible d'enter à l'interieur de l'environnement python avec la commande suivante :

```bash
docker exec -ti epsi_python_B3C1_nGtFsBjB bash
```

- Lorsque vous êtes dans le container executer la suite d'instruction suivante pour télécharger le projet et installer les dépendances :

```bash
mkdir ~/python
cd ~/python
git clone https://github.com/Lecogoni/epsi-python-app.git .
cd project
pip install -r requirement.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```
> Note : Il est possible que les commandes python ne passent pas, essayer avec "python3" ou "py" à la place de "python". Similitude possible avec l'instruction "pip".

> Note d'installation : Il faut vérifier que vous êtes bien dans le dossier "project" pour correctement executer les commandes pip & python. Si lors du "python manage.py runserver 0.0.0.0:8000" une erreur de dépandance survient faite un "python freeze > requirement.txt" puis de nouveau un "pip install -r requirement.txt" dans le répertoire "project"

L'application est maintenant disponible à l'adresse suivante : http://127.0.0.1:8000/

> Une bar de navigation est disponible pour ce déplacer sur les différentes parties du projet, la page d'accueil contient plus d'informations sur ces différentes parties.

## Back-Office

- Un accès à la base de donnée et au back-office du projet Python Django est disponible avec les informations suivantes:

- Aller à l'adresse suivante : http://127.0.0.1:8000/admin/

- Saisir les informations suivantes :

```
Username(2 comptes) : admin / root
Email address: admin@yopmail.com
Password : Epsipython1 (même password pour les deux)
```

Trois tables sont disponibles "Curencys" qui contient les monnaies de l'API monnaitare, "Regions" qui contient la liste des régions et département qui l'a compose et enfin une table "Weather" qui contient la météo.
>>>>>>> @{-1}
