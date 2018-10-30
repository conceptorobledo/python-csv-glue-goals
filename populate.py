import pandas as pd
import numpy as np

from private import SPREADSHEET_ID, SHEET_RANGES, SS_TO_WRITE_ID
from connect import gsheet_to_dataframe, write_gsheet

# Toma data de Gsheets, cruza la información por una key única que se crea y luego guarda los resultados.
# La data resultante representa una parte de la data y no la totalidad de entrada.
# Este script añade data de nuevos días. 

##Cargar dataframes de gsheets
df_goals = gsheet_to_dataframe(SPREADSHEET_ID,SHEET_RANGES['goal'])
df_lead = gsheet_to_dataframe(SPREADSHEET_ID,SHEET_RANGES['event'])

## Pasar a int
df_goals['Day of the month'] = df_goals['Day of the month'].astype(np.int64)
df_lead['Day of the month'] = df_lead['Day of the month'].astype(np.int64)
df_goals['Month of Year'] = df_goals['Month of Year'].astype(np.int64)
df_lead['Month of Year'] = df_lead['Month of Year'].astype(np.int64)

## Elegir fecha de extracción
day = 27
month_of_year = 201810

## Filtro por fecha
lead_range = (df_lead['Day of the month'] == day) & (df_lead['Month of Year'] == month_of_year)
goals_range = (df_goals['Day of the month'] == day) & (df_goals['Month of Year'] == month_of_year)
df_lead = df_lead[lead_range]
df_goals = df_goals[goals_range]

## Generar Keys y cambiar a str las columnas no númericas.
df_lead['key'] = df_lead['Month of Year'].map(str) + 'd' + df_lead['Day of the month'].map(str) + 'h' + df_lead['Hour'].map(str) + df_lead['Device Category'] + df_lead['Browser'] + df_lead['Operating System'] + 'OS'  + 'res' + df_lead['Screen Resolution'] 
df_goals['key'] = df_goals['Month of Year'].map(str) + 'd' + df_lead['Day of the month'].map(str) + 'h' + df_goals['Hour'].map(str) + df_goals['Device Category'] + df_goals['Browser'] + df_goals['Operating System'] + 'OS' + 'res' + df_goals['Screen Resolution'] 

print(df_lead.head(10))