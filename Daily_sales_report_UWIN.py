#!/usr/bin/env python
# coding: utf-8

# In[1]:

import streamlit as st

# Example app
st.title("Daily_sales")
st.write("Hello, this is daily sales cleaner web app!")


import pandas as pd

# Load the two CSV files
file1 = pd.read_csv('media.csv')
file2 = pd.read_csv('trove.csv')

# Fill empty cells in specific columns (Year, Month, Week, Day of Month, Day of Week, Terminal, Bill Type) based on the previous row's value in both files
columns_to_fill_file1 = ['Year', 'Month', 'Week', 'Date', 'Day of Week', 'Terminal']
columns_to_fill_file2 = ['Year', 'Month', 'Week', 'Date', 'Day of Week', 'Terminal', 'Bill Type']

file1[columns_to_fill_file1] = file1[columns_to_fill_file1].fillna(method='ffill')
file2[columns_to_fill_file2] = file2[columns_to_fill_file2].fillna(method='ffill')

# Rename 'Date' to 'Day of Month' in both files
file1.rename(columns={'Date': 'Day'}, inplace=True)
file2.rename(columns={'Date': 'Day'}, inplace=True)

# Rename 'Media' to 'Bill Type' and 'Net' to 'Total' to match file2 for consistency
file1.rename(columns={'Media': 'Bill Type', 'Net': 'Total'}, inplace=True)

# Concatenate the two dataframes (instead of merging)
common_columns = ['Bill Type', 'Terminal', 'Count', 'Year', 'Month', 'Week', 'Day', 'Day of Week']
final_table = pd.concat([file1[common_columns + ['Collected', 'Tip', 'Total']], 
                         file2[common_columns + ['Total']]], ignore_index=True)

# Make sure 'Year', 'Month', and 'Day of Month' are present and valid
final_table['Year'] = pd.to_numeric(final_table['Year'], errors='coerce')
final_table['Month'] = pd.to_numeric(final_table['Month'], errors='coerce')
final_table['Day'] = pd.to_numeric(final_table['Day'], errors='coerce')

# Now, create 'Date' column from 'Year', 'Month', and 'Day of Month'
final_table['Date'] = pd.to_datetime(final_table[['Year', 'Month', 'Day']], errors='coerce')

# Define the mapping for 'Profit center' based on 'Terminal'
profit_center_mapping = {
    'Cashier_1': 'CAW Market', 'Cashier_2': 'CAW Market', 'Cashier_3': 'CAW Market', 'Cashier_4': 'CAW Market', 'Flip_1': 'CAW Market', 'Flip_2': 'CAW Market',
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

# Add 'Profit center' column based on 'Terminal'
final_table['Profit center'] = final_table['Terminal'].map(profit_center_mapping)

# Export the final dataframe to a CSV file
final_table.to_csv('final_file.csv', index=False)

print("Final CSV file generated as 'final_file.csv'")


# In[ ]:




