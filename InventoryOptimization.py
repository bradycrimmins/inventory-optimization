import pandas as pd
import pulp 
from sqlalchemy import create_engine

# Placeholder connection strings
cloud_db_string = 'cloud_database_connection_string'
on_prem_db_string = 'on_premises_database_connection_string'

# Connect to cloud and on-premises databases
cloud_engine = create_engine(cloud_db_string)
on_prem_engine = create_engine(on_prem_db_string)

# Dynamically fetch sales data
sales_query = """
SELECT product_id, location_id, SUM(quantity_sold) AS total_sold, shelf_life_days 
FROM sales_data 
JOIN product_details ON sales_data.product_id = product_details.id
GROUP BY product_id, location_id;
"""
sales_data = pd.read_sql(sales_query, cloud_engine)

# Dynamically fetch inventory and cost data
inventory_query = """
SELECT product_id, location_id, holding_cost, ordering_cost, lead_time_days, echelon 
FROM inventory_costs
JOIN locations ON inventory_costs.location_id = locations.id;
"""
inventory_data = pd.read_sql(inventory_query, on_prem_engine)

# Merge datasets for optimization
data_for_optimization = pd.merge(sales_data, inventory_data, on=['product_id', 'location_id'], how='inner')

# Assume demand_forecasts and other necessary data are dynamically fetched and stored in data_for_optimization

# Initialize the optimization problem
problem = pulp.LpProblem("Advanced_Inventory_Optimization", pulp.LpMinimize)

# Decision Variables
order_quantities = pulp.LpVariable.dicts("OrderQuantity",
                                         [(row['product_id'], row['location_id']) for index, row in data_for_optimization.iterrows()],
                                         lowBound=0,
                                         cat='Continuous')

# Objective Function: Minimize total costs and waste from perishables
problem += (
    pulp.lpSum([
        order_quantities[(product, location)] * row['ordering_cost'] + 
        0.5 * order_quantities[(product, location)] * row['holding_cost'] - 
        0.1 * min(row['shelf_life_days'] - row['lead_time_days'], 0) * order_quantities[(product, location)]  # Waste penalty
        for (product, location), row in data_for_optimization.iterrows()
    ]),
    "Total Cost and Waste Minimization"
)

# Multi-echelon Constraints: Balancing inventory across levels
for (product, location), row in data_for_optimization.iterrows():
    if row['echelon'] == 1:
        # Higher echelon: ensure enough stock is ordered to supply lower echelons
        problem += order_quantities[(product, location)] >= 1.2 * row['total_sold'], f"High_Echelon_Supply_{product}_{location}"
    else:
        # Lower echelon: direct demand fulfillment
        problem += order_quantities[(product, location)] >= row['total_sold'], f"Demand_Fulfillment_{product}_{location}"

# Solve the problem
problem.solve()

# Output results
for var in order_quantities:
    print(f"Order Quantity for {var}: {order_quantities[var].varValue}")