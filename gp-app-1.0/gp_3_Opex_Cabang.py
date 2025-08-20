import streamlit as st
import pandas as pd

# st.set_page_config(page_title="Opex Cabang")
# st.sidebar.header("Opex Cabang Generator")

def opex_cabang(opex_file):
    file_name = opex_file
    cabang = ['CBR', 'CKP', 'FTM', 'DM', 'KBJ', 'TAJUR', 'KPG', 'GRESIK', 'MJKT', 'MDN', 'SBY', 'HO', 'SERPONG']
    output_file = "opex_cabang.xlsx"

    # Read each sheet into a dictionary.
    # (Note: Use sheet_name=sheet, not "cabang=sheet".)
    dfs = {}
    for sheet in cabang:
        opex = pd.read_excel(file_name, header=6, sheet_name=sheet)
        opex.reset_index(drop=True, inplace=True)
        opex.rename(columns={"Unnamed: 0": "Bulan"}, inplace=True)
        # Drop rows only if every column is NaN
        opex = opex.dropna(how='all')
        dfs[sheet] = opex

    # Define an aggregation function that creates a new column by summing columns
    # whose names match a given regex pattern.
    def aggregate_columns(df, keyword, new_col_name):
        """
        Aggregates columns that match the regex keyword by summing them row-wise,
        and creates a new column with name new_col_name.
        """
        df[new_col_name] = df.filter(regex=keyword).sum(axis=1)

    # Process each cabang individually and store the aggregated summary in a dictionary.
    aggregated_dict = {}

    for cab in cabang:
        # Get the raw DataFrame for this cabang
        df = dfs[cab].copy()
        
        # Transpose and reassign the first row as column headers
        df_trans = df.transpose()
        df_trans.columns = df_trans.iloc[0]
        df_trans = df_trans[1:]
        
        # --- Perform aggregation ---
        # (You can include as many aggregate_columns calls as needed.)
        aggregate_columns(df_trans, '(?i)gaji', 'BY GAJI')
        aggregate_columns(df_trans, '(?i)tunjangan hari raya', 'BY THR')
        aggregate_columns(df_trans, '(?i)tk', 'BY BPJS TENAGA KERJA')
        aggregate_columns(df_trans, '(?i)kesehatan', 'BY BPJS KESEHATAN')
        aggregate_columns(df_trans, '(?i)amortisasi', 'BY AMORTISASI PRA OPERASI')
        aggregate_columns(df_trans, '(?i)lembur', 'BY LEMBUR')
        aggregate_columns(df_trans, '(?i)promosi|pameran|iklan|brosur|spanduk|showroom event', 'BY MARKETING')
        aggregate_columns(df_trans, '(?i)keamanan', 'BY SECURITY')
        aggregate_columns(df_trans, '(?i)kebersihan', 'BY CLEANING SERVICE')
        aggregate_columns(df_trans, '(?i)bbm|transport', 'BY DO KIRIM UNIT')
        aggregate_columns(df_trans, '(?i)dinas', 'BY PERJALANAN DINAS')
        aggregate_columns(df_trans, '(?i)fotocopy', 'BY FOTOCOPY')
        aggregate_columns(df_trans, '(?i)seragam', 'BY SERAGAM & SEPATU')
        aggregate_columns(df_trans, '(?i)perlengkapan kantor', 'BY ATK')
        aggregate_columns(df_trans, '(?i)cafetaria', 'BY CAFETARIA')
        aggregate_columns(df_trans, '(?i)rapat', 'BY MEETING')
        aggregate_columns(df_trans, '(?i)training', 'BY TRAINING / SPD')
        aggregate_columns(df_trans, '(?i)pemeliharaan kendaraan|perbaikan kendaraan', 'BY REPAIR UNIT')
        aggregate_columns(df_trans, '(?i)stnk', 'BY STNK')
        aggregate_columns(df_trans, '(?i)perbaikan gedung|perbaikan perlengkapan|perbaikan gudang', 'BY PERBAIKAN GEDUNG')
        aggregate_columns(df_trans, '(?i)perbaikan peralatan bengkel|perbaikan bengkel', 'BY PERBAIKAN BENGKEL')
        aggregate_columns(df_trans, '(?i)psikotest|lowongan', 'BY RECRUITMENT')
        aggregate_columns(df_trans, '(?i)perlengkapan bengkel', 'BY CHEMICAL BENGKEL')
        aggregate_columns(df_trans, '(?i)asuransi', 'BY ASURANSI')
        aggregate_columns(df_trans, '(?i)listrik', 'BY LISTRIK')
        aggregate_columns(df_trans, '(?i)telepon|internet', 'BY TELPON & INTERNET')
        aggregate_columns(df_trans, '(?i)air dan gas', 'BY AIR / PDAM')
        aggregate_columns(df_trans, '(?i)iuran rutin', 'BY IPLK')
        aggregate_columns(df_trans, '(?i)pbb', 'BY PBB')
        aggregate_columns(df_trans, '(?i)perijinan', 'BY PERIZINAN')
        aggregate_columns(df_trans, '(?i)reklame|biaya pajak', 'BY PAJAK + REKLAME')
        aggregate_columns(df_trans, '(?i)materai', 'BY MATERAI')
        aggregate_columns(df_trans, '(?i)website', 'BY IT')
        aggregate_columns(df_trans, '(?i)credit|administrasi|transfer', 'BY ADM BANK')
        aggregate_columns(df_trans, '(?i)kirim dokumen', 'BY KIRIM DOKUMEN')
        aggregate_columns(df_trans, '(?i)konsultan|audit', 'BY TENAGA AHLI')
        aggregate_columns(df_trans, '(?i)rekreasi|duka cita|sumbangan|tunjangan lainnya|pernikahan', 'BY DONASI / SUMBANGAN')
        aggregate_columns(df_trans, '(?i)sewa lain-lain|buka puasa|penjualan lainnya', 'BY LAIN-LAIN')
        aggregate_columns(df_trans, '(?i)representasi|goodwill', 'BY CUSTOMER SERVICE')
        aggregate_columns(df_trans, '(?i)perbaikan alat kantor', 'BY PERBAIKAN / SERVICE AC / ALAT KANTOR')
        aggregate_columns(df_trans, '(?i)insentif reguler', 'BY BY INSENTIF SPV SALES/BM/SM')
        aggregate_columns(df_trans, '(?i)provisi', 'BY PROVISI')
        aggregate_columns(df_trans, '(?i)penyusutan', 'BY PENYUSUTAN')
        # ... (add other aggregation calls as in your original script)
        
        # Convert any aggregated column (if needed) to numeric and then to integer.
        df_trans = df_trans.apply(
            lambda col: pd.to_numeric(col, errors='coerce').fillna(0).astype(int)
            if col.dtype == 'object' else col
        )
        # Optionally, divide numeric columns by 1000 if desired.
        df_trans = df_trans.apply(lambda x: x / 1000 if x.dtype in ['float64', 'int64'] else x)
        
        # Select only the aggregated columns you want in the final summary.
        # Adjust the list below as needed.
        selected_cols = [
            'BY GAJI',
            'BY THR',
            'BY BPJS TENAGA KERJA',
            'BY BPJS KESEHATAN',
            'BY AMORTISASI PRA OPERASI',
            'BY LEMBUR',
            'BY MARKETING',
            'BY SECURITY',
            'BY CLEANING SERVICE',
            'BY DO KIRIM UNIT',
            'BY PERJALANAN DINAS',
            'BY FOTOCOPY',
            'BY SERAGAM & SEPATU',
            'BY ATK', 
            'BY CAFETARIA',
            'BY CUSTOMER SERVICE',
            'BY INSENTIF SPV SALES/BM/SM',
            'BY MEETING',
            'BY TRAINING / SPD',
            'BY PERBAIKAN / SERVICE AC / ALAT KANTOR',
            'BY REPAIR UNIT',
            'BY STNK',
            'BY PERBAIKAN GEDUNG',
            'BY PERBAIKAN BENGKEL',
            'BY RECRUITMENT',
            'BY CHEMICAL BENGKEL',
            'BY ASURANSI',
            'BY LISTRIK',
            'BY TELPON & INTERNET',
            'BY AIR / PDAM',
            'BY IPLK',
            'BY PBB',
            'BY PERIZINAN',
            'BY PAJAK + REKLAME',
            'BY MATERAI',
            'BY IT',
            'BY ADM BANK',
            'BY KIRIM DOKUMEN',
            'BY TENAGA AHLI',
            'BY DONASI / SUMBANGAN',
            'BY LAIN-LAIN',
            'BY PROVISI',
            'BY PENYUSUTAN'
            # ... add other aggregated column names here
        ]
        # Make sure to include only columns that exist in df_trans
        summary_cols = [col for col in selected_cols if col in df_trans.columns]
        opex_summary = df_trans[summary_cols]

        opex_summary = opex_summary.assign(
            **{
                #'BY TUNJ MAKAN': 0,
                'BY TUNJ TEMPAT TINGGAL': 0,
                #'BY INSENTIF SPV SALES/BM/SM': 0,
                'BY INSENTIF AFTER SALES': 0,
                'BY SEWA GEDUNG': 0,
                'BY SEWA KENDARAAN': 0,
                'BY TEST DRIVE': 0,
                'BY BBM INVENTARIS': 0,
                #'BY PENYUSUTAN': 0,
                'BY INTEREST DF': 0,
                #'BY PROVISI': 0,
                'BY INTEREST AGING UNIT': 0,
                'TOTAL BIAYA OPEX': 0
            }
        )

        new_columns_order = ['BY GAJI',
                        'BY TUNJ MAKAN',
                        'BY THR',
                        'BY BPJS TENAGA KERJA',
                        'BY BPJS KESEHATAN',
                        'BY AMORTISASI PRA OPERASI',
                        'BY MARKETING',
                        'BY LEMBUR',
                        'BY SECURITY',
                        'BY CLEANING SERVICE',
                        'BY INSENTIF SPV SALES/BM/SM',
                        'BY INSENTIF AFTER SALES',
                        'BY SEWA GEDUNG',
                        'BY SEWA KENDARAAN',
                        'BY DO KIRIM UNIT',
                        'BY TEST DRIVE',
                        'BY BBM INVENTARIS',
                        'BY PERJALANAN DINAS',
                        'BY FOTOCOPY',
                        'BY SERAGAM & SEPATU',
                        'BY ATK', 
                        'BY CAFETARIA',
                        'BY CUSTOMER SERVICE',
                        'BY MEETING',
                        'BY TRAINING / SPD',
                        'BY PERBAIKAN / SERVICE AC / ALAT KANTOR',
                        'BY REPAIR UNIT',
                        'BY STNK',
                        'BY PERBAIKAN GEDUNG',
                        'BY PERBAIKAN BENGKEL',
                        'BY RECRUITMENT',
                        'BY CHEMICAL BENGKEL',
                        'BY ASURANSI',
                        'BY LISTRIK',
                        'BY TELPON & INTERNET',
                        'BY AIR / PDAM',
                        'BY IPLK',
                        'BY PBB',
                        'BY PERIZINAN',
                        'BY PAJAK + REKLAME',
                        'BY MATERAI',
                        'BY IT',
                        'BY DONASI / SUMBANGAN',
                        'BY ADM BANK',
                        'BY KIRIM DOKUMEN',
                        'BY TENAGA AHLI',
                        'BY LAIN-LAIN',
                        'BY PENYUSUTAN',
                        'BY INTEREST DF',
                        'BY PROVISI',
                        'BY INTEREST AGING UNIT',
                        'TOTAL BIAYA OPEX'
        ]
        
        opex_summary = opex_summary[new_columns_order]
        # Optionally: you can assign additional constant columns (e.g., using showroom_tp/workshop_tp)
        # opex_summary = opex_summary.assign(BY_THR=0, BY_TUNJ_MAKAN=0, ...)
        
        # Store the processed summary in the dictionary for this cabang.
        aggregated_dict[cab] = opex_summary

    # Write each aggregated summary to a separate sheet in one Excel file.
    with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
        for cab, summary_df in aggregated_dict.items():
            # Optionally, transpose the summary if you prefer rows as cost items:
            output_df = summary_df.transpose()
            output_df.to_excel(writer, sheet_name=cab, index=True)
    return output_file

def main():
    st.title("Opex Cabang Generator")
    st.markdown(
        """
        File needed:
        - Laba Rugi - per Cabang (Combine into one file w/ different sheets)
        \n\n
        ***All files are downloadable from Meta!***
        """
    )

    opex_cabang_file = st.file_uploader("Choose Opex file", type = ["xlsx"])

    if opex_cabang_file is not None:
        opex = opex_cabang(opex_cabang_file)
        
        st.success("Opex Summary File Generated!")

        with open(opex, "rb") as f:
            file_content = f.read()

        st.download_button("Download Opex Summary Exccel File", data = file_content, file_name="opex-cabang.xlsx", mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

if __name__ == "__main__":
    main()