# Data Cleaning API (Flask)

API REST pour le nettoyage automatique de données.

## Fonctionnalités
- Import CSV, Excel, JSON, XML
- Gestion des valeurs manquantes
- Suppression des doublons
- Détection et correction des outliers (IQR)
- Normalisation des données
- Export du fichier nettoyé avec le même nom

## Technologies
- Flask
- Pandas
- NumPy
- Scikit-learn

## Lancer l’API

```bash
pip install -r requirements.txt
python app.py
