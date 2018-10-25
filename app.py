import pandas as pd
import numpy as np

from private import SPREADSHEET_ID, SHEET_RANGES, SS_TO_WRITE_ID
from connect import gsheet_to_dataframe

##Cargar dataframes de gsheets
df_goals = gsheet_to_dataframe(SPREADSHEET_ID,SHEET_RANGES['goal'])
df_lead = gsheet_to_dataframe(SPREADSHEET_ID,SHEET_RANGES['event'])

##Limpiar columna
df_lead['Source / Medium'] = df_lead['Source / Medium'].replace(to_replace='emma.cl.*|Seguros_Sura.*',value='emma / email', regex=True).replace(to_replace='pagoautomatico.*|web.sura.seguroxkm.*',value='(direct) / (none)', regex=True)

## Generar Keys y cambiar a str las columnas no númericas.
df_lead['key'] = df_lead['Month of Year'].map(str) + 'd' + df_lead['Day of the month'].map(str) + 'h' + df_lead['Hour'].map(str) + df_lead['Device Category'] + df_lead['Browser'] + df_lead['Operating System'] + 'OS'  + 'res' + df_lead['Screen Resolution'] 
df_goals['key'] = df_goals['Month of Year'].map(str) + 'd' + df_lead['Day of the month'].map(str) + 'h' + df_goals['Hour'].map(str) + df_goals['Device Category'] + df_goals['Browser'] + df_goals['Operating System'] + 'OS' + 'res' + df_goals['Screen Resolution'] 

df_lead['Unique Events'] = df_lead['Unique Events'].astype(np.int64)

## Extrae leads con keys que esten en goals
df_leadgoal = df_lead.loc[df_lead['key'].isin(df_goals['key'])]

df_leadgoalcl =  df_leadgoal.sort_values('Unique Events', ascending=False).drop_duplicates(['Source / Medium','key']).copy()

n_goals = df_goals['ga:goal4Completions'].astype(np.int64).sum()
n_leads_with_key = df_leadgoalcl['Unique Events'].astype(np.int64).sum()

print('total goals: ' +  str(n_goals))
print('total leads: ' +  str(n_leads_with_key))
print(n_leads_with_key/n_goals)
print('----------- LEADS -----------')
print(df_leadgoal.groupby('Source / Medium')['Unique Events'].sum().sort_values(ascending=False))
print('----------- GOALS -----------')
print(df_leadgoalcl.groupby('Source / Medium')['key'].count())

# Tomar columnas para escribir
result = df_leadgoal[['Month of Year','Day of the month','Source / Medium','Unique Events']].values.tolist()