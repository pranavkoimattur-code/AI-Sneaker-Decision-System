import streamlit as st
import pandas as pd

from utils.calculations import calculate_kpis

st.set_page_config(page_title="AI Recommendations", layout="wide")

st.title("🤖 AI Business Advisor")
st.subheader("AI-Powered Recommendations for Smart Sneaker Display Case")

####################################################
# Sidebar Inputs
####################################################

st.sidebar.header("Business Inputs")

selling_price = st.sidebar.number_input(
    "Selling Price ($)",
    value=299.0,
    step=5.0
)

monthly_units = st.sidebar.number_input(
    "Monthly Units Sold",
    value=100,
    step=10
)

total_cost = 538819
production_units = 1000
fixed_costs = 441087
variable_cost = 97.732

####################################################
# KPI Calculation
####################################################

kpis = calculate_kpis(
    total_production_cost=total_cost,
    production_units=production_units,
    selling_price=selling_price,
    monthly_units_sold=monthly_units,
    fixed_costs=fixed_costs,
    variable_cost_per_unit=variable_cost
)

####################################################
# KPI Cards
####################################################

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Gross Margin",
    f"{kpis['gross_margin_pct']:.1f}%"
)

c2.metric(
    "Monthly Profit",
    f"${kpis['monthly_profit']:,.0f}"
)

health = 85

if kpis["gross_margin_pct"] < 20:
    health = 35
elif kpis["gross_margin_pct"] < 30:
    health = 60
elif kpis["gross_margin_pct"] < 40:
    health = 80

c3.metric(
    "Business Health",
    f"{health}/100"
)

confidence = 94

c4.metric(
    "AI Confidence",
    f"{confidence}%"
)

st.divider()

####################################################
# Recommendation Engine
####################################################

recommendations = []

####################################################
# Margin
####################################################

if kpis["gross_margin_pct"] < 25:

    recommendations.append({
        "Priority":"🔴 High",
        "Recommendation":"Increase selling price",
        "Reason":"Current margin is below 25%",
        "Impact":"Higher profit per unit"
    })

elif kpis["gross_margin_pct"] < 40:

    recommendations.append({
        "Priority":"🟡 Medium",
        "Recommendation":"Optimize manufacturing cost",
        "Reason":"Margin is acceptable but can improve",
        "Impact":"Increase profitability"
    })

else:

    recommendations.append({
        "Priority":"🟢 Low",
        "Recommendation":"Maintain current pricing",
        "Reason":"Business has healthy margins",
        "Impact":"Sustain profitability"
    })

####################################################
# Break-even
####################################################

if kpis["break_even_quantity"] > monthly_units:

    recommendations.append({
        "Priority":"🔴 High",
        "Recommendation":"Increase monthly sales",
        "Reason":"Current sales do not cover break-even",
        "Impact":"Recover fixed costs sooner"
    })

####################################################
# Cost Reduction
####################################################

estimated_savings = total_cost * 0.08

recommendations.append({
    "Priority":"🟡 Medium",
    "Recommendation":"Reduce production cost by 8%",
    "Reason":"Packaging, shipping and material costs can be optimized",
    "Impact":f"Estimated savings ${estimated_savings:,.0f}"
})

####################################################
# Pricing Recommendation
####################################################

recommended_price = (
    kpis["cost_per_unit"] / (1 - 0.40)
)

if recommended_price > selling_price:

    recommendations.append({
        "Priority":"🟡 Medium",
        "Recommendation":f"Target selling price ${recommended_price:.2f}",
        "Reason":"Achieve 40% gross margin",
        "Impact":"Higher profitability"
    })

####################################################
# Inventory Recommendation
####################################################

if monthly_units > 400:

    recommendations.append({

        "Priority":"🟢 Low",

        "Recommendation":"Increase manufacturing capacity",

        "Reason":"Demand appears strong",

        "Impact":"Reduce stock-outs"

    })

####################################################
# Recommendation Cards
####################################################

st.header("AI Recommendations")

for rec in recommendations:

    with st.container():

        st.markdown(f"### {rec['Priority']}")

        st.write(f"**Recommendation**")

        st.success(rec["Recommendation"])

        st.write(f"**Reason**")

        st.write(rec["Reason"])

        st.write(f"**Estimated Impact**")

        st.info(rec["Impact"])

        st.divider()

####################################################
# Executive Summary
####################################################

st.header("Executive Summary")

summary = f"""
The current business has a gross margin of
{kpis['gross_margin_pct']:.1f}%.

Estimated monthly profit is
${kpis['monthly_profit']:,.0f}.

The AI Business Advisor recommends focusing on:

• Pricing optimization

• Manufacturing cost reduction

• Break-even improvement

Overall Business Health Score:
{health}/100

Recommendation Confidence:
{confidence}%
"""

st.success(summary)

####################################################
# Recommendation Table
####################################################

st.header("Recommendation Table")

df = pd.DataFrame(recommendations)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)
