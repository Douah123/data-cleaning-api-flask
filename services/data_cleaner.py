#ce fichier est chargé du  nettoyage du fichier uploader par le User et sera appelé dans notre 
#pipeline_runner

import pandas as pd
import numpy as np 
from unidecode import unidecode

MISSING_TOKENS = {"", "none", "nan", "null", "na", "n/a", "--", "-"}


def _to_numeric_series(series):
    cleaned = series.astype(str).str.strip()
    cleaned_lower = cleaned.str.lower()
    cleaned = cleaned.mask(cleaned_lower.isin(MISSING_TOKENS), np.nan)
    cleaned = cleaned.str.replace(",", "", regex=False)
    return pd.to_numeric(cleaned, errors="coerce")


def infer_and_convert_numeric_columns(df, min_valid_ratio=0.7):
    object_cols = df.select_dtypes(exclude=np.number).columns
    converted_from_object = []

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
            converted_from_object.append(col)

    df.attrs["converted_from_object"] = converted_from_object
    return df


def _is_integer_like(series, tolerance=1e-9):
    non_null = pd.to_numeric(series.dropna(), errors="coerce").dropna()
    if non_null.empty:
        return False
    return np.isclose(non_null % 1, 0, atol=tolerance).all()


def _detect_numeric_categorical_columns(
    df,
    max_unique=20,
    max_unique_ratio=0.5,
    min_mode_share=0.2
):
    candidates = []
    numeric_cols = df.select_dtypes(include="number").columns
    converted_from_object = set(df.attrs.get("converted_from_object", []))

    for col in numeric_cols:
        col_lower = col.lower()
        if col_lower in {"id"} or col_lower.endswith("_id"):
            continue

        non_null = df[col].dropna()
        if non_null.empty:
            continue

        n = len(non_null)
        unique_count = non_null.nunique()
        unique_ratio = unique_count / n
        mode_share = non_null.value_counts(normalize=True, dropna=True).iloc[0]
        integer_like = _is_integer_like(non_null)
        converted_hint = col in converted_from_object

        small_cardinality = unique_count <= max_unique
        low_uniqueness = unique_ratio <= max_unique_ratio
        repeated_values = mode_share >= min_mode_share
        very_discrete_for_sample = unique_count <= max(5, int(np.sqrt(n)))

        # General rule: a numeric column is treated as categorical if its value distribution
        # is clearly discrete/repetitive (typical encoded categories), even when labels are numeric.
        if (
            very_discrete_for_sample
            or (small_cardinality and low_uniqueness and repeated_values)
            or (converted_hint and small_cardinality and repeated_values)
            or (integer_like and small_cardinality and low_uniqueness)
        ):
            candidates.append(col)

    return candidates


def _clean_categorical_series(series):
    cleaned = series.astype("string").str.strip()
    lowered = cleaned.str.lower()
    cleaned = cleaned.mask(lowered.isin(MISSING_TOKENS), pd.NA)

    non_null = cleaned.dropna()
    if non_null.empty:
        return cleaned.astype(object)

    token_kind = np.select(
        [
            non_null.str.fullmatch(r"[A-Za-z]+", na=False),
            non_null.str.fullmatch(r"[+-]?\d+(?:[.,]\d+)?", na=False),
            non_null.str.fullmatch(r"[A-Za-z0-9]+", na=False),
        ],
        ["alpha", "numeric", "alnum"],
        default="other",
    )

    kind_share = pd.Series(token_kind).value_counts(normalize=True)
    dominant_kind = kind_share.index[0]
    dominant_share = kind_share.iloc[0]

    # General rule: if one token format dominates a categorical column, mismatched formats are anomalies.
    if dominant_share >= 0.8:
        if dominant_kind == "alpha":
            valid_mask = cleaned.str.fullmatch(r"[A-Za-z]+", na=False)
            cleaned = cleaned.mask(cleaned.notna() & ~valid_mask, pd.NA)
        elif dominant_kind == "numeric":
            valid_mask = cleaned.str.fullmatch(r"[+-]?\d+(?:[.,]\d+)?", na=False)
            cleaned = cleaned.mask(cleaned.notna() & ~valid_mask, pd.NA)
        elif dominant_kind == "alnum":
            valid_mask = cleaned.str.fullmatch(r"[A-Za-z0-9]+", na=False)
            cleaned = cleaned.mask(cleaned.notna() & ~valid_mask, pd.NA)

    numeric_like = pd.to_numeric(
        non_null.str.replace(",", "", regex=False),
        errors="coerce"
    )

    # If a categorical column is mostly numeric codes, non-numeric tokens are treated as invalid values.
    if numeric_like.notna().mean() >= 0.8:
        full_numeric_like = pd.to_numeric(
            cleaned.str.replace(",", "", regex=False),
            errors="coerce"
        )
        cleaned = cleaned.mask(cleaned.notna() & full_numeric_like.isna(), pd.NA)

    return cleaned.astype(object)


def _clean_numeric_categorical_series(series, min_integer_share=0.8):
    cleaned = pd.to_numeric(series, errors="coerce")
    non_null = cleaned.dropna()
    if non_null.empty:
        return cleaned

    integer_mask = np.isclose(non_null % 1, 0, atol=1e-9)
    integer_share = float(integer_mask.mean())

    # General rule for numeric-coded categories: if mostly integer codes, decimals are anomalies.
    if integer_share >= min_integer_share:
        invalid_mask = cleaned.notna() & ~np.isclose(cleaned % 1, 0, atol=1e-9)
        cleaned = cleaned.mask(invalid_mask, np.nan)

    return cleaned


def gestion_valeur_manquantes(df, max_unique=20, max_unique_ratio=0.5):

    cols_to_drop = df.columns[df.isna().mean() >= 0.85]
    df = df.drop(columns=cols_to_drop)

    object_cat_cols = set(df.select_dtypes(exclude="number").columns)
    numeric_cat_cols = set(_detect_numeric_categorical_columns(df, max_unique, max_unique_ratio))
    cat_cols = object_cat_cols.union(numeric_cat_cols)
    df.attrs["categorical_columns"] = sorted(cat_cols)

    for col in cat_cols:
        if col not in df.columns:
            continue

        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = _clean_numeric_categorical_series(df[col])
        else:
            df[col] = _clean_categorical_series(df[col])

        mode = df[col].mode(dropna=True)
        if not mode.empty:
            df[col] = df[col].fillna(mode.iloc[0])
        else:
            df[col] = df[col].fillna("Unknown")

    num_cols = [col for col in df.select_dtypes(include="number").columns if col not in cat_cols]

    for col in num_cols:
        median_value = df[col].median()
        if not np.isnan(median_value):
            df[col] = df[col].fillna(median_value)

    return df
def gestion_valeur_abberantes(df):
    
    numeric_cols = df.select_dtypes(include= np.number).columns
    categorical_cols = set(df.attrs.get("categorical_columns", []))
    numeric_cols = [col for col in numeric_cols if col.lower() not in {"id"} and not col.lower().endswith("_id")]
    numeric_cols = [col for col in numeric_cols if col not in categorical_cols]
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
