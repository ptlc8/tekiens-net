# API Tekiens.net

Cette API permet d'effectuer des opérations sur des associations (assos) et des événements (events) à l'aide de différentes méthodes. Elle prend en charge les opérations de lecture, de mise à jour, d'ajout et de suppression d'associations, d'événements et de sessions.

Les paramètres peuvent être passés dans l'URL ou dans le corps de la requête au format formulaire (x-www-form-urlencoded).


## Sommaire

- [Assos](#assos)
- [Events](#events)
- [Sessions](#sessions)


### Endpoints

| Méthode   | URL                                              | Description                                                           |
|-----------|--------------------------------------------------|-----------------------------------------------------------------------|
| 🔵 GET    | [/api/assos](#-get-apiassos)                     | Récupère toutes les associations                                      |
| 🔵 GET    | [/api/assos/{id}](#-get-apiassosid)              | Récupère l'association avec l'identifiant {id}                        |
| 🟡 PUT    | [/api/assos/{id}](#-put-apiassosid)              | Met à jour l'association avec l'identifiant {id}                      |
| 🔵 GET    | [/api/assos/{id}/events](#-get-apiassosidevents) | Récupère tous les événements de l'association avec l'identifiant {id} |
| 🔵 GET    | [/api/events](#-get-apievents)                   | Récupère tous les événements                                          |
| 🟢 POST   | [/api/events](#-post-apievents)                  | Ajoute un événement                                                   |
| 🔵 GET    | [/api/events/{id}](#-get-apieventsid)            | Récupère l'événement avec l'identifiant {id}                          |
| 🟡 PUT    | [/api/events/{id}](#-put-apieventsid)            | Met à jour l'événement avec l'identifiant {id}                        |
| 🔴 DELETE | [/api/events/{id}](#-delete-apieventsid)         | Supprime l'événement avec l'identifiant {id}                          |
| 🟢 POST   | [/api/sessions](#-post-apisessions)              | Crée une session lié à une association                                |
| 🔵 GET    | [/api/sessions/{id}](#-get-apisessionsid)        | Récupère la session avec l'identifiant {id}                           |
| 🔴 DELETE | [/api/sessions/{id}](#-delete-apisessionsid)     | Supprime la session avec l'identifiant {id}                           |


## Assos

### 🔵 `GET /api/assos`

Récupère toutes les associations.
- Paramètres :
    - campus : filtre les associations par campus (facultatif)
    - before : filtre les associations existantes avant l'année spécifiée (facultatif)
    - after : filtre les associations existantes après l'année spécifiée (facultatif)
    - order : tri les associations, "start" "end" "color" ou "random" (facultatif)
    - desc : tri les associations par ordre décroissant (facultatif)
    - limit : limite le nombre d'associations retournées (facultatif)
- Fonction api.js : `Api.assos.get()` 

### 🔵 `GET /api/assos/{id}`

Récupère l'association avec l'identifiant {id}.
- Paramètres :
    - id : identifiant de l'association
- Fonction api.js : `Api.assos.getOne(id)`

### 🟡 `PUT /api/assos/{id}`

Met à jour l'association avec l'identifiant {id}.
Fonctionne aussi avec la méthode 🟠 PATCH.
- Paramètres :
    - id : identifiant de l'association
    - session : identifiant de la session lié à l'association
    - id : nouvel identifiant de l'association (facultatif)
    - names[] : nouveaux noms de l'association dans l'ordre chronologique (multiple, facultatif)
    - logos[] : nouveaux logos de l'association dans l'ordre chronologique au format URL base64 (multiple, facultatif)
    - start : nouvelle date de début de l'association (facultatif)
    - end : nouvelle date de fin de l'association (facultatif)
    - theme : nouveau thème de l'association (facultatif)
    - campus : nouveau campus de l'association (facultatif)
    - room : nouvelle salle de l'association (facultatif)
    - socials[] : nouveaux réseaux sociaux de l'association (multiple, facultatif)
    - description : nouvelle description de l'association (facultatif)
    - color : nouvelle couleur de l'association (facultatif)
- Fonction api.js : `Api.assos.update(id, asso)`

### 🔵 `GET /api/assos/{id}/events`

Récupère tous les événements de l'association avec l'identifiant {id}.
- Paramètres :
    - id : identifiant de l'association
    - before : filtre les événements avant la date spécifiée, format SQL (facultatif)
    - after : filtre les événements après la date spécifiée, format SQL (facultatif)
    - order : tri les événements, "date" ou "random", (facultatif, par défaut date)
    - desc : tri les événements par ordre décroissant (facultatif)
    - limit : limite le nombre d'événements retournés (facultatif)
- Fonction api.js : `Api.assos.getEvents(id)`


## Events

### 🔵 `GET /api/events`

Récupère tous les événements.
- Paramètres :
    - before : filtre les événements avant la date spécifiée, format SQL (facultatif)
    - after : filtre les événements après la date spécifiée, format SQL (facultatif)
    - order : tri les événements, "date" ou "random", (facultatif, par défaut date)
    - desc : tri les événements par ordre décroissant (facultatif)
    - limit : limite le nombre d'événements retournés (facultatif)
- Fonction api.js : `Api.events.get()`

### 🟢 `POST /api/events`

Ajoute un événement.
- Paramètres :
    - session : identifiant de la session lié à l'association organisant l'événement
    - title : titre de l'événement
    - date : date et heure de l'événement au format SQL
    - place : lieu de l'événement
    - poster : affiche de l'événement au format URL base64 (facultatif)
    - description : description de l'événement (facultatif)
    - duration : durée de l'événement en minutes (facultatif)
    - price : prix de l'événement (facultatif)
    - link : lien de l'événement (facultatif)
    - access : accès à l'événement (facultatif)
    - status : statut de l'événement (programmed, cancelled, rescheduled, full, movedOnline) (facultatif)
    - capacity : capacité de l'événement (facultatif)
- Fonction api.js : `Api.events.create(event)`

### 🔵 `GET /api/events/{id}`

Récupère l'événement avec l'identifiant {id}.
- Paramètres :
    - id : identifiant de l'événement
- Fonction api.js : `Api.events.getOne(id)`

### 🟡 `PUT /api/events/{id}`

Met à jour l'événement avec l'identifiant {id}.
Fonctionne aussi avec la méthode 🟠 PATCH.
- Paramètres :
    - id : identifiant de l'événement
    - session : identifiant de la session lié à l'association organisant l'événement
    - title : titre de l'événement (facultatif)
    - date : date et heure de l'événement au format SQL (facultatif)
    - place : lieu de l'événement (facultatif)
    - poster : affiche de l'événement au format URL base64 (facultatif)
    - description : description de l'événement (facultatif)
    - duration : durée de l'événement en minutes (facultatif)
    - price : prix de l'événement (facultatif)
    - link : lien de l'événement (facultatif)
    - access : accès à l'événement (facultatif)
    - status : statut de l'événement (programmed, cancelled, rescheduled, full, movedOnline) (facultatif)
    - capacity : capacité de l'événement (facultatif)
- Fonction api.js : `Api.events.update(id, event)`

### 🔴 `DELETE /api/events/{id}`

Supprime l'événement avec l'identifiant {id}.
- Paramètres :
    - id : identifiant de l'événement
    - session : identifiant de la session lié à l'association organisant l'événement
- Fonction api.js : `Api.events.delete(id)`


## Sessions

### 🟢 `POST /api/sessions`

#### Demande de connexion

Demande un challenge au serveur pour vérifier le mot de passe.
- Paramètres :
    - asso : identifiant de l'association

Le serveur envoie un challenge (sous forme de chaine de caractères) et le sel du hash bcrypt (sous la forme "$alg$rounds$salt") utilisé pour hasher le mot de passe.
- Réponse :
    - challenge : challenge envoyé par le serveur
    - salt : sel du hash bcrypt


#### Réponse au challenge

Le client doit hacher le mot de passe avec le sel.
Puis hasher ce hash concaténé avec le identifiant de la session identifiant de la session challenge (challenge + bcrypt_hash) avec SHA256.
- Paramètres :
    - asso : identifiant de l'association
    - hash : hash SHA256 du hash bcrypt concaténé avec le challenge : SHA256(challenge + bcrypt_hash)

- Réponse :
    - id : identifiant de la session
    - asso_id : identifiant de l'association


### 🔵 `GET /api/sessions/{id}`

Récupère la session avec l'identifiant {id}.
- Paramètres :
    - id : identifiant de la session
- Fonction api.js : `Api.sessions.getOne(id)`

### 🔴 `DELETE /api/sessions/{id}`

Supprime la session avec l'identifiant {id}.
- Paramètres :
    - id : identifiant de la session
- Fonction api.js : `Api.sessions.delete(id)`
