#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd

# Example app
st.title("Daily Sales Report Cleaner")
st.write("Hello, this is a daily sales cleaner web app!")

# Upload the two CSV files
uploaded_file1 = st.file_uploader("Choose the first CSV file (media.csv)", type=["csv", "CSV"], key="file1")
uploaded_file2 = st.file_uploader("Choose the second CSV file (trove.csv)", type=["csv", "CSV"], key="file2")

if uploaded_file1 is not None and uploaded_file2 is not None:
    # Read the CSV files
    file1 = pd.read_csv(uploaded_file1)
    file2 = pd.read_csv(uploaded_file2)

    st.write("First file (media.csv):")
    st.write(file1)

    st.write("Second file (trove.csv):")
    st.write(file2)

    # Fill empty cells in specific columns (Year, Month, Week, Day of Month, Day of Week, Terminal, Bill Type) in both files
    #columns_to_fill_file1 = ['Year', 'Month', 'Week', 'Date', 'Terminal']
    #columns_to_fill_file2 = ['Year', 'Month', 'Week', 'Date', 'Terminal', 'Bill Type']

    # if there is any problems regarding day of week, replace the line 27 and 28 with the following lines which includes column "Day of Week" as well.
    columns_to_fill_file1 = ['Year', 'Month', 'Week', 'Date', 'Day of Week', 'Terminal']
    columns_to_fill_file2 = ['Year', 'Month', 'Week', 'Date', 'Day of Week', 'Terminal', 'Bill Type']    

    file1[columns_to_fill_file1] = file1[columns_to_fill_file1].fillna(method='ffill')
    file2[columns_to_fill_file2] = file2[columns_to_fill_file2].fillna(method='ffill')

    # Rename 'Date' to 'Day of Month' in both files
    file1.rename(columns={'Date': 'Day'}, inplace=True)
    file2.rename(columns={'Date': 'Day'}, inplace=True)

    # Rename 'Media' to 'Bill Type' and 'Net' to 'Total' in file1 to match file2 for consistency
    file1.rename(columns={'Media': 'Bill Type', 'Net': 'Total'}, inplace=True)

    # Concatenate the two dataframes
    common_columns = ['Bill Type', 'Terminal', 'Count', 'Year', 'Month', 'Week', 'Day', 'Day of Week']
    final_table = pd.concat([file1[common_columns + ['Collected', 'Tip', 'Total']], 
                             file2[common_columns + ['Total']]], ignore_index=True)

    # Make sure 'Year', 'Month', and 'Day of Month' are numeric
    final_table['Year'] = pd.to_numeric(final_table['Year'], errors='coerce')
    final_table['Month'] = pd.to_numeric(final_table['Month'], errors='coerce')
    final_table['Day'] = pd.to_numeric(final_table['Day'], errors='coerce')

    # Create 'Date' column from 'Year', 'Month', and 'Day of Month'
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

    # Show the final concatenated table
    st.write("Final Table:")
    st.write(final_table)

    # Allow the user to download the final table as a CSV file
    st.download_button(label="Download Final CSV", data=final_table.to_csv(index=False), file_name='final_file.csv', mime='text/csv')

else:
    st.write("Please upload both CSV files to proceed.")
