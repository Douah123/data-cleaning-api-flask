def valider_options(options):
    if options is None:
        return {
            "normalize": False,
            "method": None
        }
    if not isinstance(options, dict):
        raise ValueError("Les options doivent être un objet JSON")
    
    normalize = options.get("normalize", False)

    if not isinstance(normalize, bool):
        raise ValueError("l'option normalize doit etre un booleen")
    if normalize is False:
        return {
            "normalize": False,
            "method": None
        }
    method = options.get("method")

    if not isinstance(method, str) and method is not None:
        raise ValueError("l'option method doit etre un string")
    
    method_clean = method.lower().replace("-", "").replace("_", "").replace(" ", "")

    allowed_methods = ["minmax","zscore","robust"]
    

    if method_clean not in allowed_methods and method is not None:
        raise ValueError(
            f"Méthode invalide. Méthodes autorisées : {allowed_methods}"
        )
    return{
        "normalize": normalize,
        "method": method_clean
    }        
