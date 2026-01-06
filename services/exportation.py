import os
import pandas as pd

OUTPUT_DIR = "outputs"

def export_file(df, file):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Nom original du fichier
    filename = file.filename
    ext = filename.split(".")[-1].lower()

    path = os.path.join(OUTPUT_DIR, filename)

    if ext == "csv":
        df.to_csv(path, index=False)
    elif ext in ["xlsx", "xls"]:
        df.to_excel(path, index=False, engine="openpyxl")
    elif ext == "json":
        df.to_json(path, orient="records")
    elif ext == "xml":
        df.to_xml(path, index=False)
    else:
        raise ValueError("Type de fichier non supporté")

    return path
