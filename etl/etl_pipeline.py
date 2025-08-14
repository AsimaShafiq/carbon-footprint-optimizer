
import pandas as pd
import os
from schema_validation import validate_and_transform

def run_etl(input_file: str, output_file: str):
    """Run the ETL process: load -> validate/transform -> save"""
    
    # Step 1: Load data
    print(f"📥 Loading data from {input_file}...")
    df_raw = pd.read_csv(input_file)
    print(f"✅ Loaded {len(df_raw)} rows.")

    # Step 2: Validate & transform
    print("🔍 Validating and transforming data...")
    try:
        df_clean = validate_and_transform(df_raw)
        print(f"✅ Validation successful. {len(df_clean)} rows after cleaning.")
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        return

    # Step 3: Save cleaned data
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df_clean.to_csv(output_file, index=False)
    print(f"💾 Cleaned data saved to {output_file}")

if __name__ == "__main__":
    # Example run
    input_path = "data/raw/SupplyChainGHGEmissionFactors_v1.3.0_NAICS_CO2e_USD2022.csv"
    output_path = "data/processed/cleaned_co2e_data.csv"
    
    run_etl(input_path, output_path)
