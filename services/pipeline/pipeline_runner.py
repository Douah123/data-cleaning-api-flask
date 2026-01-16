from services.data_cleaner import clean_data
from services.normalisation import normaliser_donnees
from services.pipeline.statistics import calcul_statt
import pandas as pd
def run_pipeline(df, options):
    if df is None:
        raise ValueError("le dataframe est vide")
    
    stats_avant = calcul_statt(df)
    
    cleaned_df = clean_data(df)

    stats_apres = calcul_statt(cleaned_df)

    if options.get("normalize") is True:
        method = options.get("method")
        cleaned_df = normaliser_donnees(cleaned_df, method=method)
    else:
        cleaned_df = clean_data(df)
    
    

    return cleaned_df, stats_avant, stats_apres

