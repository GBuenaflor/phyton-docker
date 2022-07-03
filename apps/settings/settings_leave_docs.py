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
    html.H1("Leave Application Required Documents"),
    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Leave Application Required Documents"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    # dbc.Col([
                    #     dbc.Button("Add New BP Type", id="btnaddnewbpdoctype", color="primary", href='/settings/settings_bp_docs_profile?&mode=add'),# block=True
                    # ]),
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Leave Type Name", width=4, style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="sleavedoctypename", placeholder="Enter search string"
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
                html.H4("Select existing Leave Type to attach required documents to it."),
                html.Br(),
                html.Div([

                ], id="editdocleavetype"),

                dbc.Col([

                        # html.Div([
                        #     dcc.Input(id='rolesubmitstatus', type='text', value="0")
                        # ], style={'display':'none'}),
                        # html.Div([
                        #     dcc.Input(id='roleid', type='text', value="0")
                        # ], style={'display':'none'}),

                        ], width=2
                        )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback([Output('editdocleavetype', 'children')
               ],
              [
    Input('sleavedoctypename', 'value'),

],
    [
],)
def querymodulesfordtcall(sleavetypename):

    if sleavetypename:
        sleavetypename = '%'+str(sleavetypename)+'%'
        sqlcommand = '''SELECT leave_type_id, leave_type_name FROM leave_types WHERE leave_type_delete_ind = %s
            AND leave_type_name ILIKE %s

            ORDER BY leave_type_name'''
        values = (False, sleavetypename,)
    else:
        sqlcommand = """SELECT leave_type_id, leave_type_name
                          FROM leave_types
                         WHERE leave_type_delete_ind = %s

                           AND leave_type_id != %s AND leave_type_id != %s
                         ORDER BY leave_type_name"""
        values = (False, 19, 20,)
    columns = ["leave_type_id", "leave_type_name"]
    df = securequerydatafromdatabase(sqlcommand, values, columns)
    df.columns = ["Leave Type ID", "Leave Type Name"]
    columns = [{"name": i, "id": i} for i in df.columns]
    data = df.to_dict("rows")
    linkcolumn = {}
    for index, row in df.iterrows():
        linkcolumn[index] = dcc.Link(
            'Select', href='/settings/settings_leave_docs_profile?leave_type_id='+str(row["Leave Type ID"])+'&mode=edit')

    data_dict = df.to_dict()
    dictionarydata = {'Select': linkcolumn}
    data_dict.update(dictionarydata)
    df = pd.DataFrame.from_dict(data_dict)
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return [table]
