#ce fichier permet d'exporter le fichier uploader et nettoyer au User et sera appplé dans notre route 
#clean_route

import os
import uuid

OUTPUT_DIR = "outputs"

def export_file(df, original_filename):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    
    file_id = str(uuid.uuid4())
    
    input_ext = original_filename.split(".")[-1].lower()
    base_name = original_filename.rsplit(".", 1)[0] 

    if input_ext == "csv":
        output_ext = "csv"
    elif input_ext in ["xlsx", "xls","json", "xml"]:
        output_ext = "xlsx"
    else:
        raise ValueError("Type de fichier non supporté")
    output_filename = f"{base_name}_{file_id}.{output_ext}"

    path = os.path.join(OUTPUT_DIR, output_filename)

    if input_ext == "csv":
        df.to_csv(path, index=False)
    
    else:
        df.to_excel(path, index=False, engine="openpyxl")

    return {
        "file_id":file_id,
         "output_filename":output_filename,
         "path":path
    }
