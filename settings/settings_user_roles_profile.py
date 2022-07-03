import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash
import re
from dash.dependencies import Input, Output, State, MATCH, ALL
import json
from apps import commonmodules
from dash.exceptions import PreventUpdate
from app import app
from apps import home
from apps.dbconnect import securequerydatafromdatabase, modifydatabase, modifydatabasereturnid, singularcommandupdatedatabase
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
        html.H1("Manage User Roles"),
        dcc.Link('← Modify another role', href='/settings/settings_user_roles'),
        dbc.Card([
            dbc.CardHeader(
                html.H4("Selected User", id="user_role_process_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),

            dbc.Modal([
                dbc.ModalHeader("Process User Roles", id="user_roles_results_head"),
                dbc.ModalBody([
                ], id="user_roles_results_body"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Close", id="btn_user_role_head_close",
                                       color="primary", block=True),
                        ], id="user_roles_results_head_close", style={'display': 'none'}),
                        dbc.Col([
                            dbc.Button("Return", id="btn_user_role_results_head_return",
                                       color="primary", block=True, href='/settings/settings_user_roles'),
                        ], id="user_roles_results_head_return", style={'display': 'none'}),
                    ], style={'width': '100%'}),
                ]),
            ], id="user_roles_results_modal"),
            dbc.CardBody([
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("User Name:", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             html.H1("Role Name", style={ #width=2,
                                       "text-align": "left"}, id="module_user_role_user_name"),
                         ],
                            width=8
                        )],
                        row=True
                    ),
                ]),
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("Employee Number:", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Label("N/A", style={ #width=2,
                                       "text-align": "left"}, id="module_user_role_emp_number"),
                         ],
                            width=8
                        )],
                        row=True
                    ),
                ]),
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("First Name:", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Label("N/A", style={ #width=2,
                                       "text-align": "left"}, id="module_user_role_first_name"),
                         ],
                            width=8
                        )],
                        row=True
                    ),
                ]),
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("Middle Name:", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Label("N/A", style={ #width=2,
                                       "text-align": "left"}, id="module_user_role_middle_name"),
                         ],
                            width=8
                        )],
                        row=True
                    ),
                ]),
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("Last Name:", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Label("N/A", style={ #width=2,
                                       "text-align": "left"}, id="module_user_role_last_name"),
                         ],
                            width=8
                        )],
                        row=True
                    ),
                ]),
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("Extension Name:", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Label("N/A", style={ #width=2,
                                       "text-align": "left"}, id="module_user_role_extension_name"),
                         ],
                            width=8
                        )],
                        row=True
                    ),
                ]),
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("Default Unit:", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Label("N/A", style={ #width=2,
                                       "text-align": "left"}, id="module_user_role_default_unit"),
                         ],
                            width=8
                        )],
                        row=True
                    ),
                ]),
                # dbc.Form([
                #     dbc.FormGroup(
                #         [dbc.Label("Access Level Unit of Default Role:", width=2, style={"text-align": "left"}),
                #          dbc.Col([
                #              dbc.Label("N/A", style={ #width=2,
                #                        "text-align": "left"}, id="module_user_role_access_level_unit"),
                #          ],
                #             width=8
                #         )],
                #         row=True
                #     ),
                # ]),
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("Default Role:", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Label("N/A", style={ #width=2,
                                       "text-align": "left"}, id="module_user_role_role_name"),
                         ],
                            width=8
                        )],
                        row=True
                    ),
                ]),
                dbc.Card([
                    dbc.CardHeader(
                        html.H5("Select Options"),
                        style={"background-color": "rgb(123,20,24)", 'color': 'white'}
                    ),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dcc.Markdown('''__NOTE: Please ensure that at all times there is only 1 default role for this user.__''',
                                             style={'font-style': 'italic', 'font-size':'24px'})
                            ])
                        ]),
                        html.Hr(),
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Select Role to Add", style={"text-align": "left"}),
                            ]),
                            dbc.Col([
                                dcc.Dropdown(
                                    id='ddlistofusermodules',
                                    options=[
                                    ],
                                    searchable=True,
                                    clearable=True
                                ),
                            ]),
                        ], style={'width': '100%'}),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Default Unit", style={"text-align": "left"}),
                            ]),
                            dbc.Col([
                                dcc.Dropdown(
                                    id='ddlistofunitsforroles',
                                    options=[
                                    ],
                                    searchable=True,
                                    clearable=True
                                ),
                            ]),
                        ], style={'width': '100%'}),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Access Level Unit", style={"text-align": "left"}),

                            ]),
                            dbc.Col([
                                dcc.Dropdown(
                                    id='ddlistofaccesslevelunitsforroles',
                                    options=[
                                    ],
                                    searchable=True,
                                    clearable=True
                                ),
                                dbc.FormText(
                                    "Defines the access level of the role.", color="secondary"
                                ),
                            ]),
                        ], style={'width': '100%'}),
                        html.Br(),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Default Setting", style={"text-align": "left"}),
                            ]),
                            dbc.Col([
                                dcc.Checklist(
                                    options=[
                                        {'label': ' Set Role as Default?', 'value': '1'},
                                    ], id='chksetasdefault', value=[]
                                ),
                            ]),
                        ], style={'width': '100%'}),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                dbc.Button("Add Role", id="user_role_submit", color="primary"),
                            ]),
                        ], style={'width': '100%'}),
                        dbc.Row([

                        ], style={'width': '100%'}),
                        dbc.Row([
                            # dbc.Col([
                            # ]),
                            dbc.Col([
                                #dbc.Button("Cancel", id="module_role_cancel", color="warning", className="ml-auto")
                            ]),
                        ], style={'width': '100%'}),
                    ], style={'line-height': "1em", "display": "block"}),
                ]),
                html.Hr(),

                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.H4("Current Active Roles"),
                            html.H6("*The default role cannot be set to inactive"),
                            html.H6("*A role should be set to inactive if it is beyond the appointment date (e.g. OIC)"),
                            html.H6("*A role should be deleted if there is a error in the role (e.g. incorrect role assignment)"),
                            html.Div([
                                html.Div([

                                ], id="existinguserrolesdatatableprofile"),
                            ], style={'width': '100%', 'padding': '10px'}),
                        ]),
                    ], style={'width': '100%'}),
                ]),

                html.Div([
                    html.Br(),
                    html.Hr(),
                    dbc.Row([
                        dbc.Col([
                            html.H4("Current Inactive Roles"),

                            html.Div([
                                html.Div([

                                ], id="existinguserrolesdatatableprofile_inactive"),
                            ], style={'width': '100%', 'padding': '10px'}),
                        ]),
                    ], style={'width': '100%'}),
                ]),

            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback(
    [
        Output('module_user_role_user_name', 'children'),
        Output('module_user_role_first_name', 'children'),
        Output('module_user_role_middle_name', 'children'),
        Output('module_user_role_last_name', 'children'),
        Output('module_user_role_extension_name', 'children'),
        Output('module_user_role_default_unit', 'children'),
        # Output('module_user_role_access_level_unit', 'children'),
        Output('module_user_role_emp_number', 'children'),
        Output('module_user_role_role_name', 'children')
    ],
    [
        Input('url', 'search'),
    ],
    [
    ],
)
def clear_user_roles_data(url,):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":
            user_id = parse_qs(parsed.query)['user_id'][0]
            # try:
            #     user_id = parse_qs(parsed.query)['user_id'][0]
            # except:
            #     user_id = '0'
            sqluser = '''SELECT us.user_name, user_first_name, user_last_name, user_middle_name, user_name_extension, emp.emp_number
                              FROM users us
                             LEFT JOIN employees emp ON emp.emp_user_id = us.user_id
                             WHERE us.user_id = %s
                               AND us.user_delete_ind = %s'''
            values_user = (user_id, False,  )
            columns_user = ["user_name","user_first_name", "user_last_name", "user_middle_name", "user_name_extension", "emp_number"]
            dfuser = securequerydatafromdatabase(sqluser, values_user, columns_user)
            user_name = dfuser['user_name'][0]

            try:
                user_first_name = dfuser['user_first_name'][0]
                user_last_name = dfuser['user_last_name'][0]
                user_middle_name = dfuser['user_middle_name'][0]
                user_name_extension = dfuser['user_name_extension'][0]
                emp_number = dfuser['emp_number'][0]
            except:
                user_first_name = 'N/A'
                user_last_name = 'N/A'
                user_middle_name = 'N/A'
                user_name_extension = 'N/A'
                emp_number = 'N/A'

            sqlcommand = '''SELECT un.unit_name, unn.unit_name, r.role_name
                              FROM users us
                            LEFT JOIN user_roles ur ON ur.user_id = us.user_id
                            LEFT JOIN units un ON un.unit_id = ur.user_role_unit_id
                            LEFT JOIN units unn ON unn.unit_id = ur.user_role_access_level_unit_id
                            LEFT JOIN employees emp ON emp.emp_user_id = us.user_id
                            LEFT JOIN roles r ON r.role_id = ur.role_id
                             WHERE us.user_id = %s
                               AND us.user_delete_ind = %s
                               AND ur.user_role_delete_ind = %s
        					   AND ur.user_role_default = %s
                               AND un.unit_delete_ind = %s'''
            values = (user_id, False, False, True, False, )
            columns = ["unit_default_name", "access_unit_name", "role_name"]
            df = securequerydatafromdatabase(sqlcommand, values, columns)

            try:
                unit_default_name = df['unit_default_name'][0]
                access_unit_name = df['access_unit_name'][0]
                role_name = df['role_name'][0]
            except:
                unit_default_name = 'N/A'
                access_unit_name = 'N/A'
                role_name = 'N/A'
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
    return [user_name, user_first_name, user_middle_name, user_last_name, user_name_extension, unit_default_name, emp_number, role_name]

