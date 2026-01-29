#ce fichier est chargé du  nettoyage du fichier uploader par le User et sera appelé dans notre 
#pipeline_runner

import pandas as pd
import numpy as np 
from unidecode import unidecode


def gestion_valeur_manquantes(df):

    # 1️⃣ Supprimer les colonnes avec ≥ 50% de valeurs manquantes
    cols_to_drop = df.columns[df.isna().mean() >= 0.5]
    df = df.drop(columns=cols_to_drop)

    # 2️⃣ Colonnes numériques
    num_cols = df.select_dtypes(include="number").columns

    for col in num_cols:
        median_value = df[col].median()
        if not np.isnan(median_value):
            df[col] = df[col].fillna(median_value)

    # 3️⃣ Colonnes catégorielles (texte)
    cat_cols = df.select_dtypes(exclude="number").columns

    for col in cat_cols:
        mode = df[col].mode()
        if not mode.empty:
            df[col] = df[col].fillna(mode[0])
        else:
            df[col] = df[col].fillna("Unknown")

    return df
def gestion_valeur_abberantes(df):
    
    numeric_cols = df.select_dtypes(include= np.number).columns
    numeric_cols = [col for col in numeric_cols if df[col].nunique() > 2]
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3-Q1

        lower = Q1 - 1.5*IQR
        upper = Q3 + 1.5*IQR

        df[col] = np.clip(df[col], lower, upper)
        

        

    return df

def supp_doublons(df):
    
    df = df.drop_duplicates()  
    
    return df



def normalize_text(text):
    if not isinstance(text, str):
        return text
    text = text.strip().lower()
    text = unidecode(text)
    return text

def normaliser_texte(df):
    text_cols = df.select_dtypes(include="object").columns
    
    for col in text_cols:
        df[col] = df[col].apply(normalize_text)
    return df
















def clean_data(df):

    df = gestion_valeur_manquantes(df)
   
    df = gestion_valeur_abberantes(df)
    
    df = supp_doublons(df)
   
    df = normaliser_texte(df)
    
    return df
