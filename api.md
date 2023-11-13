# API Tekiens.net

Cette API permet d'effectuer des opérations sur des associations (assos) et des événements (events) à l'aide de différentes méthodes. Elle prend en charge les opérations de lecture, de mise à jour, d'ajout et de suppression d'associations et d'événements, ainsi que la fonction de connexion (login).


## Sommaire

- [Assos](#assos)
- [Events](#events)
- [Sessions](#sessions)


### Endpoints

| Méthode   | URL                                                | Description                                                           |
|-----------|----------------------------------------------------|-----------------------------------------------------------------------|
| 🔵 GET    | [/api/assos](#🔵-get-apiassos)                     | Récupère toutes les associations                                      |
| 🔵 GET    | [/api/assos/{id}](#🔵-get-apiassosid)              | Récupère l'association avec l'identifiant {id}                        |
| 🟡 PUT    | [/api/assos/{id}](#🟡-put-apiassosid)              | Met à jour l'association avec l'identifiant {id}                      |
| 🔵 GET    | [/api/assos/{id}/events](#🔵-get-apiassosidevents) | Récupère tous les événements de l'association avec l'identifiant {id} |
| 🔵 GET    | [/api/events](#🔵-get-apievents)                   | Récupère tous les événements                                          |
| 🟢 POST   | [/api/events](#🟢-post-apievents)                  | Ajoute un événement                                                   |
| 🔵 GET    | [/api/events/{id}](#🔵-get-apieventsid)            | Récupère l'événement avec l'identifiant {id}                          |
| 🟡 PUT    | [/api/events/{id}](#🟡-put-apieventsid)            | Met à jour l'événement avec l'identifiant {id}                        |
| 🔴 DELETE | [/api/events/{id}](#🔴-delete-apieventsid)         | Supprime l'événement avec l'identifiant {id}                          |
| 🟢 POST   | [/api/sessions](#🟢-post-apisessions)              | Crée une session lié à une association                                |
| 🔵 GET    | [/api/sessions/{id}](#🔵-get-apisessionsid)        | Récupère la session avec l'identifiant {id}                           |


## Assos

### 🔵 `GET /api/assos`

Récupère toutes les associations.
- Paramètres : aucun
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
    - id : nouvel identifiant de l'association
    - names : nouveaux noms de l'association dans l'ordre chronologique séparés par une virgule
    - logos : nouveaux logos de l'association dans l'ordre chronologique séparés par une virgule
    - start : nouvelle date de début de l'association
    - end : nouvelle date de fin de l'association
    - theme : nouveau thème de l'association
    - campus : nouveau campus de l'association
    - room : nouvelle salle de l'association
    - socials : nouveaux réseaux sociaux de l'association au format JSON
    - description : nouvelle description de l'association
    - color : nouvelle couleur de l'association
- Corps de la requête : association au format JSON
- Fonction api.js : `Api.assos.update(id, asso)`

### 🔵 `GET /api/assos/{id}/events`

Récupère tous les événements de l'association avec l'identifiant {id}.
- Paramètres :
    - id : identifiant de l'association
- Fonction api.js : `Api.assos.getEvents(id)`


## Events

### 🔵 `GET /api/events`

Récupère tous les événements.
- Paramètres : aucun
- Fonction api.js : `Api.events.get()`

### 🟢 `POST /api/events`

Ajoute un événement.
- Paramètres :
    - session : identifiant de la session lié à l'association organisant l'événement
- Corps de la requête : événement au format JSON
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
- Corps de la requête : événement au format JSON
- Fonction api.js : `Api.events.update(id, event)`

### 🔴 `DELETE /api/events/{id}`

Supprime l'événement avec l'identifiant {id}.
- Paramètres :
    - id : identifiant de l'événement
    - session : identifiant de la session lié à l'association organisant l'événement
- Fonction api.js : `Api.events.delete(id)`


## Sessions

### 🟢 `POST /api/sessions`

Crée une session lié à une association.
- Paramètres :
    - username : identifiant de l'association
    - password : mot de passe
- Fonction api.js : `Api.login(username, password)`

### 🔵 `GET /api/sessions/{id}`

Récupère la session avec l'identifiant {id}.
- Paramètres :
    - id : identifiant de la session
- Fonction api.js : `Api.sessions.getOne(id)`