import streamlit as st
from utils.calculations import calculate_kpis
from utils.charts import cost_breakdown_chart
from utils.data_loader import load_business_data

st.title("Cost, Margin & Break-even Dashboard")

st.sidebar.header("Business Inputs")

selling_price = st.sidebar.number_input("Selling Price per Unit ($)", value=299.0)
monthly_units_sold = st.sidebar.number_input("Monthly Units Sold", value=100)

business = load_business_data()

kpis = calculate_kpis(total_production_cost=business["total_production_cost"],
    production_units=business["production_units"],
    selling_price=selling_price,
    monthly_units_sold=monthly_units_sold,
    fixed_costs=business["fixed_costs"],
    variable_cost_per_unit=business["variable_cost_per_unit"]
)

col1, col2, col3 = st.columns(3)
col1.metric("Total Production Cost", f"${kpis['total_production_cost']:,.0f}")
col2.metric("Cost per Unit", f"${kpis['cost_per_unit']:,.2f}")
col3.metric("Selling Price", f"${kpis['selling_price']:,.2f}")

col4, col5, col6 = st.columns(3)
col4.metric("Gross Profit / Unit", f"${kpis['gross_profit_per_unit']:,.2f}")
col5.metric("Gross Margin %", f"{kpis['gross_margin_pct']:.1f}%")
col6.metric("Break-even Quantity", f"{kpis['break_even_quantity']:,.0f} units")

col7, col8 = st.columns(2)
col7.metric("Monthly Revenue", f"${kpis['monthly_revenue']:,.0f}")
col8.metric("Monthly Profit", f"${kpis['monthly_profit']:,.0f}")

st.divider()

st.plotly_chart(cost_breakdown_chart(), use_container_width=True)

st.subheader("Business Interpretation")

if kpis["gross_margin_pct"] < 25:
    st.warning("Gross margin is low. The business should review pricing and major cost drivers.")
elif kpis["gross_margin_pct"] < 40:
    st.info("Gross margin is acceptable, but cost optimization could improve profitability.")
else:
    st.success("Gross margin is strong at the current selling price.")
