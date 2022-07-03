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
    html.H1("Roles Management"),
    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Roles"),
                style={"background-color": "rgb(123,20,24)", 'color':'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Add New Role", id="btnaddnewrole", color="primary", href='/settings/settings_roles_profile?&mode=add'),# block=True
                    ]),
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Search Role Name", width=4, style={"text-align":"left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="srolename", placeholder="Enter search string"
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

                ],id="editrolesdatatable"),

                dbc.Col([

                        html.Div([
                            dcc.Input(id='rolesubmitstatus', type='text', value="0")
                        ], style={'display':'none'}),
                        html.Div([
                            dcc.Input(id='roleid', type='text', value="0")
                        ], style={'display':'none'}),

                    ], width=2
                )
            ], style = {'line-height':"1em", "display":"block"}),
        ], style = {'line-height':"1em", "display":"block"}
        )
     ]),
])

@app.callback([ Output('editrolesdatatable','children')
                ],
                [
                Input('srolename','value'),
                Input('rolesubmitstatus', 'value'),
                ],
              [
              ],)
def query_roles_dt(srolename,rolesubmitstatus):
    if srolename:
        srolename = "%"+srolename+"%"
        sqlcommand = "SELECT role_id, role_name FROM roles WHERE role_delete_ind = %s and role_name ILIKE %s ORDER By role_name"
        values = (False, srolename)
    else:
        sqlcommand = "SELECT role_id, role_name FROM roles WHERE role_delete_ind = False ORDER By role_name"
        values = (False,)
    columns = ["role_id", "role_name"]
    df = securequerydatafromdatabase(sqlcommand, values,columns)
    df.columns=["Role ID","Role Name"]
    columns = [{"name":i, "id":i} for i in df.columns]
    data = df.to_dict("rows")
    linkcolumn = {}
    for index, row in df.iterrows():
        linkcolumn[index]=dcc.Link('Edit', href='/settings/settings_roles_profile?role_id='+str(row["Role ID"])+'&mode=edit')

    data_dict = df.to_dict()
    dictionarydata = {'Select':linkcolumn}
    data_dict.update(dictionarydata)
    df =pd.DataFrame.from_dict(data_dict)
    df = df[["Role Name", "Select"]]
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return [table]
