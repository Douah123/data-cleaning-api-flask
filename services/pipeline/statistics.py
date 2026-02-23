#ce fichier nous permet d'effectuer des calculs de toutes les stats que contient le fichier uploader
#et sera appele par pipeline_runner.py(notre fichier orchestre)

import numpy as np
from services.data_cleaner import infer_and_convert_numeric_columns, _detect_numeric_categorical_columns


def _get_categorical_columns(df):
    existing = df.attrs.get("categorical_columns")
    if existing is not None:
        return set(existing).intersection(set(df.columns))

    working_df = infer_and_convert_numeric_columns(df.copy())
    object_cats = set(working_df.select_dtypes(exclude=np.number).columns)
    numeric_cats = set(_detect_numeric_categorical_columns(working_df))
    return object_cats.union(numeric_cats)


def valeurs_abber(df, categorical_cols=None):
    if categorical_cols is None:
        categorical_cols = set()

    numeric_cols = df.select_dtypes(include=np.number).columns
    numeric_cols = [col for col in numeric_cols if col not in categorical_cols]
    numeric_cols = [col for col in numeric_cols if df[col].nunique() > 2]

    valeur_abberante = 0
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        valeur_abberante += ((df[col] < lower) | (df[col] > upper)).sum()
    return int(valeur_abberante)


def calcul_statt(df):
    nb_de_lignes = int(df.shape[0])
    nb_de_colonnes = int(df.shape[1])
    nb_valeur_manquantes = int(df.isna().sum().sum())
    nb_doublons = int(df.duplicated().sum())

    categorical_cols = _get_categorical_columns(df)
    numeric_cols = set(df.select_dtypes(include=np.number).columns) - categorical_cols
    text_cols = set(df.select_dtypes(include=["object", "string"]).columns) - categorical_cols

    nb_valeurs_abberantes = valeurs_abber(df, categorical_cols=categorical_cols)
    nb_de_colonnes_numerics = int(len(numeric_cols))
    nb_de_colonnes_texte = int(len(text_cols))
    nb_de_colonnes_categorielles = int(len(categorical_cols))

    return {
        "Lignes": nb_de_lignes,
        "Colonnes": nb_de_colonnes,
        "Valeurs Manquantes": nb_valeur_manquantes,
        "Valeurs Abberantes": nb_valeurs_abberantes,
        "Doublons": nb_doublons,
        "Colonnes Numeriques": nb_de_colonnes_numerics,
        "Colonnes textuelles": nb_de_colonnes_texte,
        "Colonnes Categorielles": nb_de_colonnes_categorielles,
    }
