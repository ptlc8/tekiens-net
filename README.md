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

### Arch (btw)

```sh
pacman -S python3 npm
```

Installer un système de gestion de base de données ([arch recommande MariaDB](https://wiki.archlinux.org/title/MySQL)):
```sh
pacman -S mariadb
```

## Installation
```sh
$ cd src
$ chmod 777 data
$ python3 -m venv venv
$ venv/bin/pip install -r requirements.txt
$ cd front
$ npm install
```

### Mise en place de MariaDB

#### Installation et démarrage de MariaDB
```sh
sudo mariadb-install-db --user=mysql --basedir=/usr --datadir=/var/lib/mysql
sudo systemctl enable mariadb.service
sudo systemctl start mariadb.service
sudo mariadb-secure-installation
```
puis suivre les étapes d'installation sécurisée de MariaDB.

#### Création d'un utilisateur
```sh
mariadb -u root -p
CREATE USER 'tekiens_net'@'localhost' IDENTIFIED BY '[PASSWORD]';
GRANT ALL PRIVILEGES ON tekiens_net.* TO 'tekiens_net'@'localhost';
quit
```

#### Création de la BDD
```sh
mariadb -u tekiens_net -p
CREATE DATABASE tekiens_net CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE tekiens_net;
source init.sql # et sample.sql pour un avoir des données d'exemple
SHOW TABLES;
```

Vous devriez avoir un résultat similaire à:

MariaDB [tekiens_net]> SHOW TABLES;
+----------------+
| Tables_in_tekiens_net |
+----------------+
| assos          |
| events         |
| sessions       |
+----------------+
3 rows in set (0.001 sec)

#### Création du dotenv
Créer un fichier `.env` dans le dossier `src` avec les identifiants de la base de données sous la forme suivante :
```
DATABASE_HOST=localhost
DATABASE_USER=tekiens_net
DATABASE_PASS=supermotdepasse
DATABASE_NAME=tekiens_net
```

### Compilation du front-end

```sh
$ cd front
$ npm run build
$ cd ..
```

### Lancement en mode développement
*src/*
```sh
$ venv/bin/python3 -m flask run
```

### Lancement en mode production avec Apache2

```sh
$ apt-get update
$ apt-get install apache2 libapache2-mod-wsgi-py3
$ a2enmod wsgi
$ cp apache2.conf /etc/apache2/sites-available/tekiens-net.conf
$ # edit tekiens-net.conf with your own path
$ a2ensite tekiens-net
$ service apache2 restart
```

Si le projet est servi par un reverse proxy, créer un fichier `.env.local` dans le dossier `src/front` avec le sous-chemin du projet sous la forme suivante :
```properties
VITE_BASE_URL=/sous-chemin
```

## Échantillon de données

Pour ajouter un échantillon de données, exécuter le script `sample.sql` dans la base de données et copier les images du dossier `sample-data` dans le dossier `src/data` :

```sh
$ cp sample-data/* src/data/
$ chown -R www-data:www-data src/data/*
```

## API

Voir [api.md](api.md).
