import pandas as pd
from io import BytesIO
import gc

def opex_cabang_monthly(uploaded_file, header_rows=6):
    """
    Memory-safe combiner:
    - uploaded_file: a file-like object from Streamlit (st.file_uploader)
    - header_rows: number of rows to skip before header (default 6)
    Returns: BytesIO containing the combined Excel workbook (one sheet per month).
    """
    # Read uploaded bytes once and reuse
    file_bytes = BytesIO(uploaded_file.getbuffer())

    # Get sheet names without loading all sheets
    xls = pd.ExcelFile(file_bytes)
    sheet_names = xls.sheet_names
    if not sheet_names:
        raise ValueError("Uploaded file contains no sheets.")

    # Read master sheet (first sheet) with header offset
    master_name = sheet_names[0]
    master_df = pd.read_excel(file_bytes, sheet_name=master_name, header=header_rows)
    # Ensure we can reuse the buffer for subsequent reads
    file_bytes.seek(0)

    # Normalize variable column name: prefer first unnamed column as "Variable"
    master_df.rename(columns={c: c.strip() for c in master_df.columns}, inplace=True)
    if "Unnamed: 0" in master_df.columns:
        master_df.rename(columns={"Unnamed: 0": "Variable"}, inplace=True)
    # If first column still not named Variable, set it from index
    if master_df.columns[0] != "Variable":
        master_df.rename(columns={master_df.columns[0]: "Variable"}, inplace=True)

    # Clean master variable list: drop blank rows and keep order
    master_df["Variable"] = master_df["Variable"].astype(str).str.strip()
    master_df = master_df[master_df["Variable"] != ""].reset_index(drop=True)
    master_vars = master_df["Variable"].drop_duplicates(keep="first").tolist()

    # Container: month -> { branch_name: pd.Series(index=Variable, values=...) }
    month_dict = {}

    # Process sheets one-by-one (memory safe)
    for sheet_name in sheet_names:
        try:
            df = pd.read_excel(file_bytes, sheet_name=sheet_name, header=header_rows)
            file_bytes.seek(0)  # rewind for next read

            # Standardize column names and variable column
            df.rename(columns={c: c.strip() for c in df.columns}, inplace=True)
            if "Unnamed: 0" in df.columns:
                df.rename(columns={"Unnamed: 0": "Variable"}, inplace=True)
            if df.columns[0] != "Variable":
                df.rename(columns={df.columns[0]: "Variable"}, inplace=True)

            # Drop rows that are completely empty
            df = df.dropna(how="all").copy()

            # Clean Variable column
            df["Variable"] = df["Variable"].astype(str).str.strip()
            df = df[df["Variable"] != ""]
            df = df.drop_duplicates(subset="Variable", keep="first").reset_index(drop=True)

            # For each column (month-like columns) except "Variable", add to month_dict
            for col in df.columns:
                if col == "Variable":
                    continue
                month = str(col).strip()
                if month == "" or month.lower().startswith("unnamed"):
                    continue

                # Create a Series indexed by Variable
                ser = df.set_index("Variable")[col].copy()
                # Convert numeric-like values, fill NaN with 0 later
                ser = pd.to_numeric(ser, errors="coerce")

                # Initialize month entry if needed
                if month not in month_dict:
                    month_dict[month] = {}

                # Assign series under this branch (sheet_name)
                month_dict[month][sheet_name] = ser

            # free memory for this sheet
            del df
            gc.collect()

        except Exception as e:
            # Skip problematic sheet but continue processing others
            # (If you want Streamlit messages, raise or return message upstream)
            print(f"Warning: failed to process sheet '{sheet_name}': {e}")
            file_bytes.seek(0)
            continue

    # Build output workbook in-memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        for month, branches in month_dict.items():
            if not branches:
                continue

            # Build DataFrame from dict of Series; union of indices will be used.
            combined = pd.DataFrame(branches)

            # Reindex rows to master's variable order if possible,
            # otherwise keep combined's existing order but place master variables first.
            # Create ordered index: first master_vars that exist in combined, then any others
            existing_master_vars = [v for v in master_vars if v in combined.index]
            other_vars = [v for v in combined.index if v not in existing_master_vars]
            final_index = existing_master_vars + other_vars

            combined = combined.reindex(final_index)

            # Fill missing branch values with 0
            combined = combined.fillna(0)

            # Reset index to have 'Variable' column
            combined = combined.reset_index().rename(columns={"index": "Variable"})

            # Ensure sheet name safe for Excel (no invalid chars, max 31 chars)
            safe_name = "".join("_" if c in r'[]:*?/\'\\' else c for c in month)[:31]

            combined.to_excel(writer, sheet_name=safe_name, index=False)

    # Return BytesIO ready for download
    output.seek(0)
    return output
