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
    html.H1("Leaves Settings"),
    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Leave Types"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Add New Leave Type", id="btnaddnewleave", color="primary",
                                   href='/settings/settings_leaves_profile?&mode=add'),  # block=True
                    ]),
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Search Leave Type", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="sleavename", placeholder="Enter search string"
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
                html.H4("Existing leaves"),

                html.Div([

                ], id="editleavedatatable"),

                dbc.Col([

                        html.Div([
                            dcc.Input(id='leavesubmitstatus', type='text', value="0")
                        ], style={'display': 'none'}),
                        html.Div([
                            dcc.Input(id='leaveid', type='text', value="0")
                        ], style={'display': 'none'}),

                        ], width=2
                        )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback(
    [
        Output('editleavedatatable', 'children')
    ],
    [
        Input('sleavename', 'value'),
        Input('leavesubmitstatus', 'value'),
    ],
    [
    ],
)
def querymodulesfordtcall(sleavename, leavesubmitstatus):
    if sleavename:
        sleavename = "%"+sleavename+"%"
        sqlcommand = """SELECT leave_id, leave_name, leave_code
                          FROM leaves
                         WHERE leave_delete_ind = %s
                           AND leave_name ILIKE %s
                        ORDER BY leave_name"""
        values = (False, sleavename)
    else:
        sqlcommand = """SELECT leave_id, leave_name, leave_code
                          FROM leaves
                         WHERE leave_delete_ind = %s
                        ORDER BY leave_name"""
        values = (False, )
    columns = ["leave_id", "leave_name", "leave_code"]
    df = securequerydatafromdatabase(sqlcommand, values, columns)
    df.columns = ["Leave ID", "Leave Name", "Leave Code"]
    columns = [{"name": i, "id": i} for i in df.columns]
    data = df.to_dict("rows")
    linkcolumn = {}
    for index, row in df.iterrows():
        linkcolumn[index] = dcc.Link(
            'Edit', href='/settings/settings_leaves_profile?leave_id='+str(row["Leave ID"])+'&mode=edit')
    data_dict = df.to_dict()
    dictionarydata = {'Select': linkcolumn}
    data_dict.update(dictionarydata)
    df = pd.DataFrame.from_dict(data_dict)
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return [table]
