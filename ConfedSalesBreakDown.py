#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd

# Example app
st.title("Conf sales break down")
st.write("This web app breaks down the sales from Conf.")
import pandas as pd

# Upload the CSV file
uploaded_file = st.file_uploader("Choose the CSV file (sales.csv)", type="csv")

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
    'AceKiosk1': 'Vending Ace Kiosk',
    'AceTerm1': 'Ace Term',
    'BGTerm1': 'Dorion',
    'MclntyreTerm1': 'McIntyre', 
    'Primary': 'Primary',
    'RyanHallTerm1': 'Ryan Hall',
    'RyanHallTerm2': 'Ryan Hall',
    'RyanHallTerm3': 'Ryan Hall'
}

# Step 6: Add the 'Profit Center' column and fill it based on the 'Terminal' values
df['Profit Center'] = df['Terminal'].map(profit_center_mapping)


# Step 7: Create a dictionary for the brands based on the 'Division' values
brands_mapping = {
    'Bento Sushi': 'Bento Sushi',
    'Tim Hortons': 'Tim Hortons',
}

# Step 8: Add the 'Brands' column and fill it based on the 'Division' values, default to 'SDX'
df['Brands'] = df['Division'].map(brands_mapping).fillna('SDX')

# Step 9: Define the desired column order
column_order = [
    'Terminal', 'Year', 'Month', 'Week', 'Day', 'Date', 'Day of Week',
    'Division', 'Menu Item', 'Category', 'Group', 'Net Sales','Net Qty', 'Brands', 'Profit Center'
]

# Reorder the DataFrame columns
df = df[column_order]

# Step 10: Save the modified DataFrame to a new CSV file
df.to_csv('Brands.csv', index=False)

print("CSV file 'Brands.csv' has been created successfully with the specified column order!")
