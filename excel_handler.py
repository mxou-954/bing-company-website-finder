import sys

import pandas as pd


def load_excel(path: str) -> pd.DataFrame:
    try:
        df = pd.read_excel(path, sheet_name=0, dtype=str)
    except Exception as e:
        print(f"Impossible de lire '{path}' : {e}")
        sys.exit(1)

    if "Raison Sociale" not in df.columns:
        print("Erreur : la colonne 'Raison Sociale' est introuvable dans l'Excel.")
        sys.exit(1)

    if "Site officiel" not in df.columns:
        df["Site officiel"] = ""

    return df


def save_excel(df: pd.DataFrame, path: str) -> None:
    try:
        df.to_excel(path, index=False, engine="openpyxl")
    except Exception as e:
        print(f"Impossible d'ecrire '{path}' : {e}")
        sys.exit(1)