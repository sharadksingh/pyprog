import os
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

# Set the directory where the Excel files are located
#directory = 'C:/path/to/directory/'

#directory = 'C:\Users\Sharad\pyora\CISF_DATA\'
directory = 'C:/Users/Sharad/pyora/CISF_DATA/'

# Create a new workbook to store the merged data
merged_workbook = Workbook()
merged_sheet = merged_workbook.active

# Iterate through all the files in the directory
for file in os.listdir(directory):
    # Skip any non-Excel files
    if not file.endswith('.xls'):
        continue

    # Read the data from the current Excel file
    df = pd.read_excel(directory + file)

    # Append the data from the current file to the merged sheet
    for row in dataframe_to_rows(df, index=False, header=True):
        merged_sheet.append(row)

# Save the merged workbook
merged_workbook.save('merged.xls')
