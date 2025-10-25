import streamlit as st
import pandas as pd
from io import BytesIO
import gc

def opex_cabang_monthly(file):
    """
    Combine multiple sheets into one using the first sheet as the master list.
    Sheets are matched like a VLOOKUP based on shared keys.
    """
    # ✅ Read the uploaded file once into memory
    excel_bytes = BytesIO(file.read())

    # ✅ Get sheet names without reading all data
    xls = pd.ExcelFile(excel_bytes)
    sheet_names = xls.sheet_names

    # ✅ Read only the first sheet fully
    master_name = sheet_names[0]
    master_df = pd.read_excel(xls, sheet_name=master_name)
    master_df.columns = master_df.columns.str.strip()

    # ✅ Merge the rest of the sheets one by one
    for sheet_name in sheet_names[1:]:
        st.info(f"🔄 Processing sheet: {sheet_name}")

        df = pd.read_excel(xls, sheet_name=sheet_name)
        df.columns = df.columns.str.strip()

        common_cols = list(set(master_df.columns).intersection(df.columns))
        if not common_cols:
            st.warning(f"⚠ No matching columns found between '{master_name}' and '{sheet_name}' — skipped.")
            continue

        master_df = pd.merge(master_df, df, on=common_cols, how="left")

        # ✅ Release memory from temporary DataFrame
        del df
        gc.collect()

    # ✅ Write to in-memory Excel buffer
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        master_df.to_excel(writer, index=False, sheet_name="Combined")

    output.seek(0)
    return output


def main():
    st.title("🏢 Opex Cabang Monthly")
    st.markdown("""
    Combine all monthly **Opex Cabang** sheets into one Excel file.  
    The first sheet is treated as the **master list**,  
    while others are joined **VLOOKUP-style** using shared columns.
    """)

    opex_file = st.file_uploader("📄 Upload Opex Cabang file", type=["xlsx"])

    if opex_file is not None:
        with st.spinner("Processing your Opex Cabang Monthly file..."):
            output = opex_cabang_monthly(opex_file)

        st.success("✅ Opex Cabang Monthly file generated successfully!")

        st.download_button(
            "⬇ Download Combined Excel File",
            data=output,
            file_name="Opex_Wuling_All_Cabang_Monthly.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


if __name__ == "__main__":
    main()
