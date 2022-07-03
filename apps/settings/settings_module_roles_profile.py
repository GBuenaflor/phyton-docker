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
        dbc.Card([
            dbc.CardHeader(
                html.H4("Modify Roles For Module", id="module_role_process_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dcc.ConfirmDialog(
                id='role_usermessage',
            ),
            dbc.Modal([
                dbc.ModalHeader("Process roles", id="module_role_results_head"),
                dbc.ModalBody([
                ], id="role_results_body"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Close", id="btn_module_role_head_close",
                                       color="primary", block=True),
                        ], id="roles_results_head_close", style={'display': 'none'}),
                        dbc.Col([
                            dbc.Button("Return", id="btn_module_role_results_head_return",
                                       color="primary", block=True, href='/settings/settings_module_roles'),
                        ], id="module_roles_results_head_return", style={'display': 'none'}),
                    ], style={'width': '100%'}),
                ]),
            ], id="roles_results_modal"),
            dbc.CardBody([
                dcc.Link('← Back to Module Roles', href='/settings/settings_module_roles'),
                html.Br(),
                html.Br(),
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("Role Name", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Label("Role Name", width=6, style={
                                       "text-align": "left"}, id="module_role_name"),
                         ],
                            width=8
                        )],
                        row=True
                    ),
                ]),
                dbc.Card([
                    dbc.CardHeader(
                        html.H5("Select Module to Add"),
                        style={"background-color": "rgb(123,20,24)", 'color': 'white'}
                    ),
                    dbc.CardBody([
                        html.Hr(),
                        dbc.Row([
                            dbc.Col([
                                dcc.Dropdown(
                                    id='ddlistofmodules',
                                    options=[
                                    ],
                                    searchable=True,
                                    clearable=False
                                ),
                            ]),
                            dbc.Col([
                                dbc.Button("Add Selected Module",
                                           id="module_role_submit", color="info"),
                            ]),
                        ], style={'width': '100%'}),
                        html.Hr(),
                        dbc.Row([
                            dbc.Col([

                            ]),
                            dbc.Col([
                                #dbc.Button("Cancel", id="module_role_cancel", color="warning", className="ml-auto")
                            ]),
                        ], style={'width': '100%'}),
                    ], style={'line-height': "1em", "display": "block"}),
                ]),
                html.Hr(),

                html.Div([
                    dbc.Row([
                        # dbc.Col([
                        #     html.H4("Existing Modules"),
                        #     html.Div([
                        #         html.Div([
                        #
                        #         ],id="editrolesdatatableprofilemodule"),
                        #
                        #     ], style={'width':'100%','padding':'10px'}),
                        # ]),
                        dbc.Col([
                            html.H4("Currrent Modules"),
                            html.Div([
                                html.Div([

                                ], id="existingrolesdatatableprofilemodule"),
                                #     dash_table.DataTable(
                                #     page_action='none',
                                #     style_cell={'textAlign': 'center',
                                #                 'textOverflow': 'ellipsis',
                                #                 'maxWidth': 0,
                                #                 'height': 'auto',
                                #                 'whiteSpace': 'normal',
                                #                 'fontSize': 15, 'font-family': 'sans-serif', 'textAlign': 'center'},
                                #     row_selectable="single",
                                #     style_header={'backgroundColor': 'black',
                                #                   'color': 'white', 'fontWeight': 'bold', 'height': 'auto',
                                #                   'whiteSpace': 'normal'},  # 'width': '20px',
                                #     style_as_list_view=True,
                                #     style_data_conditional=[
                                #         {
                                #             'if': {
                                #                 'column_id': 'Consultation Status',
                                #                 'filter_query': '{Consultation Status} eq "For Triaging"'
                                #             },
                                #
                                #             'backgroundColor': 'rgb(177,252,152)',
                                #             'color': 'black',
                                #         },
                                #         {
                                #             'if': {'column_id': 'Consultation Ref No'},
                                #             'width': '8%'
                                #         },
                                #         {
                                #             'if': {'column_id': 'In CARROT?'},
                                #             'width': '6%'
                                #         },
                                #
                                #     ],
                                #     style_cell_conditional=[
                                #         {'if': {'column_id': 'Request Date'},
                                #          'width': '10%', 'textAlign': 'center'},
                                #         {
                                #             'if': {'row_index': 'odd'},
                                #             'backgroundColor': 'rgb(248, 248, 248)'
                                #         },
                                #         {
                                #             'if': {'column_id': 'Select'},
                                #             'width': '10%', 'textAlign': 'center', 'backgroundColor': 'rgb(128, 0, 0)', 'color': 'white', 'cursor': 'pointer'
                                #         },
                                #
                                #     ],
                                #     css=[{
                                #         'selector': '.dash-cell div.dash-cell-value',  # , 'width': 'inherit',
                                #         'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                                #     }],
                                #     id='dtmodulesexisting'
                                # )
                            ], style={'width': '100%', 'padding': '10px'}),
                        ]),
                    ], style={'width': '100%'}),
                ]),

            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback([
    Output('existingrolesdatatableprofilemodule', 'children'),
    Output('ddlistofmodules', 'options')
],
    [
    Input("url", "search"),
    Input("module_role_submit", 'n_clicks')
],
    [
    State("ddlistofmodules", 'value'),
    State('current_user_id', 'data'),
],)
def processmoduleroles(url, module_role_submit, ddlistofmodules, current_user_id):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if 'role_id' in parse_qs(parsed.query):
        role_id = parse_qs(parsed.query)['role_id'][0]
    else:
        role_id = "0"
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == 'module_role_submit':

            if ddlistofmodules:
                sql = """
                    INSERT INTO module_roles (role_id, module_id, module_role_inserted_by, module_role_inserted_on, module_role_delete_ind)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING module_role_id
                """
                values = (role_id, ddlistofmodules, current_user_id, datetime.now(), False)

                module_role_id = modifydatabasereturnid(sql, values)

            else:
                raise PreventUpdate
        elif eventid == 'url':
            if 'process' in parse_qs(parsed.query):

                module_id = parse_qs(parsed.query)['module_id'][0]
                sql = """
                    DELETE FROM module_roles WHERE role_id = """+role_id+""" AND module_id= """ + module_id+"""
                """
                singularcommandupdatedatabase(sql)
    else:
        pass
    df = queryavailablemodules("", role_id)
    table = queryaddedmodules("", role_id)
    return [table, df]


