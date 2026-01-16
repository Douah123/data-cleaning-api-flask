#ce fichier est chargé du  nettoyage du fichier uploader par le User et sera appelé dans notre 
#pipeline_runner

import pandas as pd
import numpy as np 
from unidecode import unidecode


def gestion_valeur_manquantes(df):

    for col in df.columns:
        
        if df[col].dtype == "object":
            df[col] = df[col].fillna("inconnu")
        elif df[col].isna().mean()*100 >= 50:
            df.drop(columns=[col], inplace=True)
        else:
            median_value = df[col].median()
            if not np.isnan(median_value):
                df[col].fillna(median_value, inplace=True)

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
