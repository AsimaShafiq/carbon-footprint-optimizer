# import pandas as pd
# import os


# # Define the fixed internal schema
# SCHEMA = {
#     "naics_code": str,
#     "industry": str,
#     "emission_factor": float,
#     "unit": str,
#     "year": int,
#     "reference_code": str
# }

# # Validation function
# def validate_and_transform(df: pd.DataFrame) -> pd.DataFrame:
#     """
#     Validates and transforms incoming dataset into the fixed schema.
#     Returns cleaned DataFrame or raises ValueError if schema is broken.
#     """
#     # Step 1: Rename columns to match schema
#     column_mapping = {
#         "2017 NAICS Code": "naics_code",
#         "2017 NAICS Title": "industry",
#         "Supply Chain Emission Factors with Margins": "emission_factor",
#         "Unit": "unit",
#         "Reference USEEIO Code": "reference_code"
#     }
#     df = df.rename(columns=column_mapping)
    
#     # Step 2: Add missing columns (with default values if not present)
#     if "year" not in df.columns:
#         df["year"] = 2022  # default year for now
    
#     # Step 3: Ensure all required columns exist
#     for col in SCHEMA.keys():
#         if col not in df.columns:
#             raise ValueError(f"Missing required column: {col}")
    
#     # Step 4: Convert data types
#     for col, dtype in SCHEMA.items():
#         try:
#             df[col] = df[col].astype(dtype)
#         except Exception as e:
#             raise ValueError(f"Column {col} cannot be converted to {dtype}: {e}")
    
#     # Step 5: Drop duplicates
#     df = df.drop_duplicates()
    
#     # Step 6: Filter unrealistic values
#     df = df[df["emission_factor"] >= 0]  # No negative emissions
    
#     return df

# # Load example dataset (CO2e file)
# input_file = "SupplyChainGHGEmissionFactors_v1.3.0_NAICS_CO2e_USD2022.csv"
# input_path = f"data/{input_file}" if os.path.exists(f"data/{input_file}") else input_file

# try:
#     df_raw = pd.read_csv(input_path)
#     df_clean = validate_and_transform(df_raw)

#     # Save cleaned data
#     output_path = "data/processed/cleaned_co2e_data.csv"
#     df_clean.to_csv(output_path, index=False)

#     script_status = f"✅ Validation successful. Cleaned file saved to {output_path}"
# except Exception as e:
#     error_log = f"❌ Validation failed: {e}"
#     with open("etl/validation_errors.log", "w") as f:
#         f.write(str(e))
#     script_status = error_log

# # Save script to etl/schema_validation.py
# script_content = """
# import pandas as pd

# SCHEMA = {
#     "naics_code": str,
#     "industry": str,
#     "emission_factor": float,
#     "unit": str,
#     "year": int,
#     "reference_code": str
# }

# def validate_and_transform(df: pd.DataFrame) -> pd.DataFrame:
#     column_mapping = {
#         "2017 NAICS Code": "naics_code",
#         "2017 NAICS Title": "industry",
#         "Supply Chain Emission Factors with Margins": "emission_factor",
#         "Unit": "unit",
#         "Reference USEEIO Code": "reference_code"
#     }
#     df = df.rename(columns=column_mapping)

#     if "year" not in df.columns:
#         df["year"] = 2022

#     for col in SCHEMA.keys():
#         if col not in df.columns:
#             raise ValueError(f"Missing required column: {col}")

#     for col, dtype in SCHEMA.items():
#         try:
#             df[col] = df[col].astype(dtype)
#         except Exception as e:
#             raise ValueError(f"Column {col} cannot be converted to {dtype}: {e}")

#     df = df.drop_duplicates()
#     df = df[df["emission_factor"] >= 0]

#     return df
# """

# with open("etl/schema_validation.py", "w") as f:
#     f.write(script_content)

# script_status


# Create updated calculation_engine.py content that reads scope mapping from CSV

calculation_engine_content = """
import pandas as pd
import os
import json

# Paths
INPUT_FILE = "data/processed/cleaned_co2e_data.csv"
SCOPE_MAPPING_FILE = "calculations/scope_mapping.csv"
OUTPUT_SUMMARY_CSV = "data/processed/emissions_summary.csv"
OUTPUT_SUMMARY_JSON = "data/processed/emissions_summary.json"

def load_scope_mapping():
    \"\"\"Loads scope mapping from CSV into a dictionary.\"\"\"
    if not os.path.exists(SCOPE_MAPPING_FILE):
        raise FileNotFoundError(f"{SCOPE_MAPPING_FILE} not found.")
    mapping_df = pd.read_csv(SCOPE_MAPPING_FILE, dtype={"naics_code": str, "scope": str})
    return dict(zip(mapping_df["naics_code"], mapping_df["scope"]))

def assign_scope(naics_code, mapping_dict):
    \"\"\"Assigns scope category based on NAICS code using mapping dict.\"\"\"
    return mapping_dict.get(str(naics_code), "Scope 3")  # Default to Scope 3

def run_calculations():
    # Step 1: Load cleaned dataset
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"{INPUT_FILE} not found. Run ETL first.")
    df = pd.read_csv(INPUT_FILE)
    print(f"📥 Loaded {len(df)} rows from cleaned dataset.")

    # Step 2: Load mapping and assign scopes
    mapping_dict = load_scope_mapping()
    df["scope"] = df["naics_code"].apply(lambda code: assign_scope(code, mapping_dict))

    # Step 3: Calculate totals
    total_emissions = df["emission_factor"].sum()
    emissions_by_scope = df.groupby("scope")["emission_factor"].sum().to_dict()
    emissions_by_industry = df.groupby("industry")["emission_factor"].sum().sort_values(ascending=False).to_dict()

    # Step 4: Save summary results
    summary_df = pd.DataFrame({
        "Metric": ["Total Emissions (kg CO2e)"] + [f"{scope} Emissions" for scope in emissions_by_scope.keys()],
        "Value": [total_emissions] + list(emissions_by_scope.values())
    })
    summary_df.to_csv(OUTPUT_SUMMARY_CSV, index=False)

    summary_json = {
        "total_emissions": total_emissions,
        "emissions_by_scope": emissions_by_scope,
        "emissions_by_industry": emissions_by_industry
    }
    with open(OUTPUT_SUMMARY_JSON, "w") as f:
        json.dump(summary_json, f, indent=4)

    print(f"✅ Summary saved to {OUTPUT_SUMMARY_CSV} and {OUTPUT_SUMMARY_JSON}")

if __name__ == "__main__":
    run_calculations()
"""

# Save the updated calculation_engine.py
with open("calculations/calculation_engine.py", "w") as f:
    f.write(calculation_engine_content)

"✅ calculation_engine.py updated to use scope_mapping.csv"
