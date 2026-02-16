## Data Cleaning API (Flask)

API REST developpee avec Flask pour nettoyer automatiquement des fichiers de donnees
(CSV, Excel, JSON, XML) et retourner un fichier pret a l'analyse.

## Fonctionnalites

- Chargement de fichiers (CSV, Excel, JSON, XML)
- Nettoyage automatique:
  - valeurs manquantes
  - doublons
  - valeurs aberrantes (IQR)
  - normalisation du texte
- Normalisation numerique (optionnelle):
  - minmax
  - zscore
  - robust
- Statistiques avant / apres nettoyage
- Telechargement du fichier nettoye
- Authentification utilisateur (inscription / connexion)

## Structure du projet

DATA_CLEANAPP/
- app.py
- routes/
  - auth_route.py
  - clean_route.py
  - download_route.py
  - history_route.py
- models/
  - clean_history.py
  - user.py
- services/
  - auth.py
  - db.py
  - data_loader.py
  - data_cleaner.py
  - normalisation.py
  - exportation.py
  - file_registry.py
  - pipeline/
    - pipeline_runner.py
    - statistics.py
    - validators.py
- outputs/

## Endpoints

### Auth

POST `/auth/register`

Body JSON:

```json
{
  "username": "alpha",
  "email": "alpha@example.com",
  "password": "motdepasse"
}
```

Contrainte mot de passe pour l'inscription:
- minimum 8 caracteres
- commence par une lettre majuscule
- contient des lettres et des chiffres (caracteres autorises: `A-Z`, `a-z`, `0-9`)

POST `/auth/login`

Body JSON:

```json
{
  "email": "alpha@example.com",
  "password": "motdepasse"
}
```

POST `/auth/logout`

GET `/auth/me`

### Data cleaning

POST `/clean`

Parametres `form-data`:
- `file`: fichier a nettoyer
- `normalize`: `true` / `false` (optionnel)
- `method`: `minmax | zscore | robust` (optionnel)

Reponse:

```json
{
  "statistiques_avant": {},
  "statistiques_apres": {},
  "download_url": "/download/<file_id>"
}
```

POST `/statavant`

GET `/download/<file_id>`

Les routes `/clean`, `/statavant` et `/download/<file_id>` necessitent une connexion utilisateur.

GET `/history`

Retourne l'historique de nettoyage de l'utilisateur connecte:
- `original_filename`
- `cleaned_at`

## Installation

```bash
pip install -r requirements.txt
python app.py
```

Variables d'environnement recommandees:
- `SECRET_KEY` (obligatoire en production)
- `DATABASE_URL` (ex: `sqlite:///users.db`, `postgresql://user:pass@host/dbname`)
- `CORS_ORIGINS` (optionnel, par defaut `*`)

Configuration MySQL (si `DATABASE_URL` n'est pas definie):
- `MYSQL_HOST` (ex: `127.0.0.1`)
- `MYSQL_PORT` (defaut: `3306`)
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_DB`

Exemple MySQL:
```bash
set SECRET_KEY=change-me
set MYSQL_HOST=127.0.0.1
set MYSQL_PORT=3306
set MYSQL_USER=root
set MYSQL_PASSWORD=motdepasse
set MYSQL_DB=data_cleanapp
python app.py
```

API disponible sur `http://127.0.0.1:5000`

## Redeploiement Render

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app` (ou `Procfile` fourni)

Variables minimales a configurer:
- `SECRET_KEY`
- `DATABASE_URL` ou `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DB`
- `CORS_ORIGINS` (optionnel, laissez `*` pour autoriser tous les frontends)

Note:
- L'API utilise une session cookie pour l'authentification.
- Si un frontend doit rester connecte, il doit envoyer les cookies (`credentials/include` selon le client HTTP).

## Auteur

Alpha Mamadou Douah Barry
