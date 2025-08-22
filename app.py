import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(page_title="AI-Powered Carbon Footprint Optimizer", layout="wide")
st.title("🌍 AI-Powered Carbon Footprint Optimizer")

# -----------------------------
# Section 1: Current Emissions Summary
# -----------------------------
st.header("📊 Current Emissions Summary")

try:
    summary_df = pd.read_csv("data/processed/emissions_summary.csv")
    st.dataframe(summary_df, use_container_width=True)
except FileNotFoundError:
    st.warning("⚠️ emissions_summary.csv not found. Please run calculation_engine.py first.")

# -----------------------------
# Section 2: Forecasted Emissions
# -----------------------------
st.header("📈 Forecasted Emissions")

col1, col2 = st.columns([2, 1])

with col1:
    try:
        forecast_df = pd.read_csv("data/processed/emissions_forecast.csv")
        st.line_chart(forecast_df.set_index("ds")["yhat"])
    except FileNotFoundError:
        st.warning("⚠️ emissions_forecast.csv not found. Please run forecasting.py first.")

with col2:
    try:
        st.image("data/processed/emissions_forecast.png", caption="Forecast Chart")
    except FileNotFoundError:
        st.info("No forecast chart found.")

# -----------------------------
# Section 3: Optimization Results
# -----------------------------
st.header("🛠️ Optimization Recommendations")

try:
    opt_df = pd.read_csv("data/processed/optimization_results.csv")
    st.dataframe(opt_df, use_container_width=True)

    chosen_actions = opt_df["Chosen Actions"].iloc[0]
    st.success(f"✅ Recommended Actions: {chosen_actions}")

    new_emissions = opt_df["New Emissions (kg CO2e)"].iloc[0]
    reduction_pct = opt_df["Achieved Reduction %"].iloc[0] * 100
    st.metric("New Projected Emissions", f"{new_emissions:,.2f} kg CO2e")
    st.metric("Reduction Achieved", f"{reduction_pct:.1f}%")
except FileNotFoundError:
    st.warning("⚠️ optimization_results.csv not found. Please run optimization.py first.")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit, Prophet & PuLP")
