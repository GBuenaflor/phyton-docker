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
                html.H4("Basic Paper Approval Flows"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Add New BP Approval Flow", id="btnaddnewbpflow", color="primary",
                                   href='/settings/settings_bp_approval_flows_profile?&mode=add'),  # block=True
                    ]),
                    html.Div([

                        dbc.Col([
                            dbc.FormGroup(
                                [
                                    dbc.Label("Search BP Flow", width=3,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Input(
                                            type="text", id="search_bpflow_input", placeholder="Enter search string"
                                        ),

                                    ],
                                        width=9
                                    ),

                                ],
                                row=True
                            ),
                        ]),


                        dbc.Row([
                            dbc.Col([
                                dbc.Button("Show All", color="primary",
                                           className="mr-1", id="bpflows_show_all"),
                            ])
                        ]),

                    ], style = {'display': 'none'}),


                ]),

                html.Hr(),
                html.H4("Existing BP Approval Flows"),

                html.Div([

                ], id="bpflowsdt"),

                # dbc.Col([
                #
                #         html.Div([
                #             dcc.Input(id='schoolsubmitstatus', type='text', value="0")
                #         ], style={'display': 'none'}),
                #         html.Div([
                #             dcc.Input(id='schoolid', type='text', value="0")
                #         ], style={'display': 'none'}),
                #
                #         ], width=2
                #         )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback(
    [
        Output('bpflowsdt', 'children')
    ],
    [
        Input('url', 'pathname'),

    ],
    [
    ],
)
def querymodulesfordtcall(url):


    sqlcommand = """
                SELECT approval_flow_id, approval_flow_name, approval_flow_code
                FROM bp_approval_flows
                WHERE approval_flow_delete_ind = %s
                ORDER BY approval_flow_name ASC
            """
    values = (False,)


    columns = ["approval_flow_id", "approval_flow_name", "approval_flow_code"]

    df = securequerydatafromdatabase(sqlcommand, values, columns)
    df.columns = ["BP Approval Flow ID", "BP Approval Flow Name", "BP Approval Flow Code"]
    columns = [{"name": i, "id": i} for i in df.columns]
    data = df.to_dict("rows")
    linkcolumn = {}
    for index, row in df.iterrows():
        linkcolumn[index] = dcc.Link(
            'Edit', href='/settings/settings_bp_approval_flows_profile?approval_flow_id='+str(row["BP Approval Flow ID"])+'&mode=edit')
    data_dict = df.to_dict()
    dictionarydata = {'Select': linkcolumn}
    data_dict.update(dictionarydata)
    df = pd.DataFrame.from_dict(data_dict)
    df = df[["BP Approval Flow Name", "BP Approval Flow Code", "Select"]]
    # print("HERE3456", df)
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return [table, ]




