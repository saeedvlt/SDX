#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd

# Example app
st.title("Conf sales table cleaner")
st.write("This web app cleans the sales data from Conf.")

# Upload the CSV file
uploaded_file = st.file_uploader("Choose the CSV file (media.csv)", type="csv")

if uploaded_file is not None:
    # Read the CSV file
    file1 = pd.read_csv(uploaded_file)

    # Display the raw CSV data
    st.write("Original CSV File:")
    st.write(file1)

    # Fill empty cells in specific columns (Year, Month, Week, Day, Day of Week, Terminal) based on the previous row's value in the file
    columns_to_fill_file1 = ['Year', 'Month', 'Week', 'Date', 'Day of Week', 'Terminal']
    file1[columns_to_fill_file1] = file1[columns_to_fill_file1].fillna(method='ffill')

    # Rename 'Date' to 'Day'
    file1.rename(columns={'Date': 'Day'}, inplace=True)

    # Select the common columns and additional columns
    common_columns = ['Media', 'Terminal', 'Count', 'Year', 'Month', 'Week', 'Day', 'Day of Week']
    final_table = file1[common_columns + ['Collected', 'Tip', 'Net']]

    # Ensure 'Year', 'Month', and 'Day' are numeric
    final_table['Year'] = pd.to_numeric(final_table['Year'], errors='coerce')
    final_table['Month'] = pd.to_numeric(final_table['Month'], errors='coerce')
    final_table['Day'] = pd.to_numeric(final_table['Day'], errors='coerce')

    # Create 'Date' column from 'Year', 'Month', and 'Day'
    final_table['Date'] = pd.to_datetime(final_table[['Year', 'Month', 'Day']], errors='coerce')

    # Display the processed table
    st.write("Processed Table:")
    st.write(final_table)

    # Allow the user to download the final processed CSV file
    st.download_button(label="Download Processed CSV", data=final_table.to_csv(index=False), file_name='final_file.csv', mime='text/csv')

else:
    st.write("Please upload a CSV file to proceed.")
