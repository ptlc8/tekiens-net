# Tekiens.net

**Tekiens.net** est un site web dédié à la vie étudiante à CY Tech, créé par [Atilla](https://atilla.org). L'objectif de ce site est de centraliser les informations sur les associations et les événements à l'école.

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

### Nix(OS)

Installer direnv (https://direnv.net/) (optionnel)

Commandes utiles :
| Commande | Description |
| --- | --- |
| `direnv allow` | Autorise la configuration du shell automatique |
| `direnv reload` | Reload le shell |
| `devenv shell` | Configure le shell (si direnv non installé) |
| `devenv up` | Lance tous les processus (mysql, backend, frontend) |

## Installation (Non nécéssaire avec Nix + direnv)
```sh
$ cd back
$ chmod 777 data
$ python3 -m venv venv
$ venv/bin/pip install -r requirements.txt
$ cd ../front
$ npm install
$ cd ..
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

#### Création de la base de données
```sh
mariadb -u tekiens_net -p
CREATE DATABASE tekiens_net CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE tekiens_net;
SOURCE init.sql
#SOURCE sample.sql # pour avoir des données d'exemple
SHOW TABLES;
```

Vous devriez avoir un résultat similaire à:

```
MariaDB [tekiens_net]> SHOW TABLES;
+-----------------------+
| Tables_in_tekiens_net |
+-----------------------+
| assos                 |
| events                |
| sessions              |
+-----------------------+
3 rows in set (0.001 sec)
```

#### Création du dotenv
Créer un fichier `.env` dans le dossier `back` avec les identifiants de la base de données sous la forme suivante :
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

### Exécution en mode développement

```sh
$ cd back
$ venv/bin/python3 -m flask run
$ cd ..
```

### Exécution en mode production avec Apache2

```sh
$ apt-get update
$ apt-get install apache2 libapache2-mod-wsgi-py3
$ a2enmod wsgi
$ chown -R www-data:www-data back/data/*
$ cp apache2.conf /etc/apache2/sites-available/tekiens-net.conf
$ # edit tekiens-net.conf with your own path
$ a2ensite tekiens-net
$ service apache2 restart
```

Si le projet est servi par un reverse proxy, créer un fichier `.env.local` dans le dossier `front` avec le sous-chemin du projet sous la forme suivante :
```properties
VITE_BASE_URL=/sous-chemin
```

## Échantillon de données

Pour ajouter un échantillon de données, exécuter le script `sample.sql` dans la base de données et copier les images du dossier `back/data.sample` dans le dossier `back/data` (en veillant à ce que le propriétaire des fichiers soit celui qui exécute le serveur web) :

```sh
$ cp -r back/data.sample/* back/data/
```

## API

Voir [api.md](api.md).
