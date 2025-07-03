import streamlit as st
import pandas as pd
import numpy as np
import requests
from io import BytesIO

st.set_page_config(page_title="GP")
st.sidebar.header("GP File Generator")


def process_gp(file1, file2):
    # Initialize an empty list to store DataFrames
    dfs = []

    df1 = pd.read_excel(file1, header = 5)
    df1 = df1.iloc[:-1]
    df2 = pd.read_excel(file2, header = 5)
    df2 = df2.iloc[:-1]
    
    # List of file names in your GitHub repository
    file_urls = {
        "df_prima": "https://raw.githubusercontent.com/Flow1t/gp-app/main/gp-app-1.0/df-2025.xlsx",
        "all_rs": "https://raw.githubusercontent.com/Flow1t/gp-app/main/gp-app-1.0/ALL%20RS.xlsx",
        "pricelist": "https://raw.githubusercontent.com/Flow1t/gp-app/main/gp-app-1.0/Pricelist%20Car.xlsx",
        "jabodetabek": "https://raw.githubusercontent.com/Flow1t/gp-app/refs/heads/main/gp-app-1.0/wilayah.txt",
        "luar_jabodetabek": "https://raw.githubusercontent.com/Flow1t/gp-app/refs/heads/main/gp-app-1.0/luar%20jawa.txt"
    }
    
    # Function to download and read Excel files
    def load_excel_from_github(url, sheet_name=None):
        """Loads an Excel file from a GitHub raw URL and reads the specified sheet."""
        response = requests.get(url)
        
        if response.status_code == 200:
            excel_data = BytesIO(response.content)  # Convert to file-like object
            return pd.read_excel(excel_data, sheet_name=sheet_name, engine="openpyxl")  # Read the requested sheet
        else:
            raise FileNotFoundError(f"Failed to load Excel file from {url}. Status code: {response.status_code}")

    def load_text_from_github(file_name):
        url = file_name
        response = requests.get(url)
    
        if response.status_code == 200:
            return {value.strip() for line in response.text.splitlines() for value in line.split(',')}
        else:
            st.error(f"Failed to load {file_name} from GitHub")
            return set()

    ws = load_excel_from_github(file_urls["df_prima"], sheet_name= "ALL")
    rs = load_excel_from_github(file_urls["all_rs"], sheet_name = 'RS')
    price = load_excel_from_github(file_urls["pricelist"], sheet_name = 'Pricelist')
    valid_valuesA = load_text_from_github(file_urls["jabodetabek"])
    valid_valuesB = load_text_from_github(file_urls["luar_jabodetabek"])
    
    # **Combining Headers**
    #GP Report
    # Assuming the first two rows are part of the header
    header_rows = df1.iloc[:2]  # Adjust the range if more rows are part of the header

    header_rows = header_rows.fillna("")

    # Combine the header rows into a single row
    # For merged cells, NaN values will appear. Fill them forward to complete the headers.
    header_combined = header_rows.fillna(method='ffill', axis=1).agg(' '.join, axis=0)

    # Assign the combined headers to the DataFrame and drop the header rows
    df1.columns = header_combined
    df1 = df1.iloc[2:]  # Drop the first two rows (header rows)

    # Reset the index for cleaner output
    df1.reset_index(drop=True, inplace=True)

    # Trim leading and trailing whitespace from column names
    df1.columns = df1.columns.str.strip()

    #Report Penjualan Unit
    # Assuming the first two rows are part of the header
    header_rows = df2.iloc[:2]  # Adjust the range if more rows are part of the header

    header_rows = header_rows.fillna("")

    # Combine the header rows into a single row
    # For merged cells, NaN values will appear. Fill them forward to complete the headers.
    header_combined = header_rows.fillna(method='ffill', axis=1).agg(' '.join, axis=0)

    # Assign the combined headers to the DataFrame and drop the header rows
    df2.columns = header_combined
    df2 = df2.iloc[2:]  # Drop the first two rows (header rows)

    # Reset the index for cleaner output
    df2.reset_index(drop=True, inplace=True)

    # Trim leading and trailing whitespace from column names
    df2.columns = df2.columns.str.strip()

    # Ensure column selection is correct
    columns_to_convert = df1.columns[15:71]  # Select column names from index 15 to 70

    # Apply pd.to_numeric to the selected columns
    df1[columns_to_convert] = df1[columns_to_convert].apply(pd.to_numeric, errors='coerce')

    # **Aggregating Excel File Into A Report**
    # Combine all columns containing 'ONGKOS' by summing them
    df1['ONGKOS KIRIM'] = df1.filter(like="ONGKOS", axis=1).filter(regex='^(?!.*ONGKOS KIRIM KE KONSUMEN).*$', axis=1).sum(axis=1)
    columns_to_drop = df1.filter(like="ONGKOS").filter(regex='^(?!.*ONGKOS KIRIM KE KONSUMEN).*$', axis=1).columns
    columns_to_drop = [col for col in columns_to_drop if col != 'ONGKOS KIRIM']
    df1.drop(columns=columns_to_drop, inplace=True)

    df1["Special Incentive"] = df1.filter(regex='(?i)special incentive').sum(axis=1)
    df1["SALES PROGRAM"] = df1.filter(regex='(?i)rs subsidi').sum(axis=1)
    df1["FREE INSURANCE"] = df1.filter(regex='(?i)free insurance').sum(axis=1)

    # Combine all columns containing 'SURAT' by summing them (Insentif Surat Jalan)
    df1['SURAT JALAN EV'] = df1.filter(regex='(?i)surat jalan ev|cloud lite').sum(axis=1)
    columns_to_drop = df1.filter(regex='(?i)surat jalan ev 1|cloud lite').columns
    columns_to_drop = [col for col in columns_to_drop if col != 'SURAT JALAN EV']
    df1.drop(columns=columns_to_drop, inplace=True)

    # Combine all columns containing 'SURAT' by summing them (Biaya Surat Jalan)
    df1['SURAT JALAN'] = df1.filter(regex='(?i)surat jalan jabodetabek |surat jalan jawa timur ').sum(axis=1)
    #columns_to_drop = df1.filter(regex='(?i)surat jalan jabodetabek|surat jalan jawa timur').columns
    #columns_to_drop = [col for col in columns_to_drop if col != 'SURAT JALAN']
    #df1.drop(columns=columns_to_drop, inplace=True)



    # Combine all columns containing 'FLEET / NEW YEAR' by summing them
    df1['SUBSIDI FLEET / WULING NEW YEAR'] = df1.filter(regex='(?i)fleet|new year').sum(axis=1)
    columns_to_drop = df1.filter(regex='(?i)fleet|new year').columns
    columns_to_drop = [col for col in columns_to_drop if col != 'SUBSIDI FLEET / WULING NEW YEAR']
    df1.drop(columns=columns_to_drop, inplace=True)

    # Combine all columns containing 'FLUSH' by summing them
    df1['FLUSH OUT'] = df1.filter(regex='(?i)flush').sum(axis=1)
    columns_to_drop = df1.filter(regex='(?i)flush').columns
    columns_to_drop = [col for col in columns_to_drop if col != 'FLUSH OUT']
    df1.drop(columns=columns_to_drop, inplace=True)

    # Combine all columns containing 'LOYAL' by summing them
    df1['LOYAL CUSTOMER'] = df1.filter(regex='(?i)loyal').sum(axis=1)
    columns_to_drop = df1.filter(regex='(?i)loyal').columns
    columns_to_drop = [col for col in columns_to_drop if col != 'LOYAL CUSTOMER']
    df1.drop(columns=columns_to_drop, inplace=True)

    # Combine all columns containing 'GROUP' by summing them
    df1['GROUP CUSTOMER'] = df1.filter(regex='(?i)group customer|ice group').sum(axis=1)
    columns_to_drop = df1.filter(regex='(?i)group customer|ice group').columns
    columns_to_drop = [col for col in columns_to_drop if col != 'GROUP CUSTOMER']
    df1.drop(columns=columns_to_drop, inplace=True)

    # Combine all columns containing 'WS' by summing them
    df1['SUBSIDI WS'] = df1.filter(regex='(?i)ws').sum(axis=1)
    columns_to_drop = df1.filter(regex='(?i)ws').columns
    columns_to_drop = [col for col in columns_to_drop if col != 'SUBSIDI WS']
    df1.drop(columns=columns_to_drop, inplace=True)

    # Combine all columns containing 'long aging' by summing them
    df1['LONG AGING STOCK'] = df1.filter(regex='(?i)long aging').sum(axis=1)
    columns_to_drop = df1.filter(regex='(?i)long aging').columns
    columns_to_drop = [col for col in columns_to_drop if col != 'LONG AGING STOCK']
    df1.drop(columns=columns_to_drop, inplace=True)

    # Combine all columns containing 'maintenance' by summing them
    df1['SUBSIDI FREE SERVICE'] = df1.filter(regex='(?i)maintenance|free service').sum(axis=1)
    columns_to_drop = df1.filter(regex='(?i)maintenance').columns
    columns_to_drop = [col for col in columns_to_drop if col != 'SUBSIDI FREE SERVICE']
    df1.drop(columns=columns_to_drop, inplace=True)

    # Combine all columns containing 'poles|repair' by summing them
    df1['AKSESORIS LAIN-LAIN'] = df1.filter(regex='(?i)poles|repair').sum(axis=1)
    columns_to_drop = df1.filter(regex='(?i)poles|repair').columns
    columns_to_drop = [col for col in columns_to_drop if col != 'AKSESORIS LAIN-LAIN']
    df1.drop(columns=columns_to_drop, inplace=True)

    # Combine all columns containing 'kaca' by summing them
    df1['Kaca Film'] = df1.filter(regex='(?i)kaca').sum(axis=1)
    columns_to_drop = df1.filter(regex='(?i)kaca').columns
    columns_to_drop = [col for col in columns_to_drop if col != 'Kaca Film']
    df1.drop(columns=columns_to_drop, inplace=True)

    # Combine all columns containing 'voucher' by summing them
    df1['VOUCHER GIIAS'] = df1.filter(regex='(?i)shopping voucher').sum(axis=1)
    columns_to_drop = df1.filter(regex='(?i)shopping voucher').columns
    columns_to_drop = [col for col in columns_to_drop if col != 'VOUCHER GIIAS']
    df1.drop(columns=columns_to_drop, inplace=True)

    df1['VOUCHER EV & GIIAS, CASH DISKON/ trade in, EX Factory GAP'] = df1.filter(regex='(?i)electricity voucher|gasoline voucher').sum(axis=1)


    df2.rename(columns={'CHASIS': 'NO CHASIS'}, inplace=True)
    ws.rename(columns={'VIN Number': 'NO CHASIS'}, inplace=True)
    rs.rename(columns={'VIN': 'NO CHASIS'}, inplace=True)

    combined_df = pd.merge(df1, df2, on='NO CHASIS')
    combined_df = pd.merge(combined_df, ws, on = 'NO CHASIS', how = 'outer')
    combined_df = pd.merge(combined_df, rs, on = 'NO CHASIS', how = 'outer')

    GP_df = combined_df[['NO_x', 'NAMA CABANG_x', 'GROUP KENDARAAN_x', 'Date', 'CUSTOMER_x', 'KOTA_x', 'TYPE_x', 'NO CHASIS', 'YEAR', 'Report Date', 'PRICE LIST', 'SALES PROGRAM', 'SUBSIDI PPN_x', 'SUBSIDI FREE SERVICE', 'SUBSIDI FLEET / WULING NEW YEAR', 'LONG AGING STOCK', 'Special Incentive', 'GROUP CUSTOMER', 'LOYAL CUSTOMER', 'FREE INSURANCE', 'FLUSH OUT', 'SUBSIDI WS', 'DISCOUNT TOTAL', 'INSENTIF', 'PDI', 'ONGKOS KIRIM', 'SURAT JALAN', 'FEE MEDIATOR','AKSESORIS LAIN-LAIN', 'ONGKOS KIRIM KE KONSUMEN', 'CASH/LEASING', 'TENOR', 'REFUND OFFICE_x', 'Kaca Film', 'VOUCHER GIIAS', 'SURAT JALAN EV', 'VOUCHER GIIAS','VOUCHER EV & GIIAS, CASH DISKON/ trade in, EX Factory GAP']].rename(
        columns={
            'NO_x' : 'No', 
            'NAMA CABANG_x': 'Cabang', 
            'GROUP KENDARAAN_x': 'Type Mobil', 
            'Date': 'Tebusan Bulan',
            'Report Date': 'Sales Program Bulan',
            'CUSTOMER_x' : 'Nama Customer', 
            'KOTA_x' : 'WILAYAH', 
            'TYPE_x' : 'Merek/Type', 
            'NO CHASIS' : 'No Rangka', 
            'YEAR' : 'Tahun', 
            'PRICE LIST' : 'Harga OTR PPU', 
            #'SALES PROGRAM RS SUBSIDI' : 'SALES PROGRAM', 
            'SUBSIDI PPN_x' : 'SUBSIDI MOBIL LISTRIK', 
            'LONG AGING STOCK' : 'SUBSIDI UNIT AGING > 120 HARI', 
            'SUBSIDI WS' : 'WS SUBSIDI', 
            'DISCOUNT TOTAL' : 'Nilai Diskon', 
            'INSENTIF' : 'Insentif Sales', 
            'ONGKOS KIRIM' : 'BIAYA EKSPEDISI', 
            'SURAT JALAN' : 'SURAT JALAN POLDA/ SPOOT STNK / KIR', 
            'FEE MEDIATOR' : 'MEDIATOR', 
            'ONGKOS KIRIM KE KONSUMEN' : 'BIAYA TAMBAHAN ONGKIR',
            'CASH/LEASING' : 'CASH / KREDIT', 
            'REFUND OFFICE_x' : 'REFUND ASURANSI (PPU)'
        }
    )

    GP_df['Cabang'] = GP_df['Cabang'].str[13:]

    GP_df = GP_df.assign(
        **{
            #'Merk/Type':'',
            'Tebusan Dari':'SGMW',
            #'Harga OTR Awal':0,
            'RS Program Bulan':GP_df['Sales Program Bulan'],
            # 'Code Unit':'',
            # 'Dealer Margin 9 %':0.0,
            # 'Dealer Margin 7 %':0.0,
            'SELISIH OTR':0,
            #'VOUCHER EV & GIIAS, CASH DISKON/ trade in, EX Factory GAP':0,
            'SUBSIDI EX KTT':0,
            #'VOUCHER GIIAS':0,
            #'SURAT JALAN EV':0,
            'BCA / BNI EXPO':0,
            'TOTAL PROGRAM':0,
            'Coretan Diskon / SUBVENTION':0,
            'Net Diskon':0,
            'Ongkir SGMW TO DM':0,
            #'Kaca Film':0,
            'NOPIL GAGE':0,
            'TALANG AIR':0,
            'KARPET DASAR':0,
            'Tambahan Biaya BBN':0,
            'Total':0,
            'REFUND ASURANSI  (TGL TERIMA)':'',
            'REFUND YANG MASUK REK OFFICE': GP_df['REFUND ASURANSI (PPU)']/1.11,
            'GP 7 %':0,
            'GP 9 %':0,
            'TOTAL PROGRAM':0,
            'PIC':'',
            'Subsidi Discount OTR':'',
            'Interest':'',
            'PIC':'',
            'DO Bulan': ''
        } 
    )
    GP_df = pd.merge(GP_df, price, on = 'Merek/Type')

    columns_to_convert = ['Dealer Margin 9 %', 'Dealer Margin 7 %', 'REFUND YANG MASUK REK OFFICE']
    GP_df[columns_to_convert] = GP_df[columns_to_convert].astype(int)
    GP_df['Tahun'] = GP_df['Tahun'].astype(str)

    #Adding calculations
    GP_df['Ongkir SGMW TO DM'] = GP_df['Ongkir SGMW TO DM'].apply(pd.to_numeric)
    GP_df['Ongkir SGMW TO DM'] = 326000

    GP_df['Tebusan Bulan'] = pd.to_datetime(GP_df['Tebusan Bulan'], dayfirst=True).dt.strftime('%b-%y')
    GP_df['Sales Program Bulan'] = pd.to_datetime(GP_df['Sales Program Bulan'], dayfirst=True).dt.strftime('%b-%y')
    GP_df['RS Program Bulan'] = pd.to_datetime(GP_df['RS Program Bulan'], dayfirst=True).dt.strftime('%b-%y')

    mapping1 = {'KUPANG': 12000000,
            'GRESIK': 1950000,
            'MADIUN': 2350000,
            'MOJOKERTO': 2150000,
            'KERTAJAYA': 2000000}

    GP_df['BIAYA EKSPEDISI'] = GP_df['Cabang'].map(mapping1).fillna(GP_df['BIAYA EKSPEDISI']).fillna(0)

    GP_df['Tambahan Biaya BBN'] = GP_df['WILAYAH'].apply(
        lambda x: 2000000 if x in valid_valuesA else (5000000 if x in valid_valuesB else 0)
    )

    GP_df['BIAYA TAMBAHAN ONGKIR'] = np.where(GP_df['BIAYA EKSPEDISI'] != 0, 0, GP_df['BIAYA TAMBAHAN ONGKIR'])

    GP_df['Net Diskon'] = GP_df['Nilai Diskon'] - GP_df['Coretan Diskon / SUBVENTION']

    # If the absolute difference between A and B is ≤ 4,000,000, set A = B
    GP_df['Harga OTR Awal'] = np.where(abs(GP_df['Harga OTR PPU'] - GP_df['Harga OTR Awal']) <= 4000000, GP_df['Harga OTR PPU'], GP_df['Harga OTR Awal'])

    GP_df['SELISIH OTR'] = GP_df['Harga OTR PPU'] - GP_df['Harga OTR Awal']

    GP_df['Total'] = (GP_df['Ongkir SGMW TO DM'] +
                    GP_df['Kaca Film'] +
                    GP_df['NOPIL GAGE'] +
                    GP_df['TALANG AIR'] +
                    GP_df['KARPET DASAR'] +
                    GP_df['Tambahan Biaya BBN'] +
                    GP_df['Insentif Sales'] +
                    GP_df['BIAYA EKSPEDISI'] +
                    GP_df['SURAT JALAN POLDA/ SPOOT STNK / KIR'] +
                    GP_df['MEDIATOR'] +
                    GP_df['BIAYA TAMBAHAN ONGKIR'] +
                    GP_df['PDI'])

    GP_df['TENOR'] = GP_df['TENOR']/12
    GP_df['TENOR'] = GP_df['TENOR'].astype(int)

    GP_df['TOTAL PROGRAM'] = (GP_df['SELISIH OTR']+
                            GP_df['SALES PROGRAM']+
                            GP_df['SUBSIDI MOBIL LISTRIK']+
                            GP_df['SUBSIDI FREE SERVICE']+
                            GP_df['VOUCHER EV & GIIAS, CASH DISKON/ trade in, EX Factory GAP']+
                            GP_df['SUBSIDI FLEET / WULING NEW YEAR']+
                            GP_df['SUBSIDI UNIT AGING > 120 HARI']+
                            GP_df['SUBSIDI EX KTT']+
                            GP_df['Special Incentive']+
                            GP_df['GROUP CUSTOMER']+
                            GP_df['LOYAL CUSTOMER']+
                            GP_df['FREE INSURANCE']+
                            GP_df['FLUSH OUT']+
                            GP_df['SURAT JALAN EV']+
                            GP_df['WS SUBSIDI']+
                            GP_df['VOUCHER GIIAS']+
                            GP_df['BCA / BNI EXPO'])

    GP_df['GP 7 %'] = ((GP_df['Dealer Margin 7 %']+
                    GP_df['TOTAL PROGRAM'])-
                    (GP_df['Net Diskon']+
                    GP_df['Total']))

    GP_df['GP 9 %'] = ((GP_df['Dealer Margin 9 %']+
                    GP_df['TOTAL PROGRAM'])-
                    (GP_df['Net Diskon']+
                    GP_df['Total']))
    
    GP_df['REVENUE'] = (GP_df['Harga OTR PPU']+
                        GP_df['TOTAL PROGRAM']-
                        GP_df['Net Diskon'])

    # Define mapping
    mapping2 = {'FATMAWATI': 'CHANDRA', 
            'CIBUBUR': 'ERWIN S INDRAWAN', 
            'DAANMOGOT': 'SUWANDI',
            'SERPONG RAYA': 'IIN AWAN',
            'CIKUPA': 'MAHAJI',
            'KUPANG': 'MENDY',
            'KEBONJERUK': 'RUBBY LIE',
            'HARMONI': 'RACHELLA SARI CIPTADI',
            'GRESIK': 'ARRYA YUDHIANTO',
            'MADIUN': 'ARMAN BARDI',
            'MOJOKERTO': 'VICTOR YUDHA P',
            'TAJUR': 'ANANG R.',
            'KERTAJAYA': 'IVAN KURNIAWAN'}

    # Fill column1 based on column2 values
    GP_df['PIC'] = GP_df['Cabang'].map(mapping2)


    new_column_order = ['No',
                        'Cabang',
                        'PIC',
                        'Type Mobil',
                        'DO Bulan',
                        'Nama Customer',
                        'WILAYAH',
                        'Merk/Type',
                        'Merek/Type',
                        'No Rangka',
                        'Tahun',
                        'Tebusan Dari',
                        'Tebusan Bulan',
                        'Sales Program Bulan',
                        'RS Program Bulan',
                        'Code Unit',
                        'Harga OTR Awal',
                        'Harga OTR PPU',
                        'Dealer Margin 9 %',
                        'Dealer Margin 7 %',
                        'SELISIH OTR',
                        'SALES PROGRAM',
                        'SUBSIDI MOBIL LISTRIK',
                        'Subsidi Discount OTR',
                        'SUBSIDI FREE SERVICE',
                        'VOUCHER EV & GIIAS, CASH DISKON/ trade in, EX Factory GAP',
                        'SUBSIDI FLEET / WULING NEW YEAR',
                        'SUBSIDI UNIT AGING > 120 HARI',
                        'SUBSIDI EX KTT',
                        'Special Incentive',
                        'GROUP CUSTOMER',
                        'LOYAL CUSTOMER',
                        'FREE INSURANCE',
                        'FLUSH OUT',
                        'VOUCHER GIIAS',
                        'SURAT JALAN EV',
                        'WS SUBSIDI',
                        'BCA / BNI EXPO',
                        'TOTAL PROGRAM',
                        'Nilai Diskon',
                        'Coretan Diskon / SUBVENTION',
                        'Net Diskon',
                        'REVENUE',
                        'Insentif Sales',
                        'Interest',
                        'PDI',
                        'Ongkir SGMW TO DM',
                        'BIAYA EKSPEDISI',
                        'Kaca Film',
                        'NOPIL GAGE',
                        'TALANG AIR',
                        'KARPET DASAR',
                        'SURAT JALAN POLDA/ SPOOT STNK / KIR',
                        'MEDIATOR',
                        'AKSESORIS LAIN-LAIN',
                        'BIAYA TAMBAHAN ONGKIR',
                        'Tambahan Biaya BBN',
                        'Total',
                        'CASH / KREDIT',
                        'TENOR',
                        'GP 7 %',
                        'GP 9 %',
                        'REFUND ASURANSI  (TGL TERIMA)',
                        'REFUND YANG MASUK REK OFFICE',
                        'REFUND ASURANSI (PPU)'
                        ]

    GP_df = GP_df[new_column_order]

    # Format all integer columns with commas
    #GP_df = GP_df.applymap(lambda x: f"{x:,}" if isinstance(x, int) else x)

    GP_df = GP_df.drop_duplicates(subset='No Rangka', keep='first')

    jumlah_do = GP_df.pivot_table(index="Merk/Type", columns="Cabang", aggfunc="size", fill_value=0)
    gp7 = GP_df.pivot_table(index="Merk/Type", columns="Cabang", values="GP 7 %", aggfunc="sum", fill_value=0)
    gp9 = GP_df.pivot_table(index="Merk/Type", columns="Cabang", values="GP 9 %", aggfunc="sum", fill_value=0)
    refund = GP_df.pivot_table(index="Type Mobil", columns="Cabang", values="REFUND YANG MASUK REK OFFICE", aggfunc="sum", fill_value=0)

    gp_kredit = GP_df.copy()
    gp_kredit['CASH / KREDIT'] = np.where(
        gp_kredit['CASH / KREDIT'].str.contains('(?i)cash', na=False), 'CASH', 'KREDIT'
    )

    kredit = gp_kredit.pivot_table(index="CASH / KREDIT", columns="Cabang", aggfunc="size", fill_value=0)

    cabang_order = [
        "CIBUBUR",
        "CIKUPA",
        "DAANMOGOT",
        "SERPONG RAYA",
        "FATMAWATI",
        "KEBONJERUK",
        "HARMONI",
        "TAJUR",
        "KUPANG",
        "GRESIK",
        "MOJOKERTO",
        "MADIUN",
        "KERTAJAYA"
    ]

    merk_order = [
        "CONFERO DB",
        "CONFERO S",
        "FORMO S / BV",
        "FORMO MAX PU",
        "CORTEZ",
        "ALMAZ",
        "AIR EV LITE 300",
        "AIR EV LITE 200",
        "AIR EV LV 1",
        "AIR EV LV 2",
        "ALVEZ",
        "BINGUO LITE",
        "BINGUO LV 1",
        "BINGUO LV 2",
        "CLOUD EV LITE",
        "CLOUD EV"
    ]

    type_order = [
        "FORMO",
        "CONFERO",
        "CORTEZ",
        "ALMAZ",
        "AIR EV",
        "ALVEZ",
        "BINGUO",
        "CLOUD"
    ]

    jumlah_do_ordered = jumlah_do.reindex(columns = cabang_order, fill_value = 0)
    jumlah_do_ordered = jumlah_do_ordered.reindex(merk_order, fill_value=0)

    def addNewColumnsRow(unit):
        var_df = unit.reindex(columns = cabang_order, fill_value = 0)
        var_df = var_df.reindex(merk_order, fill_value=0)
        return var_df

    jumlah_do_ordered = addNewColumnsRow(jumlah_do)
    gp7_ordered = addNewColumnsRow(gp7)
    gp9_ordered = addNewColumnsRow(gp9)
    refund_ordered = refund.reindex(columns=cabang_order, fill_value=0)
    refund_ordered = refund_ordered.reindex(type_order, fill_value=0)
    kredit_ordered = kredit.reindex(columns=cabang_order, fill_value=0)

    output_file = "GP.xlsx"
    with pd.ExcelWriter("GP.xlsx", engine="xlsxwriter") as writer:
        GP_df.to_excel(writer, sheet_name="GP", index=True)
        jumlah_do_ordered.to_excel(writer, sheet_name="Jumlah DO", index=True)
        gp7_ordered.to_excel(writer, sheet_name="GP7", index=True)
        gp9_ordered.to_excel(writer, sheet_name="GP9", index=True)
        refund_ordered.to_excel(writer, sheet_name="Refund", index=True)
        kredit_ordered.to_excel(writer, sheet_name="Kredit", index=True)
    return output_file  # Optionally, return the output file path

def main():
    st.title(" Gross Profit Report Generator")
    st.markdown(
        """
        Files needed for report:
        - Monthly Gross Profit Penjualan
        - Monthly Penjualan Unit
        \n\n
        ***All files are downloadable from Meta!***
        """
    )

    gross_profit_file = st.file_uploader("Choose Gross Profit Penjualan file", type=["xlsx"])
    penjualan_unit_file = st.file_uploader("Choose Report Penjualan Unit file", type=["xlsx"])

    if gross_profit_file is not None and penjualan_unit_file is not None:
        gp = process_gp(gross_profit_file, penjualan_unit_file)

        st.success("GP File generated!")
        
        # Read the generated Excel file in binary mode
        with open(gp, "rb") as f:
            file_content = f.read()
        
        st.download_button("Download GP Report Excel File", data=file_content, file_name="gp.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


if __name__ == "__main__":
    main()
