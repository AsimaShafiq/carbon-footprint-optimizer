import pandas as pd
import os
import pulp

# Paths
INPUT_FILE = "data/processed/emissions_forecast.csv"
OUTPUT_FILE = "data/processed/optimization_results.csv"

# Example actions dictionary
# Each action has a cost ($) and emission reduction % (relative to baseline)
ACTIONS = {
    "Renewable_Energy": {"cost": 50000, "reduction_pct": 0.20},  # 20% reduction
    "EV_Fleet": {"cost": 30000, "reduction_pct": 0.15},          # 15% reduction
    "Waste_Recycling": {"cost": 15000, "reduction_pct": 0.10},   # 10% reduction
    "Carbon_Offsets": {"cost": 10000, "reduction_pct": 0.05}     # 5% reduction
}

def run_optimization(target_reduction=0.25):
    """
    Runs optimization to find the best mix of actions to achieve
    at least `target_reduction` (fraction of baseline emissions)
    while minimizing cost.
    """

    # Step 1: Load forecast data
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"{INPUT_FILE} not found. Run forecasting first.")

    forecast_df = pd.read_csv(INPUT_FILE)
    baseline_emissions = forecast_df["yhat"].iloc[-1]  # Last forecast year as baseline
    print(f"📥 Baseline future emissions: {baseline_emissions:.2f} kg CO2e")

    # Step 2: Define optimization problem
    prob = pulp.LpProblem("Carbon_Footprint_Optimization", pulp.LpMinimize)

    # Step 3: Decision variables (0 or 1 -> action chosen or not)
    action_vars = {action: pulp.LpVariable(action, cat="Binary") for action in ACTIONS.keys()}

    # Step 4: Objective = minimize total cost
    prob += pulp.lpSum([ACTIONS[a]["cost"] * action_vars[a] for a in ACTIONS]), "Total Cost"

    # Step 5: Constraint = must meet target reduction
    total_reduction = pulp.lpSum([ACTIONS[a]["reduction_pct"] * action_vars[a] for a in ACTIONS])
    prob += total_reduction >= target_reduction, "Reduction Target"

    # Step 6: Solve
    prob.solve()

    # Step 7: Collect results
    chosen_actions = [a for a in ACTIONS if action_vars[a].value() == 1]
    total_cost = sum(ACTIONS[a]["cost"] for a in chosen_actions)
    achieved_reduction = sum(ACTIONS[a]["reduction_pct"] for a in chosen_actions)
    new_emissions = baseline_emissions * (1 - achieved_reduction)

    results = {
        "Chosen Actions": chosen_actions,
        "Total Cost": total_cost,
        "Achieved Reduction %": achieved_reduction,
        "New Emissions (kg CO2e)": new_emissions
    }

    # Save results as CSV
    results_df = pd.DataFrame([results])
    results_df.to_csv(OUTPUT_FILE, index=False)

    print(f"✅ Optimization complete. Results saved to {OUTPUT_FILE}")
    print(results)

if __name__ == "__main__":
    run_optimization(target_reduction=0.25)  # Example: aim for 25% reduction
