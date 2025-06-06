import pandas as pd
import streamlit as st

# Example app
st.title("Fill Missing Values in Selected Columns")
st.write("Fills out empty cells between two cells with a value based on the top cell value")

# File uploader for users to upload the CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv", "CSV"])

# Process the file if it is uploaded
if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)

    # Identify columns with missing values
    columns_with_nan = [col for col in df.columns if df[col].isnull().any()]

    # Display columns with missing values and ask the user which ones to fill
    if columns_with_nan:
        st.write("The following columns have missing values:")
        for i, col in enumerate(columns_with_nan, 1):
            st.write(f"{i}. {col}")

        # Let user select columns to fill
        selected_columns = st.multiselect("Select the columns you want to fill", options=columns_with_nan)

        # Fill missing values in the selected columns
        for col in selected_columns:
            df[col] = df[col].fillna(method='ffill')

        # Display the processed dataframe
        st.write("Processed DataFrame:", df)

        # Provide a download button for the modified file
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download modified CSV",
            data=csv,
            file_name="output_file.csv",
            mime="text/csv"
        )

    else:
        st.write("No columns with missing values were found in the uploaded file.")
else:
    st.write("Please upload a CSV file to begin processing.")
