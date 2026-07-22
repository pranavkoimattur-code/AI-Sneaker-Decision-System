import pandas as pd

def load_business_data():

    totals = pd.read_excel(
        "data/production_cost.xlsx",
        sheet_name="Totals"
    )

    one_unit = pd.read_excel(
        "data/production_cost.xlsx",
        sheet_name="To make 1"
    )

    business_data = {
        "total_production_cost": 538819,
        "production_units": 1000,
        "cost_per_unit": 538.82,
        "selling_price": 699,
        "fixed_costs": 441087,
        "variable_cost_per_unit": 97.73,
        "monthly_units_sold": 100
    }

    return business_data