@app.callback(
    [
        Output('ddlistofunitsforroles', 'options'),
        Output('ddlistofaccesslevelunitsforroles', 'options'),
    ],
    [
        Input('url', 'search'),

    ],
    [
        State("url", "search"),
    ],
)
def fill_in_dropdowns_for_user_roles_profile(path, url):
    unitoptions = commonmodules.queryfordropdown('''
        SELECT unit_name || ' (' || unit_code || ')' as label,  unit_id as value
       FROM units
       WHERE unit_delete_ind = %s
       ORDER BY unit_name
    ''', (False,))

    return [unitoptions, unitoptions]


@app.callback([
    Output('existinguserrolesdatatableprofile', 'children'),
    Output('existinguserrolesdatatableprofile_inactive', 'children'),
    Output('ddlistofusermodules', 'options'),
    Output('ddlistofunitsforroles', 'value'),
    Output('ddlistofaccesslevelunitsforroles', 'value')
],
    [
    Input("url", "search"),
    Input("user_role_submit", 'n_clicks'),
    Input({'type': 'dynamic_delete_role', 'index': ALL}, 'n_clicks'),
    Input({'type': 'dynamic_inactive_role', 'index': ALL}, 'n_clicks'),
    Input({'type': 'dynamic_active_role', 'index': ALL}, 'n_clicks'),
],
    [
    State("ddlistofusermodules", 'value'),
    State("chksetasdefault", 'value'),
    State('ddlistofunitsforroles', 'value'),
    State('ddlistofaccesslevelunitsforroles', 'value'),
    State('current_user_id', 'data')
],)
def process_user_roles_data(url, user_role_submit, dynamic_delete_role, dynamic_inactive_role, dynamic_active_role, ddlistofusermodules, chksetasdefault, unit_id, access_level_unit_id, current_user_id):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if 'user_id' in parse_qs(parsed.query):
        user_id = parse_qs(parsed.query)['user_id'][0]
    else:
        user_id = "0"
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == 'user_role_submit':
            if ddlistofusermodules:
                if "1" in chksetasdefault:
                    default = True
                    sql = """
                        UPDATE user_roles
                           SET user_role_default = %s
                         WHERE user_id= %s
                           AND user_role_default = %s
                    """
                    values = (False, user_id, True,)
                    modifydatabase(sql, values)
                else:
                    default = False
                sql = """
                    INSERT INTO user_roles (user_id, role_id,  user_role_delete_ind, user_role_default, user_role_unit_id, user_role_access_level_unit_id,
                                            user_role_inserted_by, user_role_inserted_on, user_role_active_ind)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING user_role_id
                """
                values = (user_id, ddlistofusermodules, False, default, unit_id, access_level_unit_id, current_user_id, datetime.now(), True)
                module_role_id = modifydatabasereturnid(sql, values)
            else:
                raise PreventUpdate
        elif eventid == 'url':
            if 'process' in parse_qs(parsed.query):
                role_id = parse_qs(parsed.query)['role_id'][0]
                sql = """
                    UPDATE user_roles SET user_role_delete_ind = True WHERE role_id = """+role_id+""" AND user_id= """ + user_id+"""
                """
                singularcommandupdatedatabase(sql)
        else:

            index = json.loads(eventid)["index"]
            type = json.loads(eventid)["type"]
            user_id = parse_qs(parsed.query)['user_id'][0]
            # print('HERE3245', type)
            if type=="dynamic_delete_role":
                values=[True, False, index, user_id]
                sqlupdate = '''
                                UPDATE user_roles
                                   SET user_role_delete_ind = %s, user_role_active_ind = %s
                                 WHERE user_role_id = %s
                                   AND user_id = %s
                                   '''
                modifydatabase(sqlupdate, values) #AND user_role_unit_id = %s

            elif type=="dynamic_inactive_role":
                sql1 = """
                       SELECT user_role_default
                       FROM user_roles
                       WHERE user_role_id = %s
                       AND user_id = %s
                      """
                values1 = (index, user_id,)
                columns1 = ['user_role_default']
                dfsql1 = securequerydatafromdatabase(sql1, values1, columns1)
                if dfsql1['user_role_default'][0] == False:
                    values=[False, index, user_id]
                    sqlupdate = '''
                                    UPDATE user_roles
                                       SET user_role_active_ind = %s
                                     WHERE user_role_id = %s
                                       AND user_id = %s
                                       '''
                    modifydatabase(sqlupdate, values) #AND user_role_unit_id = %s

            elif type=="dynamic_active_role":

                values=[True, index, user_id]
                sqlupdate = '''
                                UPDATE user_roles
                                   SET user_role_active_ind = %s
                                 WHERE user_role_id = %s
                                   AND user_id = %s
                                   '''
                print('HERE73547', sqlupdate, values)
                modifydatabase(sqlupdate, values) #AND user_role_unit_id = %s
    else:
        pass
    df = query_available_roles("", user_id)
    table = query_added_roles("", user_id)
    table_2 = query_added_roles_inactive("", user_id)

    return [table, table_2, df, "", ""]

