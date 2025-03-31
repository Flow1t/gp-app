import streamlit as st
import pandas as pd
import requests
from io import BytesIO

st.set_page_config(page_title="Opex Summary")
st.sidebar.header("Opex Summary Generator")

def opex_summary(opex_file):
    file_url = {
        "opex_sum" : "https://raw.githubusercontent.com/Flow1t/gp-app/main/gp-app-1.0/opex%20sum.xlsx"
    }

    def load_excel_from_github(url, sheet_name=None):
        """Loads an Excel file from a GitHub raw URL and reads the specified sheet."""
        response = requests.get(url)
        
        if response.status_code == 200:
            excel_data = BytesIO(response.content)  # Convert to file-like object
            return pd.read_excel(excel_data, sheet_name=sheet_name, engine="openpyxl")  # Read the requested sheet
        else:
            raise FileNotFoundError(f"Failed to load Excel file from {url}. Status code: {response.status_code}")

    opex_sum = load_excel_from_github(file_url["opex_sum"], sheet_name = 'OPEX NAV 24')
    opex_sum = opex_sum.iloc[:, 1:]
    opex = pd.read_excel(opex_file, header = 6, sheet_name = "KONSOLIDASI")
    opex = opex.reset_index(drop=True)
    opex = opex.rename(columns={"Unnamed: 0": "Bulan"})
    opex = opex.dropna()

    opex_sum_transpose = opex_sum.transpose()
    opex_sum_transpose.columns = opex_sum_transpose.iloc[0]
    opex_sum_transpose = opex_sum_transpose[1:]
    opex_sum_transpose.columns = opex_sum_transpose.columns.fillna('')
    opex_sum_transpose = opex_sum_transpose.apply(
        lambda col: pd.to_numeric(col, errors='coerce').fillna(0).astype(int) 
        if col.dtypes == 'object' else col
    )

    opex_transpose = opex.transpose()
    opex_transpose.columns = opex_transpose.iloc[0]
    opex_transpose = opex_transpose[1:]
    opex_transpose = opex_transpose.apply(
        lambda col: pd.to_numeric(col, errors='coerce').fillna(0).astype(int) 
        if col.dtypes == 'object' else col
    )

    def aggregate_columns(df,df2, keyword, new_col_name):
        """Aggregates columns by keyword and sums them into a new column."""
        df2[new_col_name] = df.filter(regex=keyword).sum(axis=1)

    opex_sum_transpose['Net Sales Unit'] = opex_transpose['Penjualan Unit']
    opex_sum_transpose['Net Sales Spare Part'] = opex_transpose['Penjualan Spart & Bahan'] + opex_transpose['Retur Penjualan Spart & Bahan']
    opex_sum_transpose['Net Sales Service'] = opex_transpose['Pendapatan Jasa Servis']
    opex_sum_transpose['Total Net Sales'] = opex_transpose['Total Sales']

    opex_sum_transpose['Cost of Sales Unit'] = opex_transpose['Harga Pokok Penjualan Showroom']
    opex_sum_transpose['Cost of Sales Sparepart'] = opex_transpose['Harga Pokok Penjualan Service']
    opex_sum_transpose['Total Cost of Sales'] = opex_transpose['Total Cost']

    opex_sum_transpose["Gross Profit Unit"] = opex_transpose['Gross Profit Unit']
    opex_sum_transpose['Gross Profit Sparepart'] = opex_transpose['Gross Profit Workshop & Parts']
    opex_sum_transpose['Total Gross Profit'] = opex_transpose['Total Gross Profit']

    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)insentif', 'Selling Incentive')
    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)brosur|spanduk|event|promosi', 'Marketing Expense')
    opex_sum_transpose['Sales Commission'] = opex_transpose['Biaya Komisi Penjualan']
    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)pameran|iklan', 'Advertising & Promotions')
    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)bbm|transport|logistik|Biaya Perlengkapan Kendaraan|biaya penjualan lainnya|surat kendaraan', 'Shipping Expense')
    opex_sum_transpose['Predelivery Inspect'] = opex_transpose['Biaya PDC']
    opex_sum_transpose['Total Selling & Marketing Expense'] = opex_sum_transpose['Selling Incentive'] + opex_sum_transpose['Marketing Expense'] + opex_sum_transpose['Sales Commission'] + opex_sum_transpose['Advertising & Promotions'] + opex_sum_transpose['Shipping Expense'] + opex_sum_transpose['Predelivery Inspect']

    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)gaji|tunjangan hari raya', 'Salary Expense')
    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)lembur|rekreasi|duka cita', 'Employee Welfare')
    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)bpjs', 'Jamsostek & Pension')
    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)pemeliharaan|iuran rutin', 'Repair Maintenance')
    opex_sum_transpose['Tools'] = opex_transpose['Biaya Perlengkapan Bengkel']
    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)biaya sewa lain-lain', 'Rent Expense')
    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)representasi|cafetaria|rapat', 'Entertainment & Representation Expense') 
    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)listrik|air', 'Utilities Expense')
    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)telepon|internet|kirim dokumen', 'Communication Expense')
    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)dinas', 'Transportation & Travelling Expense')
    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)konsultan|ahli', 'Professional Fee')
    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)asuransi', 'Insurance Expense')
    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)training', 'Training Expense')
    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)reklame|materai', 'Taxes License')
    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)perlengkapan kantor|fotocopy|alat kantor', 'Office Supplies')
    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)website', 'IT Expense')
    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)psikotest|lowongan', 'Recruitment')
    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)seragam', 'Uniform')
    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)outsourcing', 'Security & Cleaning Expense')
    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)perijinan', 'Claim Expense')
    # aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)lain-lain', 'Miscellanous')
    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)provisi|credit', 'Bank Charge')

    opex_sum_transpose['Total General & Administratif Expense'] = opex_sum_transpose['Salary Expense'] + opex_sum_transpose['Employee Welfare'] + opex_sum_transpose ['Jamsostek & Pension'] + opex_sum_transpose['Repair Maintenance'] + opex_sum_transpose ['Tools'] + opex_sum_transpose['Rent Expense'] + opex_sum_transpose['Entertainment & Representation Expense'] + opex_sum_transpose['Utilities Expense'] + opex_sum_transpose['Communication Expense'] + opex_sum_transpose['Transportation & Travelling Expense'] + opex_sum_transpose['Insurance Expense'] + opex_sum_transpose['Training Expense'] + opex_sum_transpose['Taxes License'] + opex_sum_transpose['Office Supplies'] + opex_sum_transpose['IT Expense'] + opex_sum_transpose['Security & Cleaning Expense'] + opex_sum_transpose['Recruitment'] + opex_sum_transpose['Uniform'] + opex_sum_transpose['Claim Expense'] + opex_sum_transpose['Bank Charge'] + opex_sum_transpose['Professional Fee'] + opex_sum_transpose['Miscellanous']

    opex_sum_transpose['Total Operational Expense'] = opex_sum_transpose['Total Selling & Marketing Expense'] + opex_sum_transpose['Total General & Administratif Expense']

    opex_sum_transpose['EBIT'] = opex_sum_transpose['Total Gross Profit'] - opex_sum_transpose['Total Operational Expense']

    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)giro|deposito|Pendapatan Lain Rupa-Rupa', 'Interest Income/Expense Bank')
    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)dealer financing|biaya bunga bank', 'Interest Expense and Other Financial Charges')
    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)stnk', 'Other Income/Charges BBN & STNK')
    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)selisih', 'Other Income/Charges Price Difference')
    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)atpm|refund leasing|aktiva', 'Other Income/Charges Others')
    aggregate_columns(opex_transpose, opex_sum_transpose, '(?i)skp|stp', 'Other Income/Charge Tax Assets Penalty Taxes')


    opex_sum_transpose['Total Other Income/ Expenses'] = opex_sum_transpose['Interest Expense and Other Financial Charges'] + opex_sum_transpose['Other Income/Charge Tax Assets Penalty Taxes'] + opex_sum_transpose['Other Income/Charges BBN & STNK'] + opex_sum_transpose['Other Income/Charges Price Difference'] + opex_sum_transpose['Other Income/Charges Others'] + opex_sum_transpose['Interest Income/Expense Bank']

    opex_sum_transpose['EBT (Earning Before Tax)'] = opex_sum_transpose['EBIT'] - opex_sum_transpose['Total Other Income/ Expenses']

    opex_sum_transpose['EAT (Earning After Tax)'] = opex_sum_transpose['EBT (Earning Before Tax)']

    opex_sum_output = opex_sum_transpose.transpose()

    output = "opex-rangkuman.xlsx"
    opex_sum_output.to_excel(output)

    return output


def main():
    st.title("Opex Summary Generator")
    st.markdown(
        """
        File needed:
        - Laba Rugi - Konsolidasi
        \n\n
        ***All files are downloadable from Meta!***
        """
    )

    opex_summary_file = st.file_uploader("Choose Opex file", type = ["xlsx"])

    if opex_summary_file is not None:
        opex = opex_summary(opex_summary_file)
        
        st.success("Opex Summary File Generated!")

        with open(opex, "rb") as f:
            file_content = f.read()

        st.download_button("Download Opex Summary Excel File", data = file_content, file_name="opex-summary.xlsx", mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


if __name__ == "__main__":
    main()
