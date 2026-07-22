import plotly.express as px
import pandas as pd

def cost_breakdown_chart():
    df = pd.DataFrame({
        "Category": ["Fixed Costs", "Variable Costs", "Land", "Labor", "Capital"],
        "Cost": [441087, 97732, 4032, 361428, 173359],
    })

    return px.pie(
        df,
        names="Category",
        values="Cost",
        title="Cost Breakdown by Category",
    )