#
# @app.callback(
#     [
#         Output('existinguserrolesdatatableprofile', 'children'),
#         Output('ddlistofusermodules', 'options'),
#         Output('user_roles_results_modal', "is_open"),
#         Output('user_roles_results_body', "children"),
#         Output('user_roles_results_head_close', "style"),
#         Output('user_roles_results_head_return', "style"),
#     ],
#     [
#         Input("url", "search"),
#         Input("user_role_submit", 'n_clicks'),
#         Input("btn_user_role_head_close", 'n_clicks')
#     ],
#     [
#         State("ddlistofusermodules", 'value'),
#         State("chksetasdefault", 'value'),
#         State('ddlistofunitsforroles', 'value'),
#     ],
# )
# def processmoduleroles(url, user_role_submit,
#                        btn_user_role_head_close, ddlistofusermodules,
#                        chksetasdefault, unit_id):
#     ctx = dash.callback_context
#     parsed = urlparse.urlparse(url)
#     if 'user_id' in parse_qs(parsed.query):
#         user_id = parse_qs(parsed.query)['user_id'][0]
#     else:
#         user_id = "0"
#     displayed = False
#     message = "Please review input data"
#     stylehead_close = {'display': 'none'}
#     stylehead_return = {'display': 'none'}
#     if ctx.triggered:
#         eventid = ctx.triggered[0]['prop_id'].split('.')[0]
#         if eventid == 'user_role_submit':
#             rolevals = ([6, 7])
#             if (ddlistofusermodules in rolevals):
#                 default = False
#                 # sqlcommand = '''
#                 #     SELECT admin_role_id, admin_pos_name, un.unit_id, un.unit_name
#                 #       FROM admin_employees ae
#                 #     INNER JOIN admin_positions ap ON ap.admin_pos_id = ae.admin_pos_id
#                 #     INNER JOIN units un ON un.unit_id = ap.admin_pos_unit_id
#                 #     INNER JOIN employees emp ON emp.emp_id = ae.emp_id
#                 #     INNER JOIN users us ON us.user_id = emp.emp_user_id
#                 #      WHERE us.user_id = %s
#                 #        AND emp_delete_ind = %s
#                 #        AND admin_role_id = %s
#                 # '''
#                 # values = (user_id, False, ddlistofusermodules,)
#                 # columns = ["admin_role_id", "admin_pos_name", "unit_id", "unit_name"]
#                 # df = securequerydatafromdatabase(sqlcommand, values, columns)
#                 # if df.empty:
#                 #     displayed = True
#                 #     message = "Please review input data"
#                 #     stylehead_close = {'display': 'inline'}
#                 #     stylehead_return = {'display': 'none'}
#                 # else:
#                 sql = """
#                     INSERT INTO user_roles (user_id, role_id,  user_role_delete_ind, user_role_default, user_role_unit_id)
#                     VALUES (%s, %s, %s, %s, %s)
#                     RETURNING user_role_id
#                 """
#                 values = (user_id, ddlistofusermodules, False, default, unit_id)
#                 module_role_id = modifydatabasereturnid(sql, values)
#             elif ddlistofusermodules:
#                 if "1" in chksetasdefault:
#                     default = True
#                     sql = """
#                         UPDATE user_roles
#                            SET user_role_default = %s
#                          WHERE user_id = %s
#                            AND user_role_default = %s
#                     """
#                     values = (False, user_id, True,)
#                     modifydatabase(sql, values)
#                 else:
#                     default = False
#                 sql = """
#                     INSERT INTO user_roles (user_id, role_id,  user_role_delete_ind, user_role_default, user_role_unit_id)
#                     VALUES (%s, %s, %s, %s, %s)
#                     RETURNING user_role_id
#                 """
#                 values = (user_id, ddlistofusermodules, False, default, unit_id)
#                 module_role_id = modifydatabasereturnid(sql, values)
#             else:
#                 raise PreventUpdate
#         elif eventid == 'url':
#             if 'process' in parse_qs(parsed.query):
#
#                 role_id = parse_qs(parsed.query)['role_id'][0]
#                 sql = """
#                     DELETE FROM user_roles WHERE role_id = """+role_id+""" AND user_id= """ + user_id+"""
#                 """
#                 singularcommandupdatedatabase(sql)
#         elif eventid == 'btn_user_role_head_close':
#             displayed = False
#             message = ""
#             stylehead_close = {'display': 'none'}
#             stylehead_return = {'display': 'none'}
#     else:
#         pass
#     df = query_available_roles("", user_id)
#     table = query_added_roles("", user_id)
#     return [table, df, displayed, message, stylehead_close, stylehead_return]


