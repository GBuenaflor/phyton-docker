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
    html.H1("Entitlements and Entitlement Types Master Data Management"),
    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Entitlements and Entitlement Types"),
                style={"background-color": "rgb(123,20,24)", 'color':'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Add New Entitlement", id="btnaddnewent", color="primary", href='/settings/settings_entitlements_profile?&mode=add'),# block=True
                        html.Br(),
                        html.Br(),
                        dbc.Button("Add New Entitlement Type", id="btnaddnewenttype", color="primary", href='/settings/settings_entitlementtype_profile?&mode=add'),# block=True
                    ]),


                ]),
                html.Hr(),

                html.H4("Existing entitlements", id="entitlementstoggle", style = {'cursor':'pointer', 'text-decoration':'underline'}),
                dbc.Collapse([
                    dbc.Row([
                        dbc.Col([
                            dbc.FormGroup(
                                [
                                    dbc.Label("Search Entitlement Name", width=4, style={"text-align":"left"}),
                                    dbc.Col([
                                        dbc.Input(
                                            type="text", id="sentname", placeholder="Enter search string"
                                        ),

                                    ],
                                    width=8
                                    )
                                ],
                                row=True
                            ),
                        ]),
                    ]),
                    dbc.Row([
                        # html.H4("Existing entitlements"),

                        dbc.Col([
                            html.Div([
                            ],id="editentdatatable"),
                        ]),
                    ]),
                ], id="entitlementscollapse"),

                dbc.Col([

                        html.Div([
                            dcc.Input(id='entsubmitstatus', type='text', value="0")
                        ], style={'display':'none'}),
                        html.Div([
                            dcc.Input(id='entid', type='text', value="0")
                        ], style={'display':'none'}),

                    ], width=4
                ),

                html.Hr(),
                html.H4("Existing entitlement types", id="entitlementtypestoggle", style = {'cursor':'pointer', 'text-decoration':'underline'}),
                # html.H4("Existing entitlement types"),
                dbc.Collapse([
                    dbc.Row([
                        # dbc.Col(),
                        dbc.Col([
                            dbc.FormGroup(
                                [
                                    dbc.Label("Search Entitlement Type Name", width=4, style={"text-align":"left"}),
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
                    dbc.Row([
                        # html.H4("Existing entitlements"),

                        dbc.Col([
                            html.Div([

                            ],id="editenttypedatatable"),
                        ]),
                    ]),
                ], id="entitlementtypescollapse"),




                dbc.Col([

                        html.Div([
                            dcc.Input(id='enttypesubmitstatus', type='text', value="0")
                        ], style={'display':'none'}),
                        html.Div([
                            dcc.Input(id='enttypeid', type='text', value="0")
                        ], style={'display':'none'}),

                    ], width=2
                ),
            ], style = {'line-height':"1em", "display":"block"}),
        ], style = {'line-height':"1em", "display":"block"}
        )
     ]),
])

@app.callback([ Output('editentdatatable','children')
                ],
                [
                Input('sentname','value'),
                Input('entsubmitstatus', 'value'),
                ],
              [
              ],)
def querymodulesfordtcall(sentname,entsubmitstatus):
    if sentname:
        sqlcommand = "SELECT entitle_id, entitle_code, entitle_name FROM entitlements WHERE entitle_delete_ind = %s and entitle_name ILIKE %s ORDER By entitle_name"
        values = (False, "%"+sentname+"%")
    else:
        sqlcommand = "SELECT entitle_id, entitle_code, entitle_name FROM entitlements WHERE entitle_delete_ind = %s ORDER By entitle_name"
        values = (False,)
    columns = ['entitle_id', 'entitle_code', 'entitle_name']
    df = securequerydatafromdatabase(sqlcommand, values,columns)
    df.columns=["Entitlement ID", "Code", "Entitlement Name"]
    columns = [{"name":i, "id":i} for i in df.columns]
    data = df.to_dict("rows")
    linkcolumn = {}
    for index, row in df.iterrows():
        linkcolumn[index]=dcc.Link('Edit', href='/settings/settings_entitlements_profile?entitle_id='+str(row["Entitlement ID"])+'&mode=edit')

    data_dict = df.to_dict()
    dictionarydata = {'Select':linkcolumn}
    data_dict.update(dictionarydata)
    df =pd.DataFrame.from_dict(data_dict)
    df = df[["Code", "Entitlement Name", "Select"]]
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return [table]



@app.callback([ Output('editenttypedatatable','children')
                ],
                [
                Input('senttypename','value'),
                Input('enttypesubmitstatus', 'value'),
                ],
              [
              ],)
def querymodulesfordtcall(senttypename,enttypesubmitstatus):
    if senttypename:
        sqlcommand = "SELECT entitle_type_id, entitle_type_code, entitle_type_name FROM entitlement_types WHERE entitle_type_delete_ind = %s and entitle_type_name ILIKE %s ORDER By entitle_type_name"
        values = (False, "%"+senttypename+"%")
    else:
        sqlcommand = "SELECT entitle_type_id, entitle_type_code, entitle_type_name FROM entitlement_types WHERE entitle_type_delete_ind = %s ORDER By entitle_type_name"
        values = (False,)
    columns = ['entitle_type_id', 'entitle_type_code', 'entitle_type_name']
    df = securequerydatafromdatabase(sqlcommand, values,columns)
    df.columns=["Entitlement Type ID", "Code", "Entitlement Type Name"]
    columns = [{"entname":i, "entid":i} for i in df.columns]
    data = df.to_dict("rows")
    linkcolumn2 = {}
    for index, row in df.iterrows():
        linkcolumn2[index]=dcc.Link('Edit', href='/settings/settings_entitlementtype_profile?entitle_type_id='+str(row["Entitlement Type ID"])+'&mode=edit')

    data_dict = df.to_dict()
    dictionarydata = {'Select':linkcolumn2}
    data_dict.update(dictionarydata)
    df =pd.DataFrame.from_dict(data_dict)
    df = df[["Code", "Entitlement Type Name", "Select"]]
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return [table]



@app.callback(
[
    Output("entitlementscollapse", "is_open")
],
[
    Input("entitlementstoggle", "n_clicks")
],
[
    State("entitlementscollapse", "is_open")
],
)
def toggle_collapse(n, is_open):
    if n:
        return [not is_open]
    return [is_open]


@app.callback(
[
    Output("entitlementtypescollapse", "is_open")
],
[
    Input("entitlementtypestoggle", "n_clicks")
],
[
    State("entitlementtypescollapse", "is_open")
],
)
def toggle_collapse(n, is_open):
    if n:
        return [not is_open]
    return [is_open]
