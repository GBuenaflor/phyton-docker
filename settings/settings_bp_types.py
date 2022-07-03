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

    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Service Record Types"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Add New SR Type", id="btnaddnewbptype", color="primary",
                                   href='/settings/settings_bp_types_profile?&mode=add'),  # block=True
                    ]),
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("SR Type Name", width=4, style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="sbptypename", placeholder="Enter search string"
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
                html.H4("Existing SR Types"),

                html.Div([

                ], id="editbptype"),

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


@app.callback([Output('editbptype', 'children')
               ],
              [
    Input('sbptypename', 'value'),

],
    [
],)
def querymodulesfordtcall(sbptypename):

    if sbptypename:
        sbptypename = '%'+str(sbptypename)+'%'
        sqlcommand = "SELECT appt_type_id, appt_type_name FROM appointment_types WHERE appt_type_delete_ind = %s and appt_type_name ILIKE %s ORDER BY appt_type_name"
        values = (False, sbptypename)
    else:
        sqlcommand = """SELECT appt_type_id, appt_type_name,
                                     CASE
									  WHEN appt_type_is_primary = True THEN 'TRUE'
									  WHEN appt_type_is_primary = False THEN 'FALSE'
									  ELSE ''
									 END,
                                     CASE
									  WHEN is_bp_type = True THEN 'TRUE'
									  WHEN is_bp_type = False THEN 'FALSE'
									  ELSE ''
									 END,
									 CASE
									  WHEN is_sep_type = True THEN 'TRUE'
									  WHEN is_sep_type = False THEN 'FALSE'
									  ELSE ''
									 END,
                                     CASE
									  WHEN appt_type_is_gsis = True THEN 'TRUE'
									  WHEN appt_type_is_gsis = False THEN 'FALSE'
									  ELSE ''
									 END
                          FROM appointment_types
                         WHERE appt_type_delete_ind = %s
                        ORDER BY appt_type_name"""
        values = (False,)
    columns = ['appt_type_id', 'appt_type_name', 'appt_type_is_primary',
               'is_bp_type', 'is_sep_type', 'appt_type_is_gsis']
    df = securequerydatafromdatabase(sqlcommand, values, columns)
    df.columns = ["SR Type ID", "SR Name", "Is Primary Appointment?",
                  "Is a BP Type?", "Is a Separation Type?", "Is a GSIS Record?"]
    columns = [{"name": i, "id": i} for i in df.columns]
    data = df.to_dict("rows")
    linkcolumn = {}
    for index, row in df.iterrows():
        linkcolumn[index] = dcc.Link(
            'Edit', href='/settings/settings_bp_types_profile?bp_type_id='+str(row["SR Type ID"])+'&mode=edit')

    data_dict = df.to_dict()
    dictionarydata = {'Select': linkcolumn}
    data_dict.update(dictionarydata)
    df = pd.DataFrame.from_dict(data_dict)
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return [table]