def query_added_roles(sql, user_id):
    sqlcommand = '''
                SELECT ur.user_role_id, ur.role_id, r.role_name, CASE WHEN ur.user_role_default=False THEN 'No' WHEN ur.user_role_default=True THEN 'Yes' END, u.unit_name, un.unit_name
                  FROM user_roles ur inner join roles r ON r.role_id = ur.role_id
                LEFT JOIN units u ON u.unit_id = ur.user_role_unit_id
                LEFT JOIN units un ON un.unit_id = ur.user_role_access_level_unit_id
                 WHERE user_role_delete_ind = %s
                  AND ur.user_id =%s
                  AND ur.user_role_active_ind = %s
                ORDER BY role_name
            '''
    values = (False, user_id, True)
    columns = ["user_role_id","role_id", "role_name", "user_role_default", "unit_name", "unit_name"]
    df = securequerydatafromdatabase(sqlcommand, values, columns)
    df.columns = ["User Role ID","Role ID", "Role Name", "Default Role?", 'Default Unit', "Access Level Unit"]
    table = addcolumntodf_user_roles_profile(df)

    # table = addcolumntodf_user_roles_profile(df, 'Delete', 'Delete', '/settings/settings_user_roles_profile?user_id=' +
    #                       user_id+'&process=delete&role_id=', "Role ID")
    return table

