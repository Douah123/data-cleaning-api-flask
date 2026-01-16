import pandas as pd
from io import BytesIO

def load_file(file):

    if not file or not hasattr(file, "filename"):
        raise ValueError("Fichier invalide")
    filename = file.filename.lower()
    
    if filename == "":
        raise ValueError("Nom de fichier manquant")

    
    file_bytes = file.read()
    file.seek(0)
    
    try:
        if filename.endswith(".csv"):
        
            return pd.read_csv(BytesIO(file_bytes)), "csv"
        
        elif filename.endswith(".xlsx") or filename.endswith(".xls"):
            
            return pd.read_excel(BytesIO(file_bytes), engine='openpyxl'), "excel"
        
        elif filename.endswith(".json"):
            return pd.read_json(BytesIO(file_bytes)), "json"
        
        elif filename.endswith(".xml"):
            return pd.read_xml(BytesIO(file_bytes)), "xml"
        
        else:
            raise ValueError("Format non supporté")
    except Exception as e:
        raise ValueError(f"Erreur lors du chargement du fichier : {str(e)}")
