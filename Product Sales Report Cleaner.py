import streamlit as st
import pandas as pd
import os
from openpyxl import load_workbook
from openpyxl.styles import Border, Side

def clean_excel():
    # Get the first Excel file in the directory
    files = [f for f in os.listdir() if (f.endswith(".xls") or f.endswith(".xlsx")) and not f.startswith("~")]
    if not files:
        print("No Excel file found in the current directory.")
        return
    
    file_path = files[0]  # Pick the first Excel file found
    
    # Load the Excel file with headers on row 3 (zero-indexed row 2)
    df = pd.read_excel(file_path, dtype=str, header=2)
    
    # Keep only the required columns
    required_columns = ["Description", "U O M", "Quantity"]
    df = df[required_columns]
    
    # Convert Quantity column to numeric
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors='coerce')
    
    # Load the full data to check for department filtering
    df_full = pd.read_excel(file_path, dtype=str, header=2)
    
    # Define the allowed department values
    allowed_departments = {
        "Hot Hors D’Oeuvres", "Sandwich Platters", "Platters", "Hot & Ready ",
        "Food", "Bakery Items and Breakfast Pastries", "Salad Bowls "
    }
    
    # Filter rows based on the "Department" column from the original file
    if "Department" in df_full.columns:
        df = df[df_full["Department"].isin(allowed_departments)]
    
    # Get the first row (title) from the original file (row 0)
    df_header = pd.read_excel(file_path, dtype=str, header=None, nrows=1)
    
    # Generate output file path
    base_name, ext = os.path.splitext(file_path)
    output_file = f"{base_name}_processed.xlsx"  # Always save as .xlsx
    
    # Save the cleaned data to a temporary file
    df.to_excel(output_file, index=False, engine="openpyxl")
    
    # Load the workbook to modify formatting
    wb = load_workbook(output_file)
    ws = wb.active
    
    # Insert the title row (first row) at the top (above the table)
    for col_num, value in enumerate(df_header.iloc[0], start=1):  # df_header is a DataFrame with one row
        ws.cell(row=1, column=col_num).value = value
    
    # Set border style for the cleaned data (after the header row)
    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))
    
    # Apply border to all cells in the data (starting from row 2)
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            if cell.value:  # Only apply borders to non-empty cells
                cell.border = thin_border
    
    # Adjust column widths
    for col in ws.columns:
        max_length = 0
        col_letter = col[0].column_letter  # Get the column letter
        for cell in col:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        adjusted_width = max_length + 2
        ws.column_dimensions[col_letter].width = adjusted_width
    
    # Save the formatted workbook
    wb.save(output_file)
    
    print(f"Processed file saved as: {output_file}")

# Run the function
clean_excel()
