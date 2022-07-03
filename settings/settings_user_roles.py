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
    html.H1("User Roles Management"),
    html.Hr(),
    html.Div([
        dbc.Card([
            Keyboard(id="user_roles_keyboard"),
            dbc.CardHeader(
                html.H4("User Roles"),
                style={"background-color": "rgb(123,20,24)", 'color':'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H5(
                            "This module is for adding roles to users. You can only add a role after creating a user in the Users Module. Please search and select a user first.", style={'font-style': 'italic'})
                    ])
                ]),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Search User Name", width=4, style={"text-align":"left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="suserroles", placeholder="Enter search string"
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
                        dbc.FormGroup(
                            [
                                dbc.Label("Search Last Name", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="usersprofile_lastnamefilter", placeholder="Enter search string"
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
                                    dcc.Dropdown(children = 'N/A',
                                        id="suserroles_unit"
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
                            dbc.Button("Search", id="btn_search_user_roles",
                                       color="primary", block=True),
                        ]),
                        dbc.Col([
                        ]),
                    ]),
                html.Hr(),
                html.H4("Users"),

                html.Div([

                ],id="edituserrolesdatatablemodule"),

                dbc.Col([


                    ], width=2
                )
            ], style = {'line-height':"1em", "display":"block"}),
        ], style = {'line-height':"1em", "display":"block"}
        )
     ]),
])

@app.callback(
    [
        Output('suserroles_unit','options')
    ],
    [
        Input('url', 'pathname'),
    ],
    [
    ],
)
def fill_in_dropdowns_for_user_roles(pathname):
    if pathname == "/settings/settings_user_roles":
        # units = commonmodules.queryfordropdown('''
        #     SELECT unit_name as label, unit_id as value
        #       FROM units
        #      WHERE unit_delete_ind = %s
        #     ORDER BY unit_name
        # ''', (False, ))
        return [commonmodules.queryunits()]
    else:
        raise PreventUpdate


