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
                html.H4("Basic Paper Approval Statuses"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Add New BP Approval Status", id="bpstatuses_addnewbtn", color="primary",
                                   href='/settings/settings_bp_approval_statuses_profile?&mode=add'),  # block=True
                    ]),
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Search BP Approval Status", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="bpstatuses_searchinput", placeholder="Enter search string"
                                    ),

                                ],
                                    width=8
                                )
                            ],
                            row=True
                        ),
                    ]),

                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Show All", color="primary",
                                       className="mr-1", id="bpstatuses_showallbtn"),
                        ])
                    ]),

                ]),
                html.Hr(),
                html.H4("Existing BP Approval Statuses"),

                html.Div([

                ], id="bpstatuses_dt"),

                # dbc.Col([
                #
                #         html.Div([
                #             dcc.Input(id='unitsubmitstatus', type='text', value="0")
                #         ], style={'display': 'none'}),
                #         html.Div([
                #             dcc.Input(id='unitid', type='text', value="0")
                #         ], style={'display': 'none'}),
                #
                #         ], width=2
                #         )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback([Output('bpstatuses_dt', 'children')
               ],
              [
    Input('bpstatuses_searchinput', 'value'),
    Input('bpstatuses_showallbtn', 'n_clicks'),
    Input('url', 'pathname')
],
    [
],)
def querymodulesfordtcall(bpstatuses_searchinput, bpstatuses_showallbtn, url):

    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'bpstatuses_showallbtn':

            sqlcommand = '''
                        SELECT bp_status_id, bp_status_name
                        FROM bp_statuses bs
                        WHERE bp_status_delete_ind = %s
                         '''
            values = [False]
            sqlcommand = sqlcommand + " ORDER BY bp_status_name"
            columns = ["bp_status_id", "bp_status_name"]
            df = securequerydatafromdatabase(sqlcommand, values, columns)
            df.columns = ["BP Status ID", "BP Status"]
            columns = [{"name": i, "id": i} for i in df.columns]
            data = df.to_dict("rows")
            linkcolumn = {}
            for index, row in df.iterrows():
                linkcolumn[index] = dcc.Link(
                    'Edit', href='/settings/settings_bp_approval_statuses_profile?bp_status_id='+str(row["BP Status ID"])+'&mode=edit')
            data_dict = df.to_dict()
            dictionarydata = {'Select': linkcolumn}
            data_dict.update(dictionarydata)
            df = pd.DataFrame.from_dict(data_dict)
            df = df[["BP Status", "Select"]]
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
            return [table]

        elif bpstatuses_searchinput:
            bpstatuses_searchinput = '%'+ bpstatuses_searchinput+'%'
            sqlcommand = '''
                        SELECT bp_status_id, bp_status_name
                        FROM bp_statuses bs
                        WHERE bp_status_delete_ind = %s
                        AND bp_status_name ILIKE %s
                        ORDER BY bp_status_name
                         '''

            # sqlcommand = sqlcommand + "  "
            values = [False, bpstatuses_searchinput]
            # values.append('%'+ bpstatuses_searchinput+'%')

            # sqlcommand = sqlcommand + " ORDER BY bp_status_name"


            columns = ["bp_status_id", "bp_status_name"]
            df = securequerydatafromdatabase(sqlcommand, values, columns)
            df.columns = ["BP Status ID", "BP Status"]
            columns = [{"name": i, "id": i} for i in df.columns]
            data = df.to_dict("rows")
            linkcolumn = {}
            for index, row in df.iterrows():
                linkcolumn[index] = dcc.Link(
                    'Edit', href='/settings/settings_bp_approval_statuses_profile?bp_status_id='+str(row["BP Status ID"])+'&mode=edit')

            data_dict = df.to_dict()
            dictionarydata = {'Select': linkcolumn}
            data_dict.update(dictionarydata)
            df = pd.DataFrame.from_dict(data_dict)
            df = df[["BP Status", "Select"]]
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
            return [table]

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
