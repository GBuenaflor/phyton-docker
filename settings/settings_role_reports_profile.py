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
import urllib.parse as urlparse
from urllib.parse import parse_qs
import logging

app.config.suppress_callback_exceptions = False
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


def hash_string(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()


layout = html.Div([
    commonmodules.get_header(),
    commonmodules.get_menu(),
    commonmodules.get_common_variables(),

    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Add Reports to Role", id="rolereports_process_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),

            dbc.CardBody([

                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("Role:", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Label("<value>", id = 'rolereports_rolelabel',style={"text-align": "left"})
                         ],
                             width=8
                         )],
                        row=True
                    ),

                ]),

                dcc.Link('← Back to Roles', href='/settings/settings_role_reports'),
                html.Br(),
                html.Br(),


                html.H2("Included Reports"),

                html.Div([
                            dash_table.DataTable(
                                id = 'rolereports_includedreports',
                                style_header = {
                                                   # '#a88f75',
                                                   'minwidth': '100%',
                                                   'backgroundColor': 'black', 'color': 'white',
                                                   'whiteSpace': 'normal', 'fontWeight': 'bold', 'fontSize': 14, 'font-family': 'sans-serif'
                                               },
                                style_cell = {'textAlign': 'center',
                                             #            # 'minWidth': '120px', 'width': '100px',
                                             #            'maxWidth': '100px',
                                             'textOverflow': 'ellipsis',
                                             'maxWidth': 0,
                                             'height': 'auto',
                                             'whiteSpace': 'normal',
                                             'fontSize': 13, 'font-family': 'sans-serif', 'textAlign': 'center'},
                                style_table={'width': '80%',
                                             'marginLeft': '10%', 'marginRight': '10%'},
                                row_selectable="multi",
                            )

                ],id="rolereports_includedreportsdt"),

                html.Br(),
                dbc.Button("Remove Reports From Role", id="rolereports_removereport", color="primary"),  # block=True
                html.Br(),
                html.Hr(),
                html.Br(),

                html.H2("Excluded Reports"),
                html.Div([
                    dash_table.DataTable(
                        id='rolereports_excludedreports',
                        style_header={
                            # '#a88f75',
                            'minwidth': '100%',
                            'backgroundColor': 'black', 'color': 'white',
                            'whiteSpace': 'normal', 'fontWeight': 'bold', 'fontSize': 14, 'font-family': 'sans-serif'
                        },
                        style_cell={'textAlign': 'center',
                                    #            # 'minWidth': '120px', 'width': '100px',
                                    #            'maxWidth': '100px',
                                    'textOverflow': 'ellipsis',
                                    'maxWidth': 0,
                                    'height': 'auto',
                                    'whiteSpace': 'normal',
                                    'fontSize': 13, 'font-family': 'sans-serif', 'textAlign': 'center'},
                        style_table={'width': '80%',
                                     'marginLeft': '10%', 'marginRight': '10%'},
                        row_selectable="multi",
                    )

                ], id="rolereports_excludedreportsdt"),

                html.Br(),
                dbc.Button("Add Reports To Role", id="rolereports_addeport", color="primary"),  # block=True
                html.Br(),

            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])

@app.callback(
    [
        Output('rolereports_rolelabel', 'children')
    ],
    [
        Input('url', 'search')
    ]
)

def updaterolelabel(url):
    parsed = urlparse.urlparse(url)
    if parse_qs(parsed.query):
        role_id = parse_qs(parsed.query)['role_id'][0]
        sqlcommand4 = '''
                SELECT role_name
                FROM roles
                WHERE role_id = %s
                AND role_delete_ind = %s
          '''
        values4 = (role_id, False)
        columns4 = ['role_name']

        df4 = securequerydatafromdatabase(sqlcommand4, values4, columns4)

        role = df4['role_name'][0]

        return [role]

    else:
        raise PreventUpdate


@app.callback(
    [
        Output('rolereports_includedreports', 'columns'),
        Output('rolereports_includedreports', 'data'),
        Output('rolereports_excludedreports', 'columns'),
        Output('rolereports_excludedreports', 'data'),
    ],
    [
        Input('url', 'search'),
        Input('rolereports_removereport', 'n_clicks'),
        Input('rolereports_addeport', 'n_clicks')
    ],
    [
        State('current_user_id', 'data'),
        State("rolereports_includedreports", "selected_rows"),
        State('rolereports_includedreports', 'data'),
        State("rolereports_excludedreports", "selected_rows"),
        State('rolereports_excludedreports','data')

    ]
)

def populaterolereports(url, rolereports_removereport, rolereports_addeport, current_user_id,
                        rolereports_includedreportsrows, rolereports_includedreportsdata, rolereports_excludedreportsrows, rolereports_excludedreportsdata):

    ctx = dash.callback_context
    eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    parsed = urlparse.urlparse(url)
    if parse_qs(parsed.query):
        role_id = parse_qs(parsed.query)['role_id'][0]

        if eventid == "rolereports_removereport":
            for i in rolereports_includedreportsrows:
                report_id = rolereports_includedreportsdata[i]["Report ID"]

                sqlupdate = '''
                        UPDATE report_roles
                        SET report_role_delete_ind = %s
                        WHERE role_id = %s
                        AND report_id = %s
    
                '''
                values = (True, role_id, report_id)

                modifydatabase(sqlupdate, values)

        if eventid == "rolereports_addeport":
            for i in rolereports_excludedreportsrows:
                report_id = rolereports_excludedreportsdata[i]["Report ID"]

                sqlupdate = '''
                    INSERT INTO report_roles(
                    role_id, report_id, report_role_inserted_by, report_role_inserted_on, report_role_delete_ind)
                    VALUES (%s, %s, %s, %s, %s)
        
                '''
                values = (role_id, report_id, current_user_id, datetime.now(), False)

                modifydatabase(sqlupdate, values)

        sqlcommand4 = '''
                    SELECT report_id, report_name
                    FROM reports
                    WHERE report_id IN (
                        SELECT report_id
                        FROM report_roles
                        WHERE role_id = %s
                        AND report_role_delete_ind = %s
                    )
                    AND report_delete_ind = %s
                          '''
        values4 = (role_id, False, False)
        columns4 = ['report_id', 'report_name']

        df4 = securequerydatafromdatabase(sqlcommand4, values4, columns4)

        df4.columns = ["Report ID", "Report"]

        # df3roleids = df3[["Role ID"]]
        # df3 = df3[["Role"]]

        tablecols4 = [{"name:": i, "id": i} for i in df4.columns]
        tabledata4 = df4.to_dict('records')

        sqlcommand3 = '''
                    SELECT report_id, report_name
                    FROM reports
                    WHERE report_id NOT IN (
                        SELECT report_id
                        FROM report_roles
                        WHERE role_id = %s
                        AND report_role_delete_ind = %s
                    )
                    AND report_delete_ind = %s
                      '''
        values3 = (role_id, False, False)
        columns3 = ['report_id', 'report_name']

        df3 = securequerydatafromdatabase(sqlcommand3, values3, columns3)

        df3.columns = ["Report ID", "Report"]

        tablecols3 = [{"name:": i, "id": i} for i in df3.columns]
        tabledata3 = df3.to_dict('records')

        return [tablecols4, tabledata4, tablecols3, tabledata3]

    else:
        raise PreventUpdate