@app.callback(
[
    Output('edituserrolesdatatablemodule','children')
],
[

    Input('btn_search_user_roles', 'n_clicks'),
    Input("user_roles_keyboard", "keydown"),
],
[
    State('suserroles','value'),
    State('suserroles_unit', 'value'),
    State('usersprofile_lastnamefilter', 'value')
],
)
def query_users_for_dt(btn_search_user_roles, keydown, suserroles, suserroles_unit, usersprofile_lastnamefilter):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == 'btn_search_user_roles' or keydown['key'] == 'Enter':

            sqlcommand = '''SELECT us.user_id, us.user_name, UPPER(us.user_first_name), UPPER(us.user_last_name), emp.emp_primary_home_unit_id
                              FROM users us
                            LEFT JOIN persons per ON per.person_id = us.person_id
            				LEFT JOIN employees emp ON emp.person_id = per.person_id
                             WHERE user_delete_ind = %s
                                        '''
            values = [False,]

            if suserroles:
                sqlcommand = sqlcommand + ' AND user_name ILIKE %s'
                values.append('%' + suserroles + '%')
            if usersprofile_lastnamefilter:
                sqlcommand = sqlcommand + ' AND user_last_name ILIKE %s'
                values.append('%' + usersprofile_lastnamefilter + '%')
            if suserroles_unit:
                sqlcommand = sqlcommand + ' AND emp.emp_primary_home_unit_id = %s'
                values.append(suserroles_unit)

            columns = ['user_id', 'user_name', 'user_first_name', 'user_last_name', 'user_role_unit_id']
            sqlcommand = sqlcommand + 'ORDER BY UPPER(us.user_last_name)'
            df = securequerydatafromdatabase(sqlcommand, values, columns)

            df.columns = ["User ID", "User Name", "First Name", "Last Name", "Unit ID"]

            columns = [{"name": i, "id": i} for i in df.columns]

            data = df.to_dict("rows")
            linkcolumn = {}
            for index, row in df.iterrows():
                linkcolumn[index] = dcc.Link(
                    'Edit', href='/settings/settings_user_roles_profile?user_id=' + str(row["User ID"]) + '&mode=edit')

            data_dict = df.to_dict()
            dictionarydata = {'Select': linkcolumn}
            data_dict.update(dictionarydata)
            df = pd.DataFrame.from_dict(data_dict)
            df = df[["User Name", "First Name", "Last Name", "Select"]]
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
            if df.empty == True:
                table = "No entries found. Please check your search criteria."
            return [table]

        #
        #
        #     if any([suserroles_unit, suserroles,usersprofile_lastnamefilter]):
        #         if not suserroles:
        #             suserroles = ''
        #
        #         if not suserroles_unit:
        #             suserroles_unit = 0
        #
        #         sqldefaultrolecheck = '''SELECT u.user_id, user_name, user_first_name, user_last_name, ur.user_role_unit_id, 'Select' as Select
        #                                   FROM users u
        #                                 INNER JOIN user_roles ur ON ur.user_id = u.user_id
        #                                 INNER JOIN units un ON un.unit_id = ur.user_role_unit_id
        #                                  WHERE user_delete_ind = %s
        #                                    AND (user_name ILIKE %s OR user_first_name ILIKE %s OR user_last_name ILIKE %s)
        #                                    AND user_role_unit_id = %s
        #                                 '''
        #         valuesdefaultrolecheck = [False, "%"+suserroles+"%", "%"+suserroles+"%", "%"+suserroles+"%", suserroles_unit]
        #         columnsdefaultrolecheck = ["user_id", "user_name", "user_first_name", "user_last_name", "user_role_unit_id", "Select"]
        #         dfdefaultrolecheck = securequerydatafromdatabase(sqldefaultrolecheck, valuesdefaultrolecheck,columnsdefaultrolecheck)
        #
        #         try:
        #             dfuserid = dfdefaultrolecheck['user_id'][0]
        #         except:
        #             dfuserid = None
        #
        #
        #         if dfuserid is None:
        #             sqlcommand = '''SELECT DISTINCT ON (u.user_id) u.user_id, user_name, user_first_name, user_last_name, ur.user_role_unit_id, 'Select' as Select
        #                               FROM users u
        #                             LEFT JOIN user_roles ur ON ur.user_id = u.user_id
        #                             LEFT JOIN units un ON un.unit_id = ur.user_role_unit_id
        #                              WHERE user_delete_ind = %s
        #                             '''
        #             values = [False,]
        #             columns = ["user_id", "user_name", "user_first_name", "user_last_name", "user_role_unit_id", "Select"]
        #         else:
        #             sqlcommand = '''SELECT DISTINCT ON (u.user_id) u.user_id, user_name, user_first_name, user_last_name, ur.user_role_unit_id, 'Select' as Select
        #                               FROM users u
        #                             LEFT JOIN user_roles ur ON ur.user_id = u.user_id
        #                             LEFT JOIN units un ON un.unit_id = ur.user_role_unit_id
        #                              WHERE user_delete_ind = %s
        #                                AND ur.user_role_default = %s
        #                                AND ur.user_role_delete_ind = %s
        #                             '''
        #             values = [False, True, False]
        #             columns = ["user_id", "user_name", "user_first_name", "user_last_name", "user_role_unit_id", "Select"]
        #
        #         if suserroles:
        #             sqlcommand = sqlcommand + " AND (user_name ILIKE %s OR user_first_name ILIKE %s OR user_last_name ILIKE %s) "
        #             values.append("%"+suserroles+"%")
        #             values.append("%"+suserroles+"%")
        #             values.append("%"+suserroles+"%")
        #
        #         if suserroles_unit:
        #             sqlcommand = sqlcommand + " AND user_role_unit_id = %s "
        #             values.append(suserroles_unit)
        #
        #         sqlcommand = sqlcommand + " ORDER BY u.user_id, user_name ASC LIMIT 200"
        #
        #
        #         df = securequerydatafromdatabase(sqlcommand, values,columns)
        #         df.columns=["User ID","User Name", "First Name", "Last Name","Unit ID", 'Select']
        #         columns = [{"name":i, "id":i} for i in df.columns]
        #         data = df.to_dict("rows")
        #         linkcolumn = {}
        #
        #         for index, row in df.iterrows():
        #             linkcolumn[index]=dcc.Link('Select', href='/settings/settings_user_roles_profile?user_id='+str(row["User ID"])+'&mode=edit')
        #         data_dict = df.to_dict()
        #         dictionarydata = {'Select':linkcolumn}
        #         data_dict.update(dictionarydata)
        #         df =pd.DataFrame.from_dict(data_dict)
        #         df = df[["User Name", "First Name", "Last Name", "Select"]]
        #         table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
        #         return [table]
        #     else:
        #         raise PreventUpdate
        # elif not keydown:
        #     raise PreventUpdate
        # elif keydown['key'] == 'Enter':
        #     if any([suserroles_unit, suserroles,]):
        #         if not suserroles:
        #             suserroles = ''
        #
        #         if not suserroles_unit:
        #             suserroles_unit = 0
        #
        #         sqldefaultrolecheck = '''SELECT u.user_id, user_name, user_first_name, user_last_name, ur.user_role_unit_id, 'Select' as Select
        #                                   FROM users u
        #                                 INNER JOIN user_roles ur ON ur.user_id = u.user_id
        #                                 INNER JOIN units un ON un.unit_id = ur.user_role_unit_id
        #                                  WHERE user_delete_ind = %s
        #                                    AND (user_name ILIKE %s OR user_first_name ILIKE %s OR user_last_name ILIKE %s)
        #                                    AND user_role_unit_id = %s
        #                                 '''
        #         valuesdefaultrolecheck = [False, "%"+suserroles+"%", "%"+suserroles+"%", "%"+suserroles+"%", suserroles_unit]
        #         columnsdefaultrolecheck = ["user_id", "user_name", "user_first_name", "user_last_name", "user_role_unit_id", "Select"]
        #         dfdefaultrolecheck = securequerydatafromdatabase(sqldefaultrolecheck, valuesdefaultrolecheck,columnsdefaultrolecheck)
        #
        #         try:
        #             dfuserid = dfdefaultrolecheck['user_id'][0]
        #         except:
        #             dfuserid = None
        #
        #
        #         if dfuserid is None:
        #             sqlcommand = '''SELECT DISTINCT ON (u.user_id) u.user_id, user_name, user_first_name, user_last_name, ur.user_role_unit_id, 'Select' as Select
        #                               FROM users u
        #                             LEFT JOIN user_roles ur ON ur.user_id = u.user_id
        #                             LEFT JOIN units un ON un.unit_id = ur.user_role_unit_id
        #                              WHERE user_delete_ind = %s
        #                             '''
        #             values = [False,]
        #             columns = ["user_id", "user_name", "user_first_name", "user_last_name", "user_role_unit_id", "Select"]
        #         else:
        #             sqlcommand = '''SELECT DISTINCT ON (u.user_id) u.user_id, user_name, user_first_name, user_last_name, ur.user_role_unit_id, 'Select' as Select
        #                               FROM users u
        #                             LEFT JOIN user_roles ur ON ur.user_id = u.user_id
        #                             LEFT JOIN units un ON un.unit_id = ur.user_role_unit_id
        #                              WHERE user_delete_ind = %s
        #                                AND ur.user_role_default = %s
        #                                AND ur.user_role_delete_ind = %s
        #                             '''
        #             values = [False, True, False]
        #             columns = ["user_id", "user_name", "user_first_name", "user_last_name", "user_role_unit_id", "Select"]
        #
        #         if suserroles:
        #             sqlcommand = sqlcommand + " AND (user_name ILIKE %s OR user_first_name ILIKE %s OR user_last_name ILIKE %s) "
        #             values.append("%"+suserroles+"%")
        #             values.append("%"+suserroles+"%")
        #             values.append("%"+suserroles+"%")
        #
        #         if suserroles_unit:
        #             sqlcommand = sqlcommand + " AND user_role_unit_id = %s "
        #             values.append(suserroles_unit)
        #
        #         sqlcommand = sqlcommand + " ORDER BY u.user_id, user_name ASC LIMIT 200"
        #
        #
        #         df = securequerydatafromdatabase(sqlcommand, values,columns)
        #         df.columns=["User ID","User Name", "First Name", "Last Name","Unit ID", 'Select']
        #         columns = [{"name":i, "id":i} for i in df.columns]
        #         data = df.to_dict("rows")
        #         linkcolumn = {}
        #
        #         for index, row in df.iterrows():
        #             linkcolumn[index]=dcc.Link('Select', href='/settings/settings_user_roles_profile?user_id='+str(row["User ID"])+'&mode=edit')
        #         data_dict = df.to_dict()
        #         dictionarydata = {'Select':linkcolumn}
        #         data_dict.update(dictionarydata)
        #         df =pd.DataFrame.from_dict(data_dict)
        #         df = df[["User Name", "First Name", "Last Name", "Select"]]
        #         table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
        #         return [table]
        #     else:
        #         raise PreventUpdate

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
