# Tekiens.net

**Tekiens.net** by [Atilla](https://atilla.org), le site de la vie étudiante de CY Tech.
Le but de ce site est de centraliser les informations concernant les associations et les événements de l'école.

## Prérequis

### Debian / Ubuntu

```sh
$ apt-get update
$ apt-get install python3 python3-setuptools python3-venv npm
$ npm install -g n
$ n stable
```
Installer un système de gestion de base de données :
```sh
$ apt-get install mariadb-server
```
ou
```sh
$ apt-get install mysql-server
```

## Installation

```sh
$ cd src
$ python3 -m venv venv
$ venv/bin/pip install flask python-dotenv mysql-connector-python ics
$ cd front
$ npm install
```

Créer une base de données et y exécuter le script `init.sql`.

Créer un fichier `.env` dans le dossier `src` avec les identifiants de la base de données sous la forme suivante :
```properties
DATABASE_HOST=localhost
DATABASE_USER=tekiens_net
DATABASE_PASS=supermotdepasse
DATABASE_NAME=tekiens_net
```

## Compilation du front-end

```sh
$ cd front
$ npm run build
$ cd ..
```

## Lancement en mode développement

```sh
$ venv/bin/python3 -m flask run
```

## Lancement en mode production avec Apache2

```sh
$ apt-get update
$ apt-get install apache2 libapache2-mod-wsgi-py3
$ a2enmod wsgi
$ cp apache2.conf /etc/apache2/sites-available/tekiens-net.conf
$ # edit tekiens-net.conf with your own path
$ a2ensite tekiens-net
$ service apache2 restart
```

Si le projet est servi par un reverse proxy, créer un fichier `.env` dans le dossier `src/front` avec le sous-chemin du projet sous la forme suivante :
```properties
PUBLIC_URL=/sous-chemin
```