def query_added_roles_inactive(sql, user_id):
    sqlcommand = '''
                SELECT ur.user_role_id, ur.role_id, r.role_name, CASE WHEN ur.user_role_default=False THEN 'No' WHEN ur.user_role_default=True THEN 'Yes' END, u.unit_name, un.unit_name
                  FROM user_roles ur inner join roles r ON r.role_id = ur.role_id
                LEFT JOIN units u ON u.unit_id = ur.user_role_unit_id
                LEFT JOIN units un ON un.unit_id = ur.user_role_access_level_unit_id
                 WHERE user_role_delete_ind = %s
                  AND ur.user_id =%s
                  AND ur.user_role_active_ind = %s
                ORDER BY role_name
            '''
    values = (False, user_id, False)
    columns = ["user_role_id","role_id", "role_name", "user_role_default", "unit_name", "unit_name"]
    df = securequerydatafromdatabase(sqlcommand, values, columns)
    df.columns = ["User Role ID","Role ID", "Role Name", "Default Role?", 'Default Unit', "Access Level Unit"]
    table = addcolumntodf_user_roles_profile_inactive(df)

    # table = addcolumntodf_user_roles_profile(df, 'Delete', 'Delete', '/settings/settings_user_roles_profile?user_id=' +
    #                       user_id+'&process=delete&role_id=', "Role ID")
    return table


