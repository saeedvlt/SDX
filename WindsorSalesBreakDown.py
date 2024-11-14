import pandas as pd

# Step 1: Load the CSV file, specifying low_memory=False to avoid dtype warnings
df = pd.read_csv('sales.csv', low_memory=False)

# Step 2: Fill empty spaces with the value from the cell above in each column
df.ffill(inplace=True)

# Step 3: Rename the 'Date' column to 'Day'
df.rename(columns={'Date': 'Day'}, inplace=True)

# Step 4: Add a new 'Date' column by combining Day, Month, and Year columns
# First, clean the Day, Month, Year to avoid invalid entries (e.g., non-numeric)
df = df[df['Day'].astype(str).str.isdigit() & df['Month'].astype(str).str.isdigit() & df['Year'].astype(str).str.isdigit()]

# Convert the Day, Month, and Year to a proper datetime format
df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']].astype(str).agg('-'.join, axis=1), format='%Y-%m-%d', errors='coerce')

# Step 5: Create a dictionary for the profit centers based on the 'Terminal' values
profit_center_mapping = {
    'Cashier_1': 'CAW Market', 'Cashier_2': 'CAW Market', 'Cashier_3': 'CAW Market', 'Cashier_4': 'CAW Market', 
    'Flip_1': 'CAW Market', 'Flip_2': 'CAW Market',
    'Cashier_5': 'Origins',
    'Cashier_6': 'Odette (Dividends)', 'Flip_3': 'Odette (Dividends)',
    'Cashier_7': 'Alumni Hall (The Corner)',
    'Cashier_8': 'Toldo Athletic',
    'Cashier_9': 'Croc', 'Cashier_10': 'Croc',
    'Cashier_11': 'CEI (Tim Hortons)',
    'Cashier_13': 'CAW - Starbucks', 'Cashier_14': 'CAW - Starbucks',
    'Cashier_16': 'Chatime - Leddy',
    'Cashier_15': 'Law',
    'Flip_4': 'Downtown'
}

# Step 6: Add the 'Profit Center' column and fill it based on the 'Terminal' values
df['Profit Center'] = df['Terminal'].map(profit_center_mapping)

# Step 7: Create a dictionary for the brands based on the 'Division' values
brands_mapping = {
    'Booster Juice': 'Booster Juice',
    'Subway': 'Subway',
    'Pizza Pizza': 'Pizza Pizza',
    'Tim Hortons': 'Tim Hortons',
    'Chatime': 'Chatime', 
    'Starbucks': 'Starbucks'
}

# Step 8: Add the 'Brands' column and fill it based on the 'Division' values, default to 'SDX'
df['Brands'] = df['Division'].map(brands_mapping).fillna('SDX')

# Step 9: Define the desired column order
column_order = [
    'Terminal', 'Year', 'Month', 'Week', 'Day', 'Date', 'Day of Week',
    'Division', 'Menu Item', 'Category', 'Group', 'Net Sales','Net Qty',
    'Profit Center', 'Brands'
]

# Reorder the DataFrame columns
df = df[column_order]

# Step 10: Save the modified DataFrame to a new CSV file
df.to_csv('Brands.csv', index=False)

print("CSV file 'Brands.csv' has been created successfully with the specified column order!")
