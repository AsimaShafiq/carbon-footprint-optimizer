import pandas as pd
import os
import json

# Paths
INPUT_FILE = "data/processed/cleaned_co2e_data.csv"
OUTPUT_SUMMARY_CSV = "data/processed/emissions_summary.csv"
OUTPUT_SUMMARY_JSON = "data/processed/emissions_summary.json"

# Placeholder mapping for NAICS codes to Scope categories
# Later this can be loaded from a CSV or DB
SCOPE_MAPPING = {
    # Example mappings
    "111110": "Scope 3",  # Soybean Farming
    "221100": "Scope 2",  # Electric Power Generation
    # Default mapping
}

def assign_scope(naics_code):
    """Assigns scope category based on NAICS code."""
    return SCOPE_MAPPING.get(str(naics_code), "Scope 3")

def run_calculations():
    # Step 1: Load cleaned dataset
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"{INPUT_FILE} not found. Run ETL first.")
    
    df = pd.read_csv(INPUT_FILE)
    print(f"📥 Loaded {len(df)} rows from cleaned dataset.")

    # Step 2: Assign scopes
    df["scope"] = df["naics_code"].apply(assign_scope)

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



