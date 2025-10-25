import streamlit as st
import pandas as pd

def opex_cabang_monthly(file):
    """
    Combine multiple sheets into one using the first sheet as the master list.
    Sheets are matched like a VLOOKUP based on shared keys.
    """
    # Read all sheets
    all_sheets = pd.read_excel(file, sheet_name=None)
    sheet_names = list(all_sheets.keys())

    # First sheet = master
    master_name = sheet_names[0]
    master_df = all_sheets[master_name].copy()

    # Normalize column names
    master_df.columns = master_df.columns.str.strip()

    # Merge the rest of the sheets using left joins (VLOOKUP-style)
    for sheet_name in sheet_names[1:]:
        df = all_sheets[sheet_name].copy()
        df.columns = df.columns.str.strip()

        # Find common columns to join on (like VLOOKUP keys)
        common_cols = list(set(master_df.columns).intersection(set(df.columns)))
        if not common_cols:
            st.warning(f"⚠ No matching columns found between '{master_name}' and '{sheet_name}' — skipped.")
            continue

        # Merge, keeping master order
        master_df = pd.merge(master_df, df, on=common_cols, how="left")

    # Save output file
    output_file = "Opex_Combined_vlookup_style.xlsx"
    master_df.to_excel(output_file, index=False)
    return output_file


def main():
    st.title("🏢 Opex Cabang Monthly Merger")
    st.markdown(
        """
        Combine all monthly Opex Cabang sheets into one Excel file.  
        The first sheet will be used as the **master list** (complete variables).  
        Other sheets are matched **VLOOKUP-style** based on shared columns.
        """
    )

    opex_file = st.file_uploader("📄 Upload Opex Cabang file", type=["xlsx"])

    if opex_file is not None:
        with st.spinner("Processing your Opex Cabang Monthly file..."):
            output = opex_cabang_monthly(opex_file)
        st.success("✅ Opex Cabang Monthly file generated successfully!")
        
        with open(output, "rb") as f:
            st.download_button(
                "⬇ Download Combined Excel File",
                f,
                file_name="Opex_Wuling_All_Cabang_Monthly.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

if __name__ == "__main__":
    main()
