<img src="https://pic.infini.fr/9ISNflin/b9lylW93.png" alt="drawing" width="500"/>

# Tekiens.net

**Tekiens.net** est un site web dédié à la vie étudiante à CY Tech, créé par [Atilla](https://atilla.org). L'objectif de ce site est de centraliser les informations sur les associations et les événements à l'école.

Il propose actuellement un profil pour chaque association permettant de répertorier toutes les informations utile sur l'association et de publier des évènements qui seront à la fois présents sur la page Association et dans la page Evènement qui récapitule tous les évènements en cours ou à venir à CY tech. 
Le site peut aussi générer une mise en forme HTML de mail à partir de template pour aider les association dans leur communication. 

Pour les étudiants, un système de calendrier (ICS) permet d'ajouter le flux des évènements d'une ou plusieurs associations à son calendrier en plus d'un flux RSS.

## Technologies utilisées

Le site utilise actuellement [Flask](https://flask.palletsprojects.com) pour gérer le back-end, en Python donc. 

Le framework javascript [VueJS](https://vuejs.org/) est utilisé pour le front-end.

Et la base de données est gérée en SQL (MySQL/MariaDB).

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

### Windows

Installer:
- [Python](https://www.python.org/downloads/)
- [NodeJS](https://nodejs.org/en/download/prebuilt-installer)
- [Mariadb](https://mariadb.org/download)

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

## Installation 

### Linux(Non nécéssaire avec Nix + direnv)
```sh
$ cd back
$ chmod 777 data
$ python3 -m venv venv
$ venv/bin/pip install -r requirements.txt
$ cd ../front
$ npm install
$ cd ..
```

### Windows
Powershell:
```powershell
PS> cd .\back 
PS> py -3 -m venv venv
PS> .\venv\Scripts\activate  #si script bloqué : "set-executionpolicy remotesigned" dans powershell 
PS> pip install -r .\requirements.txt
```

### Mise en place de MariaDB

#### Installation et démarrage de MariaDB (Hors Windows)
```sh
sudo mariadb-install-db --user=mysql --basedir=/usr --datadir=/var/lib/mysql
sudo systemctl enable mariadb.service
sudo systemctl start mariadb.service
sudo mariadb-secure-installation
```
puis suivre les étapes d'installation sécurisée de MariaDB.

#### Création d'un utilisateur

pour Windows, utiliser ces lignes de commandes avec l'app : "Command Prompt MariaDB" 

```sh
mariadb -u root -p
CREATE USER 'tekiens_net'@'localhost' IDENTIFIED BY '[PASSWORD]';
GRANT ALL PRIVILEGES ON tekiens_net.* TO 'tekiens_net'@'localhost';
quit
```

#### Création de la base de données

pour Windows, utiliser ces lignes de commandes avec l'app : "Command Prompt MariaDB" 

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
| emails                |
| events                |
| sessions              |
+-----------------------+
4 rows in set (0,001 sec)
```

#### Création du dotenv
Créer un fichier `.env` dans le dossier `back` avec les identifiants de la base de données sous la forme suivante :
```sh
DATABASE_HOST=localhost
DATABASE_USER=tekiens_net
DATABASE_PASS=supermotdepasse
DATABASE_NAME=tekiens_net
```

### Mise en place de la connexion au serveur SMTP (optionnel)

Utile pour envoyer les emails pour les événements. Si vous ne voulez pas utiliser cette fonctionnalité, vous pouvez passer cette étape.

#### Informations dans le dotenv

La connexion au serveur smtp se fait grâce aux informations dans le `.env` :

``` sh
SMTP_ADDRESS=<smtp address>   # Exemple: smtp.gmail.com
SMTP_PORT=<smtp port>         # Exemple: 465
SMTP_TLS=true                 # Optionnel, true par défaut
SMTP_USERNAME=<smtp username> # Exemple: foo.bar@example.com
SMTP_PASSWORD=<smtp password>
```

#### Avec gmail

Si vous voulez utiliser le serveur SMTP de gmail et utiliser votre propre adresse gmail, vous ne pourrez pas utiliser votre mot de passe directement dans le `.env`. À la place il faut créer un  [https://myaccount.google.com/apppasswords](mot de passe d'application), de préférence réservé à tekiens.net, et l'utiliser en tant que mot de passe SMTP.

### Compilation du front-end

#### Linux:

```sh
$ cd front
$ npm run build
$ cd ..
```

#### Windows:

Powershell:
```powershell
PS> cd .\front
PS> npm run build
PS> cd ..
```

### Exécution en mode développement

#### Linux:

```sh
$ cd back
$ venv/bin/python3 -m flask run
$ cd ..
```

#### Windows:

Powershell:
```powershell
PS> cd .\back
PS> .\venv\Scripts\activate
PS> python -m flask run
PS> cd ..
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
