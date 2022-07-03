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
                html.H4("Clearance Statuses"),
                style={"background-color": "rgb(123,20,24)", 'color':'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Add New Status", id="btnaddnewclearance", color="primary", href='/settings/settings_clearance_stats_profile?&mode=add'),# block=True
                    ]),
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Search Status Name", width=4, style={"text-align":"left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="scstatusname", placeholder="Enter search string"
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
                html.H4("Existing Roles"),

                html.Div([

                ],id="cstatusdatatable"),

                dbc.Col([

                        html.Div([
                            dcc.Input(id='cstatusubmitstatus', type='text', value="0")
                        ], style={'display':'none'}),
                        html.Div([
                            dcc.Input(id='cstatusid', type='text', value="0")
                        ], style={'display':'none'}),

                    ], width=2
                )
            ], style = {'line-height':"1em", "display":"block"}),
        ], style = {'line-height':"1em", "display":"block"}
        )
     ]),
])

@app.callback([ Output('cstatusdatatable','children')
                ],
                [
                Input('scstatusname','value'),
                Input('cstatusubmitstatus', 'value'),
                ],
              [
              ],)
def querymodulesfordtcall(scstatusname,cstatusubmitstatus):
    if scstatusname:
        sqlcommand = "SELECT clearance_office_status_id, clearance_office_status_name FROM clearance_office_statuses WHERE clearance_office_status_delete_ind = %s and clearance_office_status_name ILIKE %s ORDER By clearance_office_status_name"
        values = (False, scstatusname)
    else:
        sqlcommand = "SELECT clearance_office_status_id, clearance_office_status_name FROM clearance_office_statuses WHERE clearance_office_status_delete_ind = %s ORDER By clearance_office_status_name"
        values = (False,)
    columns = ["clearance_office_status_id", "clearance_office_status_name"]
    df = securequerydatafromdatabase(sqlcommand, values,columns)
    df.columns=["Status ID","Status Name"]
    columns = [{"name":i, "id":i} for i in df.columns]
    data = df.to_dict("rows")
    linkcolumn = {}
    for index, row in df.iterrows():
        linkcolumn[index]=dcc.Link('Edit', href='/settings/settings_clearance_stats_profile?status_id='+str(row["Status ID"])+'&mode=edit')

    data_dict = df.to_dict()
    dictionarydata = {'Select':linkcolumn}
    data_dict.update(dictionarydata)
    df =pd.DataFrame.from_dict(data_dict)
    df = df[["Status Name", "Select"]]
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return [table]
