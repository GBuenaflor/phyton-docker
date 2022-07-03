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
    html.H1("Leave Approval Statuses and Link to Roles Settings"),
    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Leave Approval Statuses"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Add New Leave Approval Status", id="leave_approval_status_addnewbtn", color="primary",
                                   href='/settings/settings_leave_approval_statuses_profile?&mode=add'),  # block=True
                    ], width=5),
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Search Leave Approval Status", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="leave_approval_status_searchinput", placeholder="Enter search string"
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
                            dbc.Button("", color="primary",
                                       className="mr-1", id="leave_approval_status_searchbtn"),
                        ])
                    ]),

                ]),
                html.Hr(),
                html.H4("Existing Leave Approval Statuses"),

                html.Div([

                ], id="leave_approval_status_dt"),

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


@app.callback([Output('leave_approval_status_dt', 'children')
               ],
              [
    Input('leave_approval_status_searchinput', 'value'),
    Input('leave_approval_status_searchbtn', 'n_clicks'),
    Input('url', 'pathname')
],
    [
],)
def leavestatus_querymodulesfordtcall(leave_approval_status_searchinput, leave_approval_status_searchbtn, url):

    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'leave_approval_status_searchbtn':

            sqlcommand = '''
                        SELECT leave_status_id, leave_status_name
                          FROM leave_statuses ls
                         WHERE leave_status_delete_ind = %s
                         '''
            values = [False]

            if leave_approval_status_searchinput:
                sqlcommand = sqlcommand + " AND leave_status_name ILIKE %s  "
                values.append('%' + leave_approval_status_searchinput + '%')

            sqlcommand = sqlcommand + " ORDER BY leave_status_name"


            columns = ["leave_status_id", "leave_status_name"]
            df = securequerydatafromdatabase(sqlcommand, values, columns)
            df.columns = ["Leave Approval Status ID", "Leave Approval Status"]
            columns = [{"name": i, "id": i} for i in df.columns]
            data = df.to_dict("rows")
            linkcolumn = {}
            for index, row in df.iterrows():
                linkcolumn[index] = dcc.Link(
                    'Edit', href='/settings/settings_leave_approval_statuses_profile?leave_status_id='+str(row["Leave Approval Status ID"])+'&mode=edit')

            data_dict = df.to_dict()
            dictionarydata = {'Select': linkcolumn}
            data_dict.update(dictionarydata)
            df = pd.DataFrame.from_dict(data_dict)
            df = df[["Leave Approval Status", "Select"]]
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
            return [table]

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback(
[
    Output('leave_approval_status_searchbtn', 'children')
],
[
    Input('leave_approval_status_searchinput', 'value'),
    Input('url', 'pathname'),
],
[
],
)
def leavestatus_changesearchbuttonlabel(leave_approval_status_searchinput, url):
    if url == '/settings/settings_leave_approval_statuses':

        if leave_approval_status_searchinput:

            return ['Search']
        else:

            return ['Show All']
        # else:
        #     raise PreventUpdate
    else:

        raise PreventUpdate
