#script function:
    # Copy filenames from an image list Excel file into the metadata Excel file.
    #     Matches are based on photopoint ID and date (first by exact YYYYMMDD, then by YYYYMM if the day is missing/marked as '00').
    #     - handles up to 4 duplicate photos (_seq1 to _seq4) per entry.
    #     - prioritises exact day matches before filling with month-only matches.
#Saves as a new 'output' excel file

import pandas as pd #for excel files
from pathlib import Path
import re

print("")
 
# Define paths for excel doc list of image filenames and for excel doc 
image_list_path = Path(r" ")  #Add in excel file with modified filename list path in " "
main_excel_path = Path(r" ")  #Add in METADATA excel file path in " "
output_excel_path = main_excel_path.with_name(main_excel_path.stem + "_OUTPUT.xlsx")  #Add in output excel file path in " " (creating copy so original is kept unchanged)

# load image filename list
image_df = pd.read_excel(image_list_path, sheet_name="sheet1")
image_filenames = image_df["final names with seqX"].dropna().astype(str) #get column with final modified names

# build lookup dictionary {(photopoint, date): [filenames]}
image_by_key = {}
for name in image_filenames:
    name = name.strip().lower()
    m = re.match(r"(?P<pp>[a-z0-9\-]+)_(?P<date>\d{8})_seq(?P<seq>\d+)", name)
    if m:
        key = (m.group("pp"), m.group("date"))
        image_by_key.setdefault(key, []).append(name)

# load main Excel data
df = pd.read_excel(main_excel_path, sheet_name="Sheet1")
df.columns = df.columns.str.strip()

# format date field to match to excel file dates
def format_date(val):
    if pd.isna(val):
        return ""
    if isinstance(val, pd.Timestamp):
        return val.strftime("%Y%m%d")
    return str(int(val)) if isinstance(val, float) else str(val)

df["date_image file name"] = df["date_image file name"].apply(format_date)

# match files to each row
for idx, row in df.iterrows():
    pp = str(row.get("photopoint", "")).strip().lower()
    date = str(row.get("date_image file name", "")).strip()

    if not pp or not date:
        continue

    key = (pp, date)
    matches = image_by_key.get(key, [])

    if matches:
        for i, filename in enumerate(matches[:4]):  # fill in cells photo1 to photo4
            col = f"photo {i+1}"
            if col in df.columns:
                df.at[idx, col] = filename


# create an index of rows by (photopoint, YYYYMM)
row_lookup = {}
for idx, row in df.iterrows():
    pp = str(row.get("photopoint", "")).strip().lower()
    date = str(row.get("date_image file name", "")).strip()
    ym = date[:6]
    if pp and ym:
        row_lookup.setdefault((pp, ym), []).append((idx, row))
        

# Second pass: Match by photopoint and year-month, ignore specific day
# this second pass for unmatched files with no day specified (filename has '00' where day should be e.g. '19921100'), for these match just the month and year IF the cells are empty (haven't already matched a file with a day date)
for name in image_filenames:
    name = name.strip().lower()
    m = re.match(r"(?P<pp>[a-z0-9\-]+)_(?P<ym>\d{6})\d{2}_seq(?P<seq>\d+)", name)
    if not m:
        continue  # Skip if filename format doesn't match

    pp = m.group("pp")
    ym = m.group("ym")

    possible_rows = row_lookup.get((pp, ym), [])
    for idx, row in possible_rows:
        for i in range(1, 5):
            col = f"photo {i}"
            if col in df.columns and (pd.isna(df.at[idx, col]) or df.at[idx, col] == ""):
                df.at[idx, col] = name
                break  # Fill one photo slot only


# Save updated excel doc
df.to_excel(output_excel_path, index=False)
print(f"Done. Saved to: {output_excel_path}")