def queryaddedmodules(sql, role_id):
    sqlcommand = '''SELECT mr.module_id, m.module_header, m.module_name
    FROM module_roles mr inner join modules m ON m.module_id = mr.module_id
    WHERE module_delete_ind = %s and mr.role_id =%s
    ORDER By module_header, module_name'''
    values = (False, role_id)
    columns = ["module_id", "module_header", "module_name"]
    df = securequerydatafromdatabase(sqlcommand, values, columns)
    df.columns = ["Module ID", "Module Header", "Module Name"]
    table = addcolumntodf(df, 'Delete', 'Delete', '/settings/settings_module_roles_profile?role_id=' +
                          role_id+'&process=delete&module_id=', "Module ID")
    return table


def queryavailablemodules(sql, role_id):
    sql = """SELECT module_header  || '-' || module_name as label, module_id as value
       FROM modules
	   WHERE module_id NOT IN (SELECT module_id FROM module_roles WHERE role_id=%s)
       and module_delete_ind = %s
	   ORDER BY module_header, module_name
      """
    values = (role_id, False)
    columns = ['label', 'value']
    dfsql = securequerydatafromdatabase(sql, values, columns)
    return dfsql.to_dict('records')


def addcolumntodf(df, collabel, label, hrefvar, pkid):
    linkcolumn = {}
    for index, row in df.iterrows():
        #hrefvar = hrefvar
        linkcolumn[index] = dcc.Link(label, href=hrefvar+str(row[pkid]))
    data_dict = df.to_dict()
    dictionarydata = {collabel: linkcolumn}
    data_dict.update(dictionarydata)
    df = pd.DataFrame.from_dict(data_dict)
    return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)


# @app.callback([
#                 ],
#                 [
#                 Input("url", "search"),
#
#                 ],
#               [
#               ],)
# def querymodules(url):
#
#     return [df]


@app.callback(
    [
        Output('module_role_name', 'children'),
        # Output("module_role_process_editmodalhead", "children"),
        # Output("module_role_submit", "children"),
        # Output("role_id", 'value'),
    ],
    [
        # Input('role_submit_status', 'value'),
        # Input('btn_module_role_head_close', 'n_clicks'),
        Input("url", "pathname"),
    ],
    [
        State("url", "search"),
        # State('role_name', 'value'),
        # State('role_process_editmodalhead',"children"),
        # State("role_submit", "children"),
        # State("role_id", 'value'),
        # State("role_chkmarkfordeletion", "value"),
    ]
)
def cleardata(path, url):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":
            role_id = parse_qs(parsed.query)['role_id'][0]
            sql = '''SELECT role_name
                       FROM roles
                      WHERE role_id = %s
                        AND  role_delete_ind = %s '''
            values = (role_id, False)
            columns = ['role_name']
            df = securequerydatafromdatabase(sql, values, columns)
            role_name = df["role_name"][0]
            values = [role_name]
            return values
        elif parse_qs(parsed.query)['mode'][0] == "add":
            values = [""]
            return values
    else:
        raise PreventUpdate
