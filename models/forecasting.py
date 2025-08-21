
# For Sample Data:

# import pandas as pd
# import os
# from prophet import Prophet
# import matplotlib.pyplot as plt

# # Paths
# INPUT_FILE = "data/processed/cleaned_co2e_data.csv"
# OUTPUT_FORECAST_CSV = "data/processed/emissions_forecast.csv"
# OUTPUT_FORECAST_PNG = "data/processed/emissions_forecast.png"

# def simulate_historical_data(df):
#     """
#     Since dataset is not time-series, simulate yearly emissions totals.
#     Later, replace with real historical data.
#     """
#     # Calculate total emissions as baseline
#     baseline_total = df["emission_factor"].sum()

#     # Simulate emissions for 2018–2022 with random multipliers
#     years = [2018, 2019, 2020, 2021, 2022]
#     multipliers = [0.9, 0.95, 1.0, 1.05, 1.1]  # Example trend

#     data = {"ds": [], "y": []}
#     for year, factor in zip(years, multipliers):
#         data["ds"].append(f"{year}-01-01")
#         data["y"].append(baseline_total * factor)

#     return pd.DataFrame(data)

# def run_forecasting():
#     # Step 1: Load cleaned dataset
#     if not os.path.exists(INPUT_FILE):
#         raise FileNotFoundError(f"{INPUT_FILE} not found. Run ETL first.")
    
#     df = pd.read_csv(INPUT_FILE)

#     # Step 2: Simulate historical totals
#     ts_df = simulate_historical_data(df)

#     # Step 3: Train Prophet model
#     model = Prophet(yearly_seasonality=True, daily_seasonality=False)
#     model.fit(ts_df)

#     # Step 4: Forecast next 5 years
#     future = model.make_future_dataframe(periods=5, freq="Y")
#     forecast = model.predict(future)

#     # Step 5: Save forecast results
#     forecast_df = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
#     forecast_df.to_csv(OUTPUT_FORECAST_CSV, index=False)

#     # Step 6: Plot and save forecast chart
#     fig = model.plot(forecast)
#     plt.title("Forecasted Carbon Emissions")
#     plt.xlabel("Year")
#     plt.ylabel("kg CO2e")
#     plt.savefig(OUTPUT_FORECAST_PNG)

#     print(f"✅ Forecast saved to {OUTPUT_FORECAST_CSV} and {OUTPUT_FORECAST_PNG}")

# if __name__ == "__main__":
#     run_forecasting()


# For Actual Data

import pandas as pd
import os
from prophet import Prophet
import matplotlib.pyplot as plt

# Paths
INPUT_FILE = "data/processed/cleaned_co2e_data.csv"
OUTPUT_FORECAST_CSV = "data/processed/emissions_forecast.csv"
OUTPUT_FORECAST_PNG = "data/processed/emissions_forecast.png"

def run_forecasting():
    # Step 1: Load cleaned dataset
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"{INPUT_FILE} not found. Run ETL first.")
    
    df = pd.read_csv(INPUT_FILE)

    # Step 2: Calculate baseline emissions
    baseline_total = df["emission_factor"].sum()

    # Create minimal time-series for Prophet (3 baseline years)
    ts_df = pd.DataFrame({
        "ds": ["2020-01-01", "2021-01-01", "2022-01-01"],
        "y": [baseline_total * 0.95, baseline_total, baseline_total * 1.05]  # small variation
    })

    # Step 3: Train Prophet model
    model = Prophet(yearly_seasonality=True, daily_seasonality=False)
    model.fit(ts_df)

    # Step 4: Forecast next 5 years
    future = model.make_future_dataframe(periods=5, freq="Y")
    forecast = model.predict(future)

    # Step 5: Save forecast results
    forecast_df = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
    forecast_df.to_csv(OUTPUT_FORECAST_CSV, index=False)

    # Step 6: Plot and save forecast chart
    fig = model.plot(forecast)
    plt.title("Forecasted Carbon Emissions")
    plt.xlabel("Year")
    plt.ylabel("kg CO2e")
    plt.savefig(OUTPUT_FORECAST_PNG)

    print(f"✅ Forecast saved to {OUTPUT_FORECAST_CSV} and {OUTPUT_FORECAST_PNG}")

if __name__ == "__main__":
    run_forecasting()
