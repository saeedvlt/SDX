#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd

# Title and description of the app
st.title("Sales Data Breakdown")
st.write("This app processes and organizes sales data.")

# Step 1: Upload the CSV file
uploaded_file = st.file_uploader("Choose the CSV file (e.g., sales.csv)", type=["csv", "CSV"])

# Only proceed if a file is uploaded
if uploaded_file is not None:
    try:
        # Load the CSV file into a DataFrame, specifying low_memory=False
        df = pd.read_csv(uploaded_file, low_memory=False)

        # Step 2: Fill empty spaces with the value from the cell above in each column
        df.ffill(inplace=True)

        # Step 3: Rename the 'Date' column to 'Day'
        df.rename(columns={'Date': 'Day'}, inplace=True)

        # Step 4: Add a new 'Date' column by combining Day, Month, and Year columns
        # Ensure Day, Month, and Year columns contain valid numeric values
        df = df[df['Day'].astype(str).str.isdigit() & 
                df['Month'].astype(str).str.isdigit() & 
                df['Year'].astype(str).str.isdigit()]

        # Convert Day, Month, and Year to a proper datetime format
        df['Date'] = pd.to_datetime(
            df[['Year', 'Month', 'Day']].astype(str).agg('-'.join, axis=1),
            format='%Y-%m-%d',
            errors='coerce'
        )

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
            'Division', 'Menu Item', 'Category', 'Group', 'Net Sales', 'Net Qty',
            'Profit Center', 'Brands'
        ]

        # Reorder the DataFrame columns
        df = df[column_order]

        # Display the final DataFrame in the Streamlit app
        st.write(df)

        # Step 10: Convert the modified DataFrame to CSV and make it downloadable
        csv = df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="Download Processed CSV",
            data=csv,
            file_name="Processed_Sales_Data.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.warning("Please upload a CSV file to proceed.")
