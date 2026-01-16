#ce fichier nous permet d'effectuer des calculs de toutes les stats que contient le fichier uploader
#et sera appelé par pipeline_runner.py(notre fichier orchestre)

import pandas as pd
import numpy as np

def valeurs_abber(df):
    numeric_cols = df.select_dtypes(include= np.number).columns
    numeric_cols = [col for col in numeric_cols if df[col].nunique() > 2]
    valeur_abberante = 0
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3-Q1

        lower = Q1 - 1.5*IQR
        upper = Q3 + 1.5*IQR
        valeur_abberante += ((df[col] < lower) | (df[col] > upper)).sum()
    return int(valeur_abberante)

def calcul_statt(df):
    
    nb_de_lignes = int(df.shape[0])
    nb_de_colonnes = int(df.shape[1])
    nb_valeur_manquantes = int(df.isna().sum().sum())
    nb_valeurs_abberantes = valeurs_abber(df)
    nb_doublons = int(df.duplicated().sum())
    nb_de_colonnes_numerics = int(len(df.select_dtypes(include= np.number).columns))
    nb_de_colonnes_texte = int(len(df.select_dtypes(include="object").columns))
    return {
        "nb_de_lignes": nb_de_lignes,
        "nb_de_colonnes": nb_de_colonnes,
        "nb_valeur_manquantes": nb_valeur_manquantes,
        "nb_valeurs_abberantes": nb_valeurs_abberantes,
        "nb_doublons": nb_doublons,
        "nb_de_colonnes_numerics": nb_de_colonnes_numerics,
        "nb_de_colonnes_texte": nb_de_colonnes_texte
    }

