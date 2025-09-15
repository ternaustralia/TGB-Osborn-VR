#EXCEL LIST
#   -create excel doc with list of all jpeg filenames within a specified source directory, iterating through subfolderse as well

import os
import glob 
import pandas as pd  #for excel doc stuff
from pathlib import Path

print('')
print('')
 
# specify the source directory
source_dir = Path(r" ")  #add in path for source directory ""

# listing directory contents **note not neccessary but can print this as a check
os.listdir(source_dir)
#print(os.listdir(source_dir_all))

#Excel doc listing: find ALL jpg in a folder/subfolder and create list of them into one column
#recursively search folders, using .rglob
# Get base names with extension (if want without, change file.name to file.stem)
jpg_files = [
    file.name
    for file in source_dir.rglob("*.jpg")
    if not file.name.startswith ("._") # skip hidden/system files
]

#save to excel file
output_file = source_dir / "File_Name_List_Output.xlsx"  
df = pd.DataFrame(jpg_files, columns=["File Names"])
df.to_excel(output_file, index=False)

print("Excel file created: ", output_file)

print('done')
