from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import pandas as pd

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

# The ID and range of a sample spreadsheet.

def gsheet_to_dataframe( spreadsheet_id, range_name ):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    result = service.spreadsheets().values().get(spreadsheetId= spreadsheet_id,
                                                range=range_name).execute()
    values = result.get('values', [])
    if not values:
        return print('No hay datos')
    else:
        df_goals = pd.DataFrame(values, columns = values[0])
        df_goals = df_goals.drop(df_goals.index[0])
        return df_goals


if __name__ == '__main__':
    gsheet_to_dataframe() 


def write_gsheet(spreadsheet_id, range_name, values):
    body = {
        'values': values
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()
    return print('{0} cells updated.'.format(result.get('updatedCells')));
    