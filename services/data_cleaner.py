import pandas as pd
import numpy as np 
from unidecode import unidecode
from sklearn.preprocessing import StandardScaler

def gestion_valeur_manquantes(df):
    report = {}

    for col in df.columns:
        missing_before = int(df[col].isna().sum())
        if df[col].dtype == "object":
            df[col] = df[col].fillna("inconnu")
        else:
            mean_value = df[col].mean()
            if not np.isnan(mean_value):
                df[col].fillna(mean_value, inplace=True)
        
        report[col] = {
            "valeurs_manquantes": missing_before
        }

    return df, report

def gestion_valeur_abberantes(df):
    report = {}
    numeric_cols = df.select_dtypes(include= np.number).columns
    numeric_cols = [col for col in numeric_cols if df[col].nunique() > 2]
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3-Q1

        lower = Q1 - 1.5*IQR
        upper = Q3 + 1.5*IQR

        outliers_detected =((df[col] < lower) | (df[col] > upper)).sum()
        df[col] = np.clip(df[col], lower, upper)

        report[col] = {
            "outliers_detected": int(outliers_detected)
        }

    return df, report 

def supp_doublons(df):
    before = len(df) 
    df = df.drop_duplicates()  
    after = len(df)
    return df, after - before



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

def normaliser_donnees(df, exclude_cols=None):
    if exclude_cols is None:
        exclude_cols = []
    numeric_cols = df.select_dtypes(include=np.number).columns
    numeric_cols = [col for col in numeric_cols if df[col].nunique() > 2
    and col.lower() not in [c.lower() for c in exclude_cols]
    ]
    if len(numeric_cols) == 0:
        return df

    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    return df














def clean_data(df):
    report = {}

    
    df, missing_report = gestion_valeur_manquantes(df)
    report["valeur_manquantes"] = missing_report

   
    df, outliers_report = gestion_valeur_abberantes(df)
    report["outliers_gerer"] = outliers_report
    
    df, duplicates_removed = supp_doublons(df)
    report["doublons_supprimer"] = duplicates_removed

    
    df = normaliser_texte(df)

   
    df = normaliser_donnees(df, exclude_cols=["id", "user_id", "client_id", "index"])

    return df, report
