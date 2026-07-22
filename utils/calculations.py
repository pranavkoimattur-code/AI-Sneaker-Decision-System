from typing import Any


def _as_number(value: Any, field_name: str) -> float:
    """
    Convert an input value to a float and produce a clear error
    if a list or other invalid type is supplied.
    """
    if isinstance(value, list):
        raise TypeError(
            f"{field_name} must be a number, but received a list: {value}"
        )

    try:
        return float(value)
    except (TypeError, ValueError) as error:
        raise TypeError(
            f"{field_name} must be numeric. Received: {value!r}"
        ) from error


def calculate_kpis(
    total_production_cost: float,
    production_units: int,
    selling_price: float,
    monthly_units_sold: int,
    fixed_costs: float,
    variable_cost_per_unit: float,
) -> dict[str, float]:
    """
    Calculate production, pricing, margin, revenue, profit,
    and break-even KPIs.
    """

    total_production_cost = _as_number(
        total_production_cost,
        "total_production_cost",
    )

    production_units = _as_number(
        production_units,
        "production_units",
    )

    selling_price = _as_number(
        selling_price,
        "selling_price",
    )

    monthly_units_sold = _as_number(
        monthly_units_sold,
        "monthly_units_sold",
    )

    fixed_costs = _as_number(
        fixed_costs,
        "fixed_costs",
    )

    variable_cost_per_unit = _as_number(
        variable_cost_per_unit,
        "variable_cost_per_unit",
    )

    if production_units <= 0:
        raise ValueError("production_units must be greater than zero.")

    cost_per_unit = total_production_cost / production_units

    gross_profit_per_unit = selling_price - cost_per_unit

    gross_margin_pct = (
        gross_profit_per_unit / selling_price * 100
        if selling_price > 0
        else 0.0
    )

    monthly_revenue = selling_price * monthly_units_sold

    monthly_profit = gross_profit_per_unit * monthly_units_sold

    contribution_margin_per_unit = (
        selling_price - variable_cost_per_unit
    )

    break_even_quantity = (
        fixed_costs / contribution_margin_per_unit
        if contribution_margin_per_unit > 0
        else 0.0
    )

    return {
        "total_production_cost": total_production_cost,
        "production_units": production_units,
        "cost_per_unit": cost_per_unit,
        "selling_price": selling_price,
        "gross_profit_per_unit": gross_profit_per_unit,
        "gross_margin_pct": gross_margin_pct,
        "break_even_quantity": break_even_quantity,
        "monthly_revenue": monthly_revenue,
        "monthly_profit": monthly_profit,
        "variable_cost_per_unit": variable_cost_per_unit,
        "contribution_margin_per_unit": contribution_margin_per_unit,
    }
