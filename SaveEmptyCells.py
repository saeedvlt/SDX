import streamlit as st

# Example app
st.title("Fill Empty Cells")
st.write("Fills out empty cells between two cells with a value based on the top cell value")

import pandas as pd

# Read the CSV file
df = pd.read_csv('sales.csv')

# Identify columns with missing values
columns_with_nan = [col for col in df.columns if df[col].isnull().any()]

# Display columns with missing values and ask the user which ones to fill
if columns_with_nan:
    print("The following columns have missing values:")
    for i, col in enumerate(columns_with_nan, 1):
        print(f"{i}. {col}")
    
    # Prompt user to enter column numbers to fill, separated by commas
    selected_columns = input("Enter the numbers of the columns you want to fill (e.g., '1,3'): ")
    selected_columns = [columns_with_nan[int(i)-1] for i in selected_columns.split(",")]

    # Fill missing values in the selected columns
    for col in selected_columns:
        df[col] = df[col].fillna(method='ffill')

# Export the modified dataframe to a new CSV file
df.to_csv('output_file.csv', index=False)

print("Processing complete. Output saved as 'output_file.csv'")
