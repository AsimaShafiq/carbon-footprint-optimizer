
import pandas as pd

SCHEMA = {
    "naics_code": str,
    "industry": str,
    "emission_factor": float,
    "unit": str,
    "year": int,
    "reference_code": str
}

def validate_and_transform(df: pd.DataFrame) -> pd.DataFrame:
    column_mapping = {
        "2017 NAICS Code": "naics_code",
        "2017 NAICS Title": "industry",
        "Supply Chain Emission Factors with Margins": "emission_factor",
        "Unit": "unit",
        "Reference USEEIO Code": "reference_code"
    }
    df = df.rename(columns=column_mapping)

    if "year" not in df.columns:
        df["year"] = 2022

    for col in SCHEMA.keys():
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    for col, dtype in SCHEMA.items():
        try:
            df[col] = df[col].astype(dtype)
        except Exception as e:
            raise ValueError(f"Column {col} cannot be converted to {dtype}: {e}")

    df = df.drop_duplicates()
    df = df[df["emission_factor"] >= 0]

    return df
