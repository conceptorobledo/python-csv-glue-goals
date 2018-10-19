import pandas as pd
import numpy as np

df_lead = pd.read_csv('goalglue-sxkm-leads.csv',delimiter=",")
df_goals = pd.read_csv('goalglue-sxkm-goals.csv',delimiter=",")

df_lead['key'] = df_lead['Day of the month'].map(str) + 'h' + df_lead['Hour'].map(str) + df_lead['Device Category'] + df_lead['Browser'] + df_lead['Operating System'] + 'OS' + df_lead['Operating System Version'].map(str) + 'res' + df_lead['Screen Resolution'] 
df_goals['key'] = df_goals['Day of the month'].map(str) + 'h' + df_goals['Hour'].map(str) + df_goals['Device Category'] + df_goals['Browser'] + df_goals['Operating System'] + 'OS' + df_goals['Operating System Version'].map(str) + 'res' + df_goals['Screen Resolution'] 

df_leadgoal = df_lead.loc[df_lead['key'].isin(df_goals['key'])]

""" print('total goals ' + str(len(df_goals.index)))
print('total leadgoals ' + str(len(df_leadgoal.index)))
print(df_goals.key.nunique())
print(df_leadgoal.key.nunique()) """

df_goalscl = df_goals[['key']].copy()
df_leadgoalcl = df_leadgoal[['Source / Medium','key']].copy()

df_cd = pd.merge(df_leadgoalcl, df_goalscl, how='inner', on = 'key')
print(df_leadgoalcl.groupby('key')['Source / Medium'].head(10))