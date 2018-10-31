## Hasta 30 de Octubre

import pandas as pd
import numpy as np

from private import SPREADSHEET_ID, SHEET_RANGES, SS_TO_WRITE_ID
from connect import gsheet_to_dataframe, write_gsheet

# Toma data de Gsheets, cruza la información por una key única que se crea y luego guarda los resultados.
# La data resultante representa una parte de la data y no la totalidad de entrada.
# Este script consolida una base para luego proporcionalmente agregar metas.

## Cargar dataframes de gsheets
df_goals = gsheet_to_dataframe(SPREADSHEET_ID,SHEET_RANGES['goal'])
df_lead = gsheet_to_dataframe(SPREADSHEET_ID,SHEET_RANGES['event'])

## Limpiar columna
df_lead['Source / Medium'] = df_lead['Source / Medium'].replace(to_replace='emma.cl.*|Seguros_Sura.*',value='emma / email', regex=True).replace(to_replace='pagoautomatico.*|web.sura.seguroxkm.*',value='(direct) / (none)', regex=True)
df_lead['Unique Events'] = df_lead['Unique Events'].astype(np.int64)
df_lead['Hour'] = df_lead['Hour'].astype(np.int64)

## Generar Keys y cambiar a str las columnas no númericas.
df_lead['key'] = df_lead['Month of Year'].map(str) + 'd' + df_lead['Day of the month'].map(str) + 'h' + df_lead['Hour'].map(str) + df_lead['Device Category'] + df_lead['Browser'] + df_lead['Operating System'] + 'OS'  + 'res' + df_lead['Screen Resolution'] 
df_goals['key'] = df_goals['Month of Year'].map(str) + 'd' + df_lead['Day of the month'].map(str) + 'h' + df_goals['Hour'].map(str) + df_goals['Device Category'] + df_goals['Browser'] + df_goals['Operating System'] + 'OS' + 'res' + df_goals['Screen Resolution'] 

## Limpiar dataset
df_leadcl = df_lead[df_lead['Source / Medium'] != 'intranet.ssura.cl / referral']
df_leadcl = df_leadcl[df_leadcl['Source / Medium'] != 'www-publimetro-cl.cdn.ampproject.org / referral']
## Extrae leads con keys que esten en goals
df_leadgoal = df_leadcl.loc[df_leadcl['key'].isin(df_goals['key'])]
""" print(df_goals.groupby('key')['ga:goal4Completions'].count())
 """
df_leadgoalcl =  df_leadgoal.sort_values('Unique Events', ascending=False).drop_duplicates(['Source / Medium','key']).copy()

n_goals = df_goals['ga:goal4Completions'].astype(np.int64).sum()
n_leads_with_key = df_leadgoalcl['Unique Events'].astype(np.int64).sum()

group_leadgoals = df_leadgoalcl.groupby('Source / Medium')['key'].count().sort_values(ascending=False)
total_leadgoals = group_leadgoals.sum()

print('total goals: ' +  str(n_goals))
print('total leads: ' +  str(n_leads_with_key))
print(n_leads_with_key/n_goals) 
"""
print('----------- LEADS -----------')
print(df_lead.groupby('Source / Medium')['Unique Events'].sum().sort_values(ascending=False))
"""
print('----------- LEAD integrados a GOALS -----------')
print(group_leadgoals) 


## Tomar columnas para escribir
result = df_leadgoal[['Month of Year','Day of the month','Source / Medium','Unique Events']]
result_pcts = df_leadgoalcl.groupby(['Month of Year','Day of the month','Source / Medium'])['Unique Events'].sum().groupby(level=0).apply(lambda x: x/total_leadgoals.sum()).reset_index()

## DF con objetivos cumplidos diarios para ser unidos proporcionalmente con el día / canal
df_goals_daily = df_goals[['Month of Year','Day of the month','ga:goal4Completions']]



sheet_headers = result.columns.values.tolist()
sheet_values = result.values.tolist()
sheet_values.insert(0, sheet_headers)

## Escribe en el Gsheet
## El tamaño del rango debe coincidir (O ser menor) con el número de columnas del dataframe
write_gsheet(SS_TO_WRITE_ID,'Result!A1:E',sheet_values)

print('Google Sheet updated ' + SPREADSHEET_ID)