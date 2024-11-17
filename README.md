<img src="https://pic.infini.fr/9ISNflin/b9lylW93.png" alt="drawing" width="500"/>

# Tekiens.net

[**Tekiens.net**](https://tekiens.net/) est un site web dédié à la vie étudiante à CY Tech, créé par [Atilla](https://atilla.org). L'objectif de ce site est de centraliser les informations sur les associations et les événements à l'école.

Il propose actuellement un profil pour chaque association permettant de répertorier toutes les informations utile sur l'association et de publier des évènements qui seront à la fois présents sur la page Association et dans la page Evènement qui récapitule tous les évènements en cours ou à venir à CY tech. 
Le site peut aussi générer une mise en forme HTML de mail à partir de template pour aider les association dans leur communication. 

Pour les étudiants, un système de calendrier (ICS) permet d'ajouter le flux des évènements d'une ou plusieurs associations à son calendrier en plus d'un flux RSS.

Vous pouvez aussi rejoindre le [serveur discord](https://discord.gg/yx7ectUSUV) si vous voulez participer au projet!

## Technologies utilisées

- **Back-end** : Le site utilise actuellement [Flask](https://flask.palletsprojects.com) pour gérer le back-end, en Python donc. 

- **Front-end** : Le framework javascript [VueJS](https://vuejs.org/) est utilisé pour le front-end.

- **BDD** : La base de données est gérée en SQL (MySQL/MariaDB).


## Installation 

### Prérequis

- **Debian / Ubuntu** : 
```sh
apt-get update
apt-get install python3 python3-setuptools python3-venv npm
npm install -g n
n stable
apt-get install mariadb-server # ou mysql-server
```

- **Windows** :
    - [Python](https://www.python.org/downloads/)
    - [NodeJS](https://nodejs.org/en/download/prebuilt-installer)
    - [Mariadb](https://mariadb.org/download)

- **Arch** : (btw) 
```sh
pacman -S python3 npm
pacman -S mariadb 
```

- Nix(OS)
Installer direnv (https://direnv.net/) (optionnel)

Commandes utiles :
| Commande        | Description                                         |
| --------------- | --------------------------------------------------- |
| `direnv allow`  | Autorise la configuration du shell automatique      |
| `direnv reload` | Reload le shell                                     |
| `devenv shell`  | Configure le shell (si direnv non installé)         |
| `devenv up`     | Lance tous les processus (mysql, backend, frontend) |

### Mise en place de l'environnement de developpement

- **Linux** : (non nécéssaire avec Nix + direnv)
```sh
cd back
chmod 777 data
python3 -m venv venv
venv/bin/pip install -r requirements.txt
cd ../front
npm install
cd ..
```

- **Windows** : (powershell)
```powershell
cd .\back 
py -3 -m venv venv
.\venv\Scripts\activate  #si script bloqué : "set-executionpolicy remotesigned" dans powershell 
pip install -r .\requirements.txt
cd ..\front
npm install
cd ..
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

```sh
mariadb -u root -p
CREATE USER 'tekiens_net'@'localhost' IDENTIFIED BY '[PASSWORD]';
GRANT ALL PRIVILEGES ON tekiens_net.* TO 'tekiens_net'@'localhost';
quit
```
_pour **Windows**, utiliser ces lignes de commandes avec l'app : "Command Prompt MariaDB"_

#### Création de la base de données

```sh
mariadb -u tekiens_net -p
CREATE DATABASE tekiens_net CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE tekiens_net;
SOURCE init.sql
#SOURCE sample.sql # pour avoir des données d'exemple
SHOW TABLES;
```
_pour **Windows**, utiliser ces lignes de commandes avec l'app : "Command Prompt MariaDB"_

Vous devriez avoir un résultat similaire à :
```
MariaDB [tekiens_net]> SHOW TABLES;
+-----------------------+
| Tables_in_tekiens_net |
+-----------------------+
| assos                 |
| campus                |
| emails                |
| events                |
| sessions              |
+-----------------------+
4 rows in set (0,001 sec)
```

#### Création du dotenv

Créer un fichier `.env` dans le dossier `back` avec les identifiants de la base de données sous la forme suivante :
```
DATABASE_HOST=localhost
DATABASE_USER=tekiens_net
DATABASE_PASS=supermotdepasse
DATABASE_NAME=tekiens_net
```

### Mise en place de la connexion au serveur SMTP (optionnel)

Utile pour envoyer les emails pour les événements. Si vous ne voulez pas utiliser cette fonctionnalité, vous pouvez passer cette étape.

#### Création dans le dotenv

La connexion au serveur smtp se fait grâce aux informations dans le `.env` :
```
SMTP_ADDRESS=<smtp address>   # Exemple: smtp.gmail.com
SMTP_PORT=<smtp port>         # Exemple: 465
SMTP_TLS=true                 # Optionnel, true par défaut
SMTP_USERNAME=<smtp username> # Exemple: foo.bar@example.com
SMTP_PASSWORD=<smtp password>
```

#### Avec gmail

Si vous voulez utiliser le serveur SMTP de gmail et utiliser votre propre adresse gmail, vous ne pourrez pas utiliser votre mot de passe
directement dans le `.env`. À la place il faut créer un  [https://myaccount.google.com/apppasswords](mot de passe d'application), de
préférence réservé à tekiens.net, et l'utiliser en tant que mot de passe SMTP.

## Exécution en mode production

### Back-end

1. Installer Apache2 :
```sh
apt-get update
apt-get install apache2 libapache2-mod-wsgi-py3
```
2. Activer le module WGSI (pour servir une application flask) :
```sh
a2enmod wsgi
chown -R www-data:www-data back/data/*
```
3. Configuration de Apache :
```sh
cp apache2.conf /etc/apache2/sites-available/tekiens-net.conf
# edit tekiens-net.conf with your own path
```
4. Lancer de l'application 
```sh
a2ensite tekiens-net
service apache2 restart
```

Si le projet est servi par un reverse proxy, créer un fichier `.env.local` dans le dossier `front` avec le sous-chemin du projet sous la forme suivante :
```properties
VITE_BASE_URL=/sous-chemin
```

### Front-end

```sh
cd front
npm run build
cd ..
```

## Exécution en mode développement

### Backend

- **Linux** :
```sh
cd back
venv/bin/python3 -m flask run
cd ..
```

- **Windows** : (powershell) 
```powershell
cd .\back
.\venv\Scripts\activate
python -m flask run
cd ..
```

### Front-end

```sh
cd front
npm run dev
```

## Échantillon de données

Pour ajouter un échantillon de données, exécuter le script `sample.sql` dans la base de données et copier les images du dossier `back/data.sample` dans le dossier `back/data` (en veillant à ce que le propriétaire des fichiers soit celui qui exécute le serveur web) :

```sh
cp -r back/data.sample/* back/data/
```

## API

Voir [api.md](api.md).
