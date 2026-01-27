## Data Cleaning API (Flask)

API REST développée avec Flask pour nettoyer automatiquement des fichiers de données
(CSV, Excel, JSON, XML) et retourner un fichier prêt à l’analyse.

## Fonctionnalités

Chargement de fichiers (CSV, Excel, JSON, XML)

Nettoyage automatique :

valeurs manquantes

doublons

valeurs aberrantes (IQR)

normalisation du texte

Normalisation numérique (optionnelle) :

minmax

zscore

robust

Statistiques avant / après nettoyage

Téléchargement du fichier nettoyé

## Structure du projet
DATA_CLEANAPP/
├── app.py
├── routes/
│   ├── clean_route.py
│   └── download_route.py
├── services/
│   ├── data_loader.py
│   ├── data_cleaner.py
│   ├── normalisation.py
│   ├── exportation.py
│   ├── file_registry.py
│   └── pipeline/
│       ├── pipeline_runner.py
│       ├── statistics.py
│       └── validators.py
└── outputs/

## Endpoints
POST /clean

Paramètres (form-data)

file : fichier à nettoyer

normalize : true / false (optionnel)

method : minmax | zscore | robust (optionnel)

Réponse

{
  "statistiques_avant": {...},
  "statistiques_apres": {...},
  "download_url": "/download/<file_id>"
}

GET /download/<file_id>

Télécharge le fichier nettoyé.

## Installation
pip install -r requirements.txt
python app.py


API disponible sur http://127.0.0.1:5000

## Auteur

Alpha Mamadou Douah Barry