def query_available_roles(sql, user_id):
    sql = """
       SELECT role_name as label, role_id as value
         FROM roles
        WHERE role_id NOT IN (SELECT role_id
                                FROM user_roles
                               WHERE user_id=%s
                                 AND user_role_delete_ind = %s)
          AND role_delete_ind = %s
       ORDER BY role_name
      """
    values = (user_id, False, False,)
    columns = ['label', 'value']
    dfsql = securequerydatafromdatabase(sql, values, columns)
    return dfsql.to_dict('records')


def addcolumntodf_user_roles_profile(df):  #, hrefvar, pkid
    linkcolumn = {}
    for index, row in df.iterrows():
        #hrefvar = hrefvar
        # linkcolumn[index] = dcc.Link(label, href=hrefvar+str(row[pkid]))
        linkcolumn[index] = dbc.Button("Delete",id={'index':str(row["User Role ID"]), 'type': 'dynamic_delete_role'}, color="primary", className="mr-1", block=True )
    data_dict = df.to_dict()
    dictionarydata = {'Delete': linkcolumn}
    data_dict.update(dictionarydata)
    df = pd.DataFrame.from_dict(data_dict)

    linkcolumn2 = {}
    for index, row in df.iterrows():
        #hrefvar = hrefvar
        # linkcolumn[index] = dcc.Link(label, href=hrefvar+str(row[pkid]))
        linkcolumn2[index] = dbc.Button("Mark as Inactive",id={'index':str(row["User Role ID"]), 'type': 'dynamic_inactive_role'}, color="primary", className="mr-1", block=True )
    data_dict2 = df.to_dict()
    dictionarydata2 = {'Mark as Inactive': linkcolumn2}
    data_dict2.update(dictionarydata2)
    df2 = pd.DataFrame.from_dict(data_dict2)
    # print('HERE3457', df)


    return dbc.Table.from_dataframe(df2, striped=True, bordered=True, hover=True)

def addcolumntodf_user_roles_profile_inactive(df):  #, hrefvar, pkid
    linkcolumn = {}
    for index, row in df.iterrows():
        #hrefvar = hrefvar
        # linkcolumn[index] = dcc.Link(label, href=hrefvar+str(row[pkid]))
        linkcolumn[index] = dbc.Button("Delete",id={'index':str(row["User Role ID"]), 'type': 'dynamic_delete_role'}, color="primary", className="mr-1", block=True )
    data_dict = df.to_dict()
    dictionarydata = {'Delete': linkcolumn}
    data_dict.update(dictionarydata)
    df = pd.DataFrame.from_dict(data_dict)

    linkcolumn2 = {}
    for index, row in df.iterrows():
        #hrefvar = hrefvar
        # linkcolumn[index] = dcc.Link(label, href=hrefvar+str(row[pkid]))
        linkcolumn2[index] = dbc.Button("Mark as Active",id={'index':str(row["User Role ID"]), 'type': 'dynamic_active_role'}, color="primary", className="mr-1", block=True )
    data_dict2 = df.to_dict()
    dictionarydata2 = {'Mark as Active': linkcolumn2}
    data_dict2.update(dictionarydata2)
    df2 = pd.DataFrame.from_dict(data_dict2)
    # print('HERE3457', df)


    return dbc.Table.from_dataframe(df2, striped=True, bordered=True, hover=True)
