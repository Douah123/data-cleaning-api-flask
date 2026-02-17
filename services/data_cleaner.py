#ce fichier est chargé du  nettoyage du fichier uploader par le User et sera appelé dans notre 
#pipeline_runner

import pandas as pd
import numpy as np 
from unidecode import unidecode


def _to_numeric_series(series):
    cleaned = (
        series.astype(str)
        .str.strip()
        .replace({"": np.nan, "none": np.nan, "nan": np.nan, "null": np.nan})
        .str.replace(",", "", regex=False)
    )
    return pd.to_numeric(cleaned, errors="coerce")


def infer_and_convert_numeric_columns(df, min_valid_ratio=0.7):
    object_cols = df.select_dtypes(exclude=np.number).columns
    for col in object_cols:
        if col.lower() in {"id"} or col.lower().endswith("_id"):
            continue
        original = df[col]
        converted = _to_numeric_series(original)
        non_null_count = original.notna().sum()
        if non_null_count == 0:
            continue
        valid_ratio = converted.notna().sum() / non_null_count
        if valid_ratio >= min_valid_ratio:
            df[col] = converted
    return df


def gestion_valeur_manquantes(df):

    cols_to_drop = df.columns[df.isna().mean() >= 0.5]
    df = df.drop(columns=cols_to_drop)

    num_cols = df.select_dtypes(include="number").columns

    for col in num_cols:
        median_value = df[col].median()
        if not np.isnan(median_value):
            df[col] = df[col].fillna(median_value)

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
    numeric_cols = [col for col in numeric_cols if col.lower() not in {"id"} and not col.lower().endswith("_id")]
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

    df = infer_and_convert_numeric_columns(df)

    df = gestion_valeur_manquantes(df)
   
    df = gestion_valeur_abberantes(df)
    
    df = normaliser_texte(df)

    df = supp_doublons(df)
    
    return df
