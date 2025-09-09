# app.py
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="SB Daily Report Generator", layout="centered")
st.title("SB Daily Report — CSV lookup & export")
st.write("Upload a CSV. The app will look up items in column A and grab the corresponding column B value.")

# Items to look up
ITEMS = [
    "Net Sales", "Tax Collected", "Total Revenue", "Total Discount",
    "Debit", "SUBX Card", "UWIN Charge", "VISA", "MOP",
    "Mastercard", "AMEX", "Check Count", "Total Collection"
]

uploaded_file = st.file_uploader("Upload CSV file (must contain at least two columns)", type=["csv"])
fill_zero = st.checkbox("Fill missing items with 0 (unchecked -> leave blank/NaN)", value=True)

if uploaded_file is not None:
    try:
        # Read CSV (Streamlit gives a file-like object)
        df = pd.read_csv(uploaded_file)

        # Basic validation
        if df.shape[1] < 2:
            st.error("The uploaded CSV must have at least two columns (Column A and Column B).")
        else:
            st.markdown("**Preview of uploaded file (first 5 rows):**")
            st.dataframe(df.head())

            # Build fast lookup from Column A -> Column B (case-insensitive, trimmed)
            col_a = df.iloc[:, 0].astype(str).str.strip()
            col_b = df.iloc[:, 1]
            pairs = pd.DataFrame({"k": col_a.str.lower(), "v": col_b}).drop_duplicates(subset="k", keep="first")
            lookup = dict(zip(pairs["k"], pairs["v"]))

            # Create result
            values = []
            for item in ITEMS:
                raw = lookup.get(item.lower())
                if pd.isna(raw) or raw is None:
                    val = 0 if fill_zero else ""
                else:
                    val = raw
                values.append(val)

            final_df = pd.DataFrame({
                "Item": ITEMS,
                "Value": values,
                "Date": date.today().strftime("%Y-%m-%d"),
                "Store": "Starbucks"
            })

            st.markdown("**Result table:**")
            st.dataframe(final_df)

            # Prepare CSV for download
            csv_bytes = final_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download SB_daily_report.csv",
                data=csv_bytes,
                file_name="SB_daily_report.csv",
                mime="text/csv"
            )

            st.success("Done — export is ready.")
    except Exception as e:
        st.error(f"Error reading or processing the CSV: {e}")
