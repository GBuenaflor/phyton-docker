import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash
import re
from dash.dependencies import Input, Output, State
from apps import commonmodules
from dash.exceptions import PreventUpdate
from app import app
from apps import home
from apps.dbconnect import securequerydatafromdatabase, modifydatabase, modifydatabasereturnid
import hashlib
from datetime import datetime
import dash_table
import pandas as pd
import numpy as np


def hash_string(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()


layout = html.Div([
    commonmodules.get_header(),
    commonmodules.get_menu(),
    commonmodules.get_common_variables(),
    html.H1("Units Master Data Management"),
    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Units"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Add New Unit", id="btnaddnewunit", color="primary",
                                   href='/settings/settings_units_profile?&mode=add'),  # block=True
                    ]),
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Search Unit", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="sunitname", placeholder="Enter search string"
                                    ),

                                ],
                                    width=8
                                )
                            ],
                            row=True
                        ),
                    ]),

                ]),
                html.Hr(),
                html.H4("Existing Units"),

                html.Div([

                ], id="editunitdatatable"),

                dbc.Col([

                        html.Div([
                            dcc.Input(id='unitsubmitstatus', type='text', value="0")
                        ], style={'display': 'none'}),
                        html.Div([
                            dcc.Input(id='unitid', type='text', value="0")
                        ], style={'display': 'none'}),

                        ], width=2
                        )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback([Output('editunitdatatable', 'children')
               ],
              [
    Input('sunitname', 'value'),
    Input('unitsubmitstatus', 'value'),
],
    [
],)
def query_units_for_dt(sunitname, unitsubmitstatus):
    if sunitname:
        sunitname = "%"+sunitname+"%"
        # sqlcommand = '''SELECT unit_id, unit_name
        #              FROM units
        #              WHERE unit_delete_ind = %s
        #              AND unit_is_active = %s
        #              AND unit_name ILIKE %s ORDER By unit_name'''

        sqlcommand = '''SELECT unit_id, unit_name || ' (' || unit_code || ')' as unit_name
                     FROM units
                     WHERE unit_delete_ind = %s
                     AND (unit_name ILIKE %s OR unit_code ILIKE %s)
                     ORDER BY unit_name'''

        values = (False, sunitname, sunitname)
    else:
        # sqlcommand = '''SELECT unit_id, unit_name
        #                 FROM units WHERE unit_delete_ind = %s
        #                 and unit_is_active = %s
        #                 ORDER By unit_name'''

        sqlcommand = '''SELECT unit_id, unit_name || ' (' || unit_code || ')' as unit_name
                        FROM units
                        WHERE unit_delete_ind = %s
                        ORDER By unit_name'''
        values = (False,)
    columns = ["unit_id", "unit_name"]
    df = securequerydatafromdatabase(sqlcommand, values, columns)
    df.columns = ["Unit ID", "Unit Name"]
    columns = [{"name": i, "id": i} for i in df.columns]
    data = df.to_dict("rows")
    linkcolumn = {}
    for index, row in df.iterrows():
        linkcolumn[index] = dcc.Link(
            'Edit', href='/settings/settings_units_profile?unit_id='+str(row["Unit ID"])+'&mode=edit')

    data_dict = df.to_dict()
    dictionarydata = {'Select': linkcolumn}
    data_dict.update(dictionarydata)
    df = pd.DataFrame.from_dict(data_dict)
    df = df[["Unit Name", "Select"]]
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return [table]
