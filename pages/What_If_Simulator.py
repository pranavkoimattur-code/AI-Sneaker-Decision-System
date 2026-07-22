import streamlit as st
import pandas as pd
import plotly.express as px

from utils.calculations import calculate_kpis

st.title("What-If Simulator")
st.subheader("Test how pricing, cost, and sales changes affect profitability")

st.sidebar.header("Scenario Inputs")

base_total_production_cost = 538819
base_production_units = 1000
base_fixed_costs = 441087
base_variable_cost_per_unit = 97.732

selling_price = st.sidebar.slider("Selling Price per Unit ($)", 850, 750,800)
monthly_units_sold = st.sidebar.slider("Monthly Units Sold", 10, 1000, 100)

material_cost_change = st.sidebar.slider("Material Cost Change (%)", -30, 50, 0)
labor_cost_change = st.sidebar.slider("Labor Cost Change (%)", -30, 50, 0)
shipping_cost_change = st.sidebar.slider("Shipping Cost Change (%)", -30, 50, 0)
marketing_cost_change = st.sidebar.slider("Marketing Cost Change (%)", -30, 50, 0)

st.divider()

# Approximate cost buckets for simulation
cost_buckets = {
    "Materials": 120000,
    "Labor": 361428,
    "Shipping": 45000,
    "Marketing": 12391,
}

adjusted_cost_buckets = {
    "Materials": cost_buckets["Materials"] * (1 + material_cost_change / 100),
    "Labor": cost_buckets["Labor"] * (1 + labor_cost_change / 100),
    "Shipping": cost_buckets["Shipping"] * (1 + shipping_cost_change / 100),
    "Marketing": cost_buckets["Marketing"] * (1 + marketing_cost_change / 100),
}

other_costs = base_total_production_cost - sum(cost_buckets.values())
adjusted_total_production_cost = sum(adjusted_cost_buckets.values()) + other_costs
adjusted_cost_per_unit = adjusted_total_production_cost / base_production_units

adjusted_variable_cost_per_unit = base_variable_cost_per_unit * (
    1
    + material_cost_change / 100 * 0.40
    + labor_cost_change / 100 * 0.35
    + shipping_cost_change / 100 * 0.15
    + marketing_cost_change / 100 * 0.10
)

kpis = calculate_kpis(
    total_production_cost=adjusted_total_production_cost,
    production_units=base_production_units,
    selling_price=selling_price,
    monthly_units_sold=monthly_units_sold,
    fixed_costs=base_fixed_costs,
    variable_cost_per_unit=adjusted_variable_cost_per_unit,
)

col1, col2, col3 = st.columns(3)
col1.metric("Adjusted Production Cost", f"${kpis['total_production_cost']:,.0f}")
col2.metric("Adjusted Cost per Unit", f"${kpis['cost_per_unit']:,.2f}")
col3.metric("Selling Price", f"${kpis['selling_price']:,.2f}")

col4, col5, col6 = st.columns(3)
col4.metric("Gross Profit / Unit", f"${kpis['gross_profit_per_unit']:,.2f}")
col5.metric("Gross Margin %", f"{kpis['gross_margin_pct']:.1f}%")
col6.metric("Break-even Quantity", f"{kpis['break_even_quantity']:,.0f} units")

col7, col8 = st.columns(2)
col7.metric("Monthly Revenue", f"${kpis['monthly_revenue']:,.0f}")
col8.metric("Monthly Profit", f"${kpis['monthly_profit']:,.0f}")

st.divider()

st.header("Scenario Cost Breakdown")

scenario_df = pd.DataFrame({
    "Category": list(adjusted_cost_buckets.keys()) + ["Other Costs"],
    "Cost": list(adjusted_cost_buckets.values()) + [other_costs],
})

fig = px.bar(
    scenario_df,
    x="Category",
    y="Cost",
    title="Adjusted Cost by Category",
    text_auto=".2s",
)

st.plotly_chart(fig, use_container_width=True)

st.header("AI-Style Scenario Interpretation")

if kpis["gross_margin_pct"] < 25:
    st.warning(
        "This scenario creates a weak margin. The business should consider increasing price, "
        "reducing labor/material costs, or lowering production volume."
    )
elif kpis["gross_margin_pct"] < 40:
    st.info(
        "This scenario is financially workable, but there is room for optimization. "
        "The largest changed cost category should be reviewed first."
    )
else:
    st.success(
        "This scenario shows strong profitability. The current price and cost structure appear healthy."
    )

highest_cost_category = scenario_df.sort_values("Cost", ascending=False).iloc[0]

st.write(
    f"The highest cost category in this scenario is **{highest_cost_category['Category']}** "
    f"at **${highest_cost_category['Cost']:,.0f}**."
)
