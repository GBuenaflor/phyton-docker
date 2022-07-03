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
    # html.H1("Entitlement Types Master Data Management"),
    # html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Entitlement Types"),
                style={"background-color": "rgb(123,20,24)", 'color':'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Add New Entitlement Type", id="btnaddnewenttype", color="primary", href='/settings/settings_entitlementtype_profile?&mode=add'),# block=True
                    ]),
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Search Entitlement Type", width=4, style={"text-align":"left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="senttypename", placeholder="Enter search string"
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
                html.H4("Existing entitlement type"),

                html.Div([

                ],id="editenttypedatatable"),

                dbc.Col([

                        html.Div([
                            dcc.Input(id='enttypesubmitstatus', type='text', value="0")
                        ], style={'display':'none'}),
                        html.Div([
                            dcc.Input(id='enttypeid', type='text', value="0")
                        ], style={'display':'none'}),

                    ], width=2
                )
            ], style = {'line-height':"1em", "display":"block"}),
        ], style = {'line-height':"1em", "display":"block"}
        )
     ]),
])

@app.callback([ Output('editenttypedatatable','children')
                ],
                [
                Input('senttypename','value'),
                Input('enttypesubmitstatus', 'value'),
                ],
              [
              ],)
def querymodulesfordtcall(senttypename,entsubmitstatus):
    if senttypename:
        sqlcommand = "SELECT entitle_type_id, entitle_type_code, entitle_type_name FROM entitlement_types WHERE entitle_type_delete_ind = %s and entitle_type_name ILIKE %s ORDER By entitle_type_name"
        values = (False, senttypename)
    else:
        sqlcommand = "SELECT entitle_type_id, entitle_type_code, entitle_type_name FROM entitlement_types WHERE entitle_type_delete_ind = %s ORDER By entitle_type_name"
        values = (False,)
    columns = ['entitle_type_id', 'entitle_type_code', 'entitle_type_name']
    df = securequerydatafromdatabase(sqlcommand, values,columns)
    df.columns=["Entitlement Type ID", "Code", "Name"]
    columns = [{"name":i, "id":i} for i in df.columns]
    data = df.to_dict("rows")
    linkcolumn = {}
    for index, row in df.iterrows():
        linkcolumn[index]=dcc.Link('Edit', href='/settings/settings_entitlementtype_profile?entitle_type_id='+str(row["Entitlement Type ID"])+'&mode=edit')

    data_dict = df.to_dict()
    dictionarydata = {'Select':linkcolumn}
    data_dict.update(dictionarydata)
    df =pd.DataFrame.from_dict(data_dict)
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return [table]
