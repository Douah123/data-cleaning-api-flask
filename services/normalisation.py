#ce fichier permet de normaliser le fichier uploader par le user s'il choisit de le faire et
#avec la methode choisie

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler

from services.data_cleaner import (
    _detect_numeric_categorical_columns,
    infer_and_convert_numeric_columns,
)


def _get_categorical_columns(df):
    existing = df.attrs.get("categorical_columns")
    if existing is not None:
        return set(existing).intersection(set(df.columns))

    working_df = infer_and_convert_numeric_columns(df.copy())
    object_cats = set(working_df.select_dtypes(exclude=np.number).columns)
    numeric_cats = set(_detect_numeric_categorical_columns(working_df))
    return object_cats.union(numeric_cats)


def normaliser_donnees(df, method, exclude_cols=None):
    if exclude_cols is None:
        exclude_cols = ["id", "user_id", "client_id", "index"]

    categorical_cols = _get_categorical_columns(df)
    excluded_lower = {c.lower() for c in exclude_cols}

    numeric_cols = df.select_dtypes(include=np.number).columns
    numeric_cols = [
        col
        for col in numeric_cols
        if df[col].nunique() > 2
        and col.lower() not in excluded_lower
        and col not in categorical_cols
    ]

    if method == "zscore":
        scaler = StandardScaler()
    elif method == "minmax":
        scaler = MinMaxScaler()
    elif method == "robust":
        scaler = RobustScaler()
    else:
        raise ValueError("Methode de normalisation inconnue")

    if len(numeric_cols) > 0:
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    cat_cols_for_ohe = [col for col in sorted(categorical_cols) if col in df.columns]
    if len(cat_cols_for_ohe) > 0:
        for col in cat_cols_for_ohe:
            df[col] = df[col].astype("string")
        df = pd.get_dummies(df, columns=cat_cols_for_ohe, dummy_na=False)

    return df
