# Back-end avec Flask et MariaDB/MySQL

## Installation

Les explications se trouvent [dans le README à la racine du projet](../README.md).


## Créer une nouvelle association

Il suffit d'éxécuter le script `create_association.py` en lui passant les arguments nécessaires.

```bash
./create_association.py nouvelle_asso mot2passTroF0r
```

La configuration des informations de l'association se fait ensuite sur la page de modification de l'association.


## Changer un mot de passe

Il suffit d'éxécuter le script `change_password.py` en lui passant les arguments nécessaires.

```bash
./change_password.py -p mot2passTroF0r -i asso_tro_cool
```

Il est aussi possible de changer plusieurs mots de passe en même temps en utilisant un CSV (contenant des lignes de la formes `id_association,nouveau_mot_de_passe`).

```bash
./change_password.py passwords.csv
```