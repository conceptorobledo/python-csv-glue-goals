import pandas as pd
import numpy as np

## Establecer datasets
df_lead = pd.read_csv('goalglue-sxkm-leads.csv',delimiter=",")
df_goals = pd.read_csv('goalglue-sxkm-goals.csv',delimiter=",")

df_lead['Source / Medium'] = df_lead['Source / Medium'].replace(to_replace='emma.cl.*|Seguros_Sura.*',value='emma / email', regex=True)

## Mapear información y cambiar a str las columnas no númericas.
df_lead['key'] = df_lead['Day of the month'].map(str) + 'h' + df_lead['Hour'].map(str) + df_lead['Device Category'] + df_lead['Browser'] + df_lead['Operating System'] + 'OS' + df_lead['Operating System Version'].map(str) + 'res' + df_lead['Screen Resolution'] 
df_goals['key'] = df_goals['Day of the month'].map(str) + 'h' + df_goals['Hour'].map(str) + df_goals['Device Category'] + df_goals['Browser'] + df_goals['Operating System'] + 'OS' + df_goals['Operating System Version'].map(str) + 'res' + df_goals['Screen Resolution'] 

df_lead['count'] = 1

## Sacar keys que estan en los goals
df_leadgoal = df_lead.loc[df_lead['key'].isin(df_goals['key'])]
df_goalscl = df_goals[['key']].copy()

## agregar rows para poder quedar con la fuente que se repite más por key
df_aggregate_leadgoal = df_leadgoal.groupby(['key','Source / Medium'],as_index=False).agg({'count': 'sum'})
df_leadgoalcl = df_aggregate_leadgoal.sort_values('count', ascending=False).drop_duplicates(['Source / Medium','key']).copy()

## randomizar filas y eliminar duplicados
result = df_leadgoalcl[['Source / Medium','key']].sample(frac = 1).reset_index(drop=True).drop_duplicates('key').copy()

## Totales para comparación
total_goals = df_goals['key'].count()
interpolated_goals = result.groupby('Source / Medium').count().sum().values

print('Total Goals ' + str(total_goals))
print('Interpolated Goals' + str(interpolated_goals))
print('% of goals' + str(interpolated_goals/total_goals))
print(result.groupby('Source / Medium').count())
print(result.head(10))
