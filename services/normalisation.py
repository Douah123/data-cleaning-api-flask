import pandas as pd
import numpy as np 
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler

def normaliser_donnees(df, method, exclude_cols=None):
    if exclude_cols is None:
        exclude_cols = ["id", "user_id", "client_id", "index"]
    numeric_cols = df.select_dtypes(include=np.number).columns
    numeric_cols = [col for col in numeric_cols if df[col].nunique() > 2
    and col.lower() not in [c.lower() for c in exclude_cols]
    ]
    if len(numeric_cols) == 0:
        return df
    if method == "zscore":
        scaler = StandardScaler()
    elif method == "minmax":
        scaler = MinMaxScaler()
    elif method == "robust":
        scaler = RobustScaler()
    else:
        raise ValueError("Méthode de normalisation inconnue")
    
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    return df
    