import pandas as pd
from io import BytesIO

def load_file(file):
    filename = file.filename.lower()
    
    
    file_bytes = file.read()
    
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
