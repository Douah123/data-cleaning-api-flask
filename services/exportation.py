import os
import uuid

OUTPUT_DIR = "outputs"

def export_file(df, original_filename):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    
    file_id = str(uuid.uuid4())
    
    ext = original_filename.split(".")[-1].lower()
     
    base_name = original_filename.rsplit(".", 1)[0] 
    output_filename = f"{base_name}_{file_id}.{ext}"

    path = os.path.join(OUTPUT_DIR, output_filename)

    if ext == "csv":
        df.to_csv(path, index=False)
    elif ext in ["xlsx", "xls","json", "xml"]:
        ext = ["xlsx"]
        df.to_excel(path, index=False, engine="openpyxl")
    else:
        raise ValueError("Type de fichier non supporté")

    return {
        "file_id":file_id,
         "output_filename":output_filename,
         "path":path
    }
