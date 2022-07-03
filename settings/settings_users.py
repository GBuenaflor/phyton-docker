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
from dash_extensions import Keyboard

def hash_string(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()


layout = html.Div([
    commonmodules.get_header(),
    commonmodules.get_menu(),
    commonmodules.get_common_variables(),
    html.H1("Users Management"),
    # html.Hr(),
    html.Hr(),
    html.Div([
        dbc.Card([
            Keyboard(id="users_keyboard"),
            dbc.CardHeader(
                html.H4("User Account Registration"),
                #    className = 'text-white bg-primary',
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                       dbc.Button("Add New User", id="btnaddnewuser", color="primary",href='/settings/settings_users_profile?&mode=add'),  # block=True
                    ]),
                ]),
                html.Hr(),
                dbc.Row([
                    dbc.Col([
                        html.H5(
                            "This module is for adding and editing users. Click on Add New User to add a new user or search username to edit user details.", style={'font-style': 'italic'})
                    ])
                ]),
                html.Br(),
                dbc.Row([

                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Search User Name", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="susername", placeholder="Enter search string"
                                    ),
                                    dbc.FormFeedback("Please enter your middle name", valid=False)
                                ],
                                    width=8
                                )
                            ],
                            row=True
                        ),
                    ]),
                ]),

                dbc.Row([

                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Search Last Name", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="users_lastnamefilter", placeholder="Enter search string"
                                    ),
                                    dbc.FormFeedback("Please enter your middle name", valid=False)
                                ],
                                    width=8
                                )
                            ],
                            row=True
                        ),
                    ]),
                ]),

                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Search Unit", width=4, style={"text-align":"left"}),
                                dbc.Col([
                                    # dbc.Input(
                                    #     type="text", id="suserroles_unit", placeholder="Enter search string"
                                    # ),
                                    dcc.Dropdown( id="users_unitfilter"
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
                        dbc.Col([
                            dbc.Button("Search", id = 'users_searchbtn', color = 'primary', block=True),
                        ]),
                        dbc.Col([
                        ]),
                    ]),
                html.Hr(),
                html.H5("Existing Users"),
                html.Div([

                ], id="editusersdatatable"),
                dbc.Col([

                        # html.Div([
                        #     dcc.Input(id='usersubmitstatus', type='text', value="0")
                        # ], style={'display': 'none'}),
                        html.Div([
                            dcc.Input(id='userid', type='text', value="0")
                        ], style={'display': 'none'}),

                        dbc.Modal([
                            dbc.ModalHeader("Add New User:", id="userprocess_editmodalhead"),
                            dbc.ModalBody([
                                dbc.Form([
                                    dbc.FormGroup(
                                        [dbc.Label("Username", width=2, style={"text-align": "left"}),
                                         dbc.Col([
                                             dbc.Input(
                                                 type="text", id="username", placeholder="Enter username"
                                             ),
                                             dbc.FormFeedback(
                                                 "Too short, already taken, or has spaces", valid=False)
                                         ],
                                            width=8
                                        )],
                                        row=True
                                    ),
                                    dbc.FormGroup(
                                        [dbc.Label("Password", width=2, style={"text-align": "left"}),
                                         dbc.Col([
                                             dbc.Input(
                                                 type="password", id="password", placeholder="Enter password"
                                             ),
                                             dbc.FormFeedback(
                                                 "Passwords must be at least 6 characters", valid=False)
                                         ], width=8
                                        )],
                                        row=True
                                    ),
                                    dbc.FormGroup(
                                        [dbc.Label("Confirm Password", width=2, style={"text-align": "left"}),
                                         dbc.Col([
                                             dbc.Input(
                                                 type="password", id="confirm_password", placeholder="Enter password"
                                             ),
                                             dbc.FormFeedback("Passwords must match", valid=False)
                                         ], width=8
                                        )],
                                        row=True
                                    ),
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("Last Name", width=2, style={
                                                      "text-align": "left"}),
                                            dbc.Col([
                                                dbc.Input(
                                                    type="text", id="lname", placeholder="Enter last name"
                                                ),
                                                dbc.FormFeedback(
                                                    "Please enter your last name", valid=False)
                                            ],
                                                width=8
                                            )
                                        ],
                                        row=True
                                    ),
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("First Name", width=2, style={
                                                      "text-align": "left"}),
                                            dbc.Col([
                                                dbc.Input(
                                                    type="text", id="fname", placeholder="Enter first name"
                                                ),
                                                dbc.FormFeedback(
                                                    "Please enter your first name", valid=False)
                                            ],
                                                width=8
                                            )
                                        ],
                                        row=True
                                    ),
                                    dbc.FormGroup(
                                        [
                                            dbc.Label("Middle Name", width=2,
                                                      style={"text-align": "left"}),
                                            dbc.Col([
                                                dbc.Input(
                                                    type="text", id="mname", placeholder="Enter middle name"
                                                ),
                                                dbc.FormFeedback(
                                                    "Please enter your middle name", valid=False)
                                            ],
                                                width=8
                                            )
                                        ],
                                        row=True
                                    ),
                                    html.Div([
                                        dcc.Checklist(
                                            options=[
                                                {'label': 'Mark for Deletion?', 'value': '1'},
                                            ], id='chkusermarkfordeletion', value=[]
                                        ),
                                    ], id='divuserdelete',  style={'text-align': 'middle', 'display': 'inline'}),

                                ])
                            ], id="userprocess_editmodalbody"),

                            dbc.ModalFooter([
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button("Register", id="btnsubmitpatient",
                                                   color="primary", block=True),
                                    ]),
                                    dbc.Col([
                                        dbc.Button("Cancel", id="btncancelsubmitpatient",
                                                   className="ml-auto")
                                    ]),
                                ], style={'width': '100%'}),
                            ]),
                        ],
                            id="userreg_edit_modal",
                            centered=True,
                            backdrop='static',
                            size="lg",
                        ),

                        ], width=2
                        )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback(
    [
        Output('editusersdatatable', 'children')
    ],
    [
        Input('users_searchbtn', 'n_clicks'),
        Input("users_keyboard", "keydown"),


    ],
    [
    State('susername', 'value'),
    State('users_lastnamefilter', 'value'),
    State('users_unitfilter', 'value'),

    ]
)
def query_users_for_dt(users_searchbtn, keydown, susername, users_lastnamefilter, users_unitfilter):

    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'users_searchbtn' or keydown['key'] == 'Enter':

            sqlcommand = '''SELECT us.user_id, us.user_name, UPPER(us.user_first_name), UPPER(us.user_last_name), e.emp_primary_home_unit_id
                  FROM users us
                  LEFT JOIN employees e ON e.person_id = us.person_id
                 WHERE user_delete_ind = %s
                            '''
            values = [False,]

            if susername:
                sqlcommand = sqlcommand + ' AND user_name ILIKE %s'
                values.append('%' + susername +'%')
            if users_lastnamefilter:
                sqlcommand = sqlcommand + ' AND user_last_name ILIKE %s'
                values.append('%' + users_lastnamefilter + '%')
            if users_unitfilter:
                sqlcommand = sqlcommand + ' AND e.emp_primary_home_unit_id = %s'
                values.append(users_unitfilter)

            columns = ['user_id', 'user_name', 'user_first_name', 'user_last_name', 'user_role_unit_id']
            sqlcommand = sqlcommand + 'ORDER BY UPPER(us.user_last_name)'
            df = securequerydatafromdatabase(sqlcommand, values, columns)

            df.columns = ["User ID", "User Name", "First Name", "Last Name", "Unit ID"]

            columns = [{"name": i, "id": i} for i in df.columns]

            data = df.to_dict("rows")
            linkcolumn = {}
            for index, row in df.iterrows():
                linkcolumn[index] = dcc.Link(
                    'Edit', href='/settings/settings_users_profile?uid='+str(row["User ID"])+'&mode=edit')
            data_dict = df.to_dict()
            dictionarydata = {'Select': linkcolumn}
            data_dict.update(dictionarydata)
            df = pd.DataFrame.from_dict(data_dict)
            df = df[["User Name", "First Name", "Last Name", "Select"]]
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
            if df.empty == True:
                table = "No entries found. Please check your search criteria."
            return [table]
        else:
            #sqlcommand = "SELECT user_id, user_name, user_first_name, user_last_name FROM users WHERE user_delete_ind = %s ORDER By user_name"
            #values = (False,)
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('users_unitfilter','options')
    ],
    [
        Input('url', 'pathname'),
    ],
    [
    ],
)
def fill_in_dropdowns_for_users(pathname):
    if pathname == "/settings/settings_users":
        # units = commonmodules.queryfordropdown('''
        #     SELECT unit_name as label, unit_id as value
        #       FROM units
        #      WHERE unit_delete_ind = %s
        #     ORDER BY unit_name
        # ''', (False, ))
        return [commonmodules.queryunits()]
    else:
        raise PreventUpdate
