import pandas as pd

from private import SPREADSHEET_ID, SHEET_RANGES
from connect import gsheet_to_dataframe

df_goals = gsheet_to_dataframe(SPREADSHEET_ID,SHEET_RANGES['goal'])
df_lead = gsheet_to_dataframe(SPREADSHEET_ID,SHEET_RANGES['event'])

df_lead['Source / Medium'] = df_lead['Source / Medium'].replace(to_replace='emma.cl.*|Seguros_Sura.*',value='emma / email', regex=True)

print(df_goals.head(10))