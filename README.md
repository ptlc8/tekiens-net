# Tekiens.net

**Tekiens.net** by [Atilla](https://atilla.org), le site de la vie étudiante de CY Tech.
Le but de ce site est de centraliser les informations concernant les associations et les événements de l'école.

## Prérequis

### Linux

```sh
$ apt-get update
$ apt-get install python3 python3-setuptools python3-venv
```

## Installation

```sh
$ cd src
$ python3 -m venv venv
$ venv/bin/pip install flask python-dotenv mysql-connector-python
$ cd front
$ npm install
```

## Compilation du front

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