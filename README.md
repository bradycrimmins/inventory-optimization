## Inventory Optimization Script

## Overview

This Python script is designed for advanced inventory optimization across a multi-echelon supply chain network. It integrates sales data, inventory levels, and cost information from both cloud and on-premises databases to create a comprehensive dataset for optimization. The script uses the PuLP library to model and solve the inventory optimization problem, aiming to minimize total costs and waste, especially from perishable goods, while ensuring that inventory levels are balanced across different echelons of the supply chain.

## Features

- **Dynamic Data Fetching**: Automatically retrieves sales and inventory data from cloud and on-premises databases using SQL queries, ensuring that the optimization model uses the most up-to-date information.
- **Data Merging**: Combines sales data with inventory and cost data based on product and location IDs to create a unified dataset for optimization.
- **Linear Programming Optimization**: Utilizes the PuLP library to define and solve a linear programming problem that minimizes total inventory costs, including holding costs and penalties for waste.
- **Multi-Echelon Constraints**: Incorporates constraints to maintain adequate stock levels across different supply chain echelons, accommodating both higher-level supply requirements and direct demand fulfillment needs.

## Requirements

- Python 3.x
- pandas
- SQLAlchemy
- PuLP

Ensure you have the required libraries installed:

```bash
pip install pandas sqlalchemy pulp
```

## Setup

1. **Database Connections**: Update the `cloud_db_string` and `on_prem_db_string` placeholders in the script with your actual cloud and on-premises database connection strings.
2. **SQL Queries**: Adjust the `sales_query` and `inventory_query` according to your database schema and tables.

## Usage

Run the script in your Python environment. The script performs the following steps:

1. Connects to specified cloud and on-premises databases.
2. Executes SQL queries to fetch sales and inventory data.
3. Merges the datasets based on product and location IDs.
4. Defines a linear programming problem to minimize costs and waste.
5. Solves the optimization problem and prints the recommended order quantities for each product and location combination.

## Customization

- **Optimization Criteria**: You can modify the objective function and constraints within the PuLP problem definition to align with your specific business objectives and supply chain dynamics.
- **Data Sources**: The script can be adjusted to fetch data from additional or alternative sources as needed, including APIs or other database systems.

## Note

This script is provided as a template for advanced inventory optimization. Depending on the complexity of your supply chain and the specifics of your data, further customization and refinement of the optimization model may be necessary to achieve desired results.
