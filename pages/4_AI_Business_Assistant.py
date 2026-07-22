import streamlit as st

from utils.calculations import calculate_kpis
from utils.data_loader import load_business_data
from utils.llm_advisor import ask_business_advisor


st.title("AI Business Assistant")
st.subheader("Ask questions about the Smart Sneaker Display Case business")

business = load_business_data()

selling_price = st.sidebar.number_input(
    "Selling Price per Unit ($)",
    min_value=0.0,
    value=float(business["selling_price"]),
    step=5.0,
)

monthly_units_sold = st.sidebar.number_input(
    "Monthly Units Sold",
    min_value=0,
    value=int(business["monthly_units_sold"]),
    step=10,
)

kpis = calculate_kpis(
    total_production_cost=business["total_production_cost"],
    production_units=business["production_units"],
    selling_price=selling_price,
    monthly_units_sold=monthly_units_sold,
    fixed_costs=business["fixed_costs"],
    variable_cost_per_unit=business["variable_cost_per_unit"],
)

llm_data = {
    **business,
    "selling_price": selling_price,
    "monthly_units_sold": monthly_units_sold,
    "gross_profit_per_unit": kpis["gross_profit_per_unit"],
    "gross_margin_pct": kpis["gross_margin_pct"],
    "monthly_revenue": kpis["monthly_revenue"],
    "monthly_profit": kpis["monthly_profit"],
    "break_even_quantity": kpis["break_even_quantity"],
}

question = st.text_area(
    "Ask a business question",
    placeholder=(
        "Examples:\n"
        "Why is our cost per unit high?\n"
        "How can we improve our gross margin?\n"
        "What selling price would support a 40% margin?\n"
        "Which cost category should we reduce first?"
    ),
)

if st.button("Ask AI"):
    if not question.strip():
        st.warning("Enter a question first.")
    else:
        try:
            with st.spinner("Analyzing the business data..."):
                answer = ask_business_advisor(
                    business_data=llm_data,
                    question=question,
                )

            st.subheader("AI Response")
            st.write(answer)

        except Exception as error:
            st.error(f"Unable to generate an AI response: {error}")

with st.expander("View data sent to the AI"):
    st.json(llm_data)
