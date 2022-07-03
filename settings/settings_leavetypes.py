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
    html.H1("Leave Types"),
    html.Hr(),

    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Leave Types and Particulars"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Add New Leave Type", id="btnaddnewleavetype", color="primary",
                                   href='/settings/settings_leavetypes_profile?&mode=add'),  # block=True
                    ]),
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Search Leave Type", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="sleavetypename", placeholder="Enter search string"
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
                html.H4("Existing leave types and other particulars"),

                html.Div([

                ], id="editleavetypedatatable"),

                dbc.Col([

                        html.Div([
                            dcc.Input(id='leavetypesubmitstatus', type='text', value="0")
                        ], style={'display': 'none'}),
                        html.Div([
                            dcc.Input(id='leavetypeid', type='text', value="0")
                        ], style={'display': 'none'}),

                        ], width=2
                        )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback([Output('editleavetypedatatable', 'children')
               ],
              [
    Input('sleavetypename', 'value'),
    Input('leavetypesubmitstatus', 'value'),
],
    [
],)
def leavetypes_querymodulesfordtcall(sleavetypename, leavetypesubmitstatus):
    if sleavetypename:
        sleavetypename = "%"+sleavetypename+"%"
        sqlcommand = "SELECT leave_type_id, leave_type_name, leave_type_code FROM leave_types WHERE leave_type_delete_ind = %s and leave_type_name ILIKE %s ORDER By leave_type_name"
        values = (False, sleavetypename)
    else:
        sqlcommand = "SELECT leave_type_id, leave_type_name, leave_type_code FROM leave_types WHERE leave_type_delete_ind = %s ORDER By leave_type_name"
        values = (False,)
    columns = ["leave_type_id", "leave_type_name", "leave_type_code"]
    df = securequerydatafromdatabase(sqlcommand, values, columns)
    df.columns = ["Leave Type ID", "Leave Type Name/Particulars", "Code"]
    columns = [{"name": i, "id": i} for i in df.columns]
    data = df.to_dict("rows")
    linkcolumn = {}
    for index, row in df.iterrows():
        linkcolumn[index] = dcc.Link(
            'Edit', href='/settings/settings_leavetypes_profile?leave_type_id='+str(row["Leave Type ID"])+'&mode=edit')

    data_dict = df.to_dict()
    dictionarydata = {'Select': linkcolumn}
    data_dict.update(dictionarydata)
    df = pd.DataFrame.from_dict(data_dict)
    df = df[["Leave Type Name/Particulars", "Code", "Select"]]
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return [table]