#
# @app.callback(
#     [
#         Output("role_name", "valid"),
#         Output("role_name", "invalid"),
#         Output('role_submit_status',"value"),
#         Output('roles_results_modal',"is_open"),
#         Output('role_results_body',"children"),
#         Output('roles_results_head_close',"style"),
#         Output('roles_results_head_return',"style"),
#     ],
#     [
#         Input('role_submit', 'n_clicks'),
#         Input('btn_role_head_close', 'n_clicks'),
#         Input('btn_role_results_head_return', 'n_clicks'),
#     ],
#     [
#         State('current_user_id', 'data'),
#         State('role_name', 'value'),
#         State("role_submit", "children"),
#         State("role_chkmarkfordeletion", "value"),
#         State("url", "search"),
#         State('role_id', 'value'),
#     ]
#
# )
# def processdata(role_submit,btn_role_head_close,btn_role_results_head_return,
#     current_user_id, role_name, mode, role_chkmarkfordeletion,url,role_id):
#     ctx = dash.callback_context
#     stylehead_close = {'display':'none'}
#     stylehead_return = {'display':'none'}
#     parsed = urlparse.urlparse(url)
#
#     if ctx.triggered:
#         validity = [
#             False, False
#             ]
#         eventid = ctx.triggered[0]['prop_id'].split('.')[0]
#         if eventid == 'role_submit':
#             if role_name:
#                 is_valid_role_name= True
#             else:
#                 is_valid_role_name= False
#
#             validity = [
#                 is_valid_role_name, not is_valid_role_name,
#
#             ]
#             allvalid = [is_valid_role_name]
#             if all(allvalid):
#                 if mode =="Save New Role":
#                     sql = """
#                         INSERT INTO roles (role_name, role_delete_ind,
#                         role_modified_by, role_modified_on)
#                         VALUES (%s, %s, %s, %s)
#                         RETURNING role_id
#                     """
#                     values = (role_name, False, current_user_id, datetime.now())
#                     role_id = modifydatabasereturnid(sql,values)
#                     displayed = True
#                     message = "Successfully added new role"
#                     status = "1"
#                     stylehead_close = {'display':'inline'}
#                     stylehead_return = {'display':'none'}
#                 else:
#                     sql = """
#                         UPDATE roles SET role_name = %s,
#                             role_delete_ind= %s, role_modified_by= %s, role_modified_on= %s WHERE
#                             role_id = %s
#                     """
#                     if '1' in role_chkmarkfordeletion:
#                         fordelete = True
#                     else:
#                         fordelete= False
#                     values = (role_name, fordelete, current_user_id, datetime.now(), role_id)
#                     modifydatabase(sql,values)
#                     validity = [
#                         False, False
#                         ]
#                     stylehead_close = {'display':'none'}
#                     stylehead_return = {'display':'inline'}
#                     displayed = True
#                     message = "Successfully edited role"
#                     status = "1"
#             else:
#                 status = "2"
#                 displayed = True
#                 message = "Please review input data"
#                 stylehead_close = {'display':'inline'}
#                 stylehead_return = {'display':'none'}
#             out = [status, displayed, message, stylehead_close, stylehead_return]
#             out = validity+out
#
#             return out
#         elif eventid == 'btn_role_head_close':
#             status = "0"
#             displayed = False
#             message = "Please review input data"
#             stylehead_close = {'display':'inline'}
#             stylehead_return = {'display':'none'}
#             out = [status, displayed, message, stylehead_close, stylehead_return]
#             out = validity+out
#             return out
#         else:
#             raise PreventUpdate
#     else:
#         raise PreventUpdate


# @app.callback(
#     [
#         Output('module_role_name', 'value'),
#         Output("module_role_process_editmodalhead", "children"),
#         Output("module_role_submit", "children"),
#         Output("role_id",'value'),
#     ],
#     [
#         Input('role_submit_status', 'value'),
#         Input('btn_module_role_head_close', 'n_clicks'),
#         Input("url", "search"),
#     ],
#     [
#         State('role_name', 'value'),
#         State('role_process_editmodalhead',"children"),
#         State("role_submit", "children"),
#         State("role_id",'value'),
#         State("role_chkmarkfordeletion", "value"),
#     ]
#
# )
# def cleardata(role_submit_status,btn_role_head_close,url,
#     role_name, role_process_editmodalhead,role_submit,role_id,role_chkmarkfordeletion):
#     ctx = dash.callback_context
#     parsed = urlparse.urlparse(url)

#     if parsed.query:
#         if parse_qs(parsed.query)['mode'][0] == "edit":
#             role_id = parse_qs(parsed.query)['role_id'][0]
#             sql = '''SELECT * FROM roles WHERE role_id='''+str(role_id)
#             df = querydatafromdatabase(sql)
#             role_name = df["role_name"][0]
#             values = [role_name,"Edit Existing role:","Save Changes",role_id,[],{'text-align':'middle', 'display':'inline'}]
#             return values
#         elif parse_qs(parsed.query)['mode'][0] == "add":
#             values = ["",role_process_editmodalhead,role_submit,role_id,[],{'display':'none'}]
#             return values
#     else:
#         raise PreventUpdate
