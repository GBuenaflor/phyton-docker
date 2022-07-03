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
    html.H1("Module Roles Settings"),
    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Module Roles"),
                style={"background-color": "rgb(123,20,24)", 'color':'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Search Role Name", width=4, style={"text-align":"left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="srolenamemodule", placeholder="Enter search string"
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

                ],id="editrolesdatatablemodule"),

                dbc.Col([


                    ], width=2
                )
            ], style = {'line-height':"1em", "display":"block"}),
        ], style = {'line-height':"1em", "display":"block"}
        )
     ]),
])

@app.callback([ Output('editrolesdatatablemodule','children')
                ],
                [
                Input('srolenamemodule','value'),
                ],
              [
              ],)
def querymodulesfordtcall(srolename):

    sqlcommand = '''SELECT role_id, role_name
                 FROM roles
                 WHERE role_delete_ind = %s'''
    values = [False]

    if srolename:
        sqlcommand = sqlcommand + " AND role_name ILIKE %s"
        values.append('%' + str(srolename) + '%')

    sqlcommand = sqlcommand + " ORDER By role_name "

    columns = ("role_id", "role_name")

    df = securequerydatafromdatabase(sqlcommand, values, columns)
    df.columns=["Role ID","Role Name"]
    columns = [{"name":i, "id":i} for i in df.columns]
    data = df.to_dict("rows")
    linkcolumn = {}
    for index, row in df.iterrows():
        linkcolumn[index]=dcc.Link('Modify Modules', href='/settings/settings_module_roles_profile?role_id='+str(row["Role ID"])+'&mode=edit')

    data_dict = df.to_dict()
    dictionarydata = {'Select':linkcolumn}
    data_dict.update(dictionarydata)
    df =pd.DataFrame.from_dict(data_dict)
    df = df[["Role Name", "Select"]]
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

    return [table]
