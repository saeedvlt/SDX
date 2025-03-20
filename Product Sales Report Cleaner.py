import streamlit as st
import pandas as pd
import io
from openpyxl import load_workbook
from openpyxl.styles import Border, Side

# Streamlit UI
st.title("Product Sales Report Cleaner")
st.write("This web app cleans the Product Sales Report for Kitchen Uwin")

# Upload the Excel file
uploaded_file = st.file_uploader("Choose the Excel file (media.xls or media.xlsx)", type=["xls", "xlsx"])

def clean_excel(file):
    """Cleans the uploaded Excel file and returns a processed file in-memory."""

    # Read the uploaded file (choose correct engine)
    engine = "xlrd" if file.name.endswith(".xls") else "openpyxl"
    df = pd.read_excel(file, dtype=str, header=2, engine=engine)

    # Keep only the required columns
    required_columns = ["Description", "U O M", "Quantity"]
    df = df[required_columns]

    # Convert Quantity column to numeric
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors='coerce')

    # Load the full data again to check for department filtering
    df_full = pd.read_excel(file, dtype=str, header=2, engine=engine)

    # Define allowed department values
    allowed_departments = {
        "Hot Hors D’Oeuvres", "Sandwich Platters", "Platters", "Hot & Ready ",
        "Food", "Bakery Items and Breakfast Pastries", "Salad Bowls "
    }

    # Filter rows based on the "Department" column from the original file
    if "Department" in df_full.columns:
        df = df[df_full["Department"].isin(allowed_departments)]

    # Get the first row (title) from the original file (row 0)
    df_header = pd.read_excel(file, dtype=str, header=None, nrows=1, engine=engine)

    # Save the cleaned data to a BytesIO stream
    output_stream = io.BytesIO()
    df.to_excel(output_stream, index=False, engine="openpyxl")
    output_stream.seek(0)  # Reset stream position

    # Load workbook from stream
    wb = load_workbook(output_stream)
    ws = wb.active

    # Insert title row at the top
    ws.insert_rows(1)  # Insert a new row at the top
    for col_num, value in enumerate(df_header.iloc[0], start=1):
        ws.cell(row=1, column=col_num).value = value

    # Apply borders only to table data (excluding header row)
    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))

    for row in ws.iter_rows(min_row=2):  # Apply borders only from the second row onwards
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

    # Save modified workbook to a new BytesIO stream
    final_output_stream = io.BytesIO()
    wb.save(final_output_stream)
    final_output_stream.seek(0)

    return final_output_stream

# If a file is uploaded, process it
if uploaded_file:
    cleaned_file = clean_excel(uploaded_file)

    # Provide download button for the cleaned file
    st.download_button(
        label="Download Cleaned File",
        data=cleaned_file,
        file_name="cleaned_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
