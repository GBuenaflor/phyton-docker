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
from apps.commonmodules import checkiflengthzero2, checkstyle2



app.config.suppress_callback_exceptions = False
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


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
                html.H4("Add New Leave Approval Status", id="leave_approval_status_profile_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),

            dbc.CardBody([
                dcc.Link('← Back to Leave Approval Statuses', href='/settings/settings_leave_approval_statuses'),
                html.Br(),
                html.Br(),
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("Leave Approval Status Name", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="leave_approval_status_profile_name", placeholder="Enter Leave Approval Status"
                             ),
                             dbc.FormFeedback("Enter a valid Leave approval status", valid=False)
                         ],
                            width=8
                        )],
                        row=True
                    ),

                    dbc.FormGroup(
                        [dbc.Label("Leave Approval Status Description", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="leave_approval_status_profile_description", placeholder="e.g. Leave Application is for VCA Approval"
                             ),
                             dbc.FormFeedback("Enter a valid Leave approval status description", valid=False)
                         ],
                             width=8
                         )],
                        row=True
                    ),

                    dbc.FormGroup(
                        [dbc.Label("Leave Status Past Name", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="leave_approval_status_profile_pastname", placeholder="e.g. Approved by VCA"
                             ),
                             dbc.FormFeedback("Enter a valid BP approval status description", valid=False)
                         ],
                             width=8
                         )],
                        row=True
                    ),



                    dbc.FormGroup(
                        [dbc.Label("Leave Approval Status Type", width=2, style={"text-align": "left"}, id = 'leave_approval_status_profile_type_label'),
                         dbc.Col([
                             dcc.Dropdown(
                                 id="leave_approval_status_profile_type",
                                 options=[
                                    {'label': 'Approval Status', 'value': 0},
                                    {'label': 'Return Status', 'value': 1},
                                    {'label': 'Terminal Status', 'value': 2},
                                    {'label': 'In Process Status', 'value': 3},

                                 ],
                                 searchable=False,
                                 value = 0
                             ),
                             dbc.FormFeedback("Select a Leave status type", valid=False)
                         ],
                             width=8
                         )],
                        row=True
                    ),

                    html.Hr(),


                    html.Div([
                        dbc.Card([
                            dbc.CardHeader(
                                html.H4("Add Role to Approval Status", id="leave_approval_status_profile_add_role_to_status"),
                                style={"background-color": "rgb(123,20,24)", 'color': 'white', 'height':45}
                            ),

                            dbc.CardBody([
                            html.H5("To add role to this Leave Approval Status, select a role below and click Add Role.", style={'font-style': 'italic'}),
                            dbc.FormGroup(
                                [dbc.Label("Add Approving Role to Leave Approval Status", width=2, style={"text-align": "left"}, id = 'leave_approval_status_profile_role_label'),
                                 dbc.Col([
                                     dcc.Dropdown(
                                         id="leave_approval_status_profile_addrole",
                                         options=[
                                         ],
                                         searchable=True
                                     ),
                                     #dbc.FormFeedback("Too short or already taken", valid = False)
                                 ],
                                    width=8
                                )],
                                row=True
                            ),

                            dbc.Button("Add Role", id="leave_approval_status_profile_addrolebtn", color="primary", block=False),
                            html.Br(),
                            html.Br(),
                            dbc.Label("Roles Associated with this Approval Status:", width=4, style={"text-align": "left"}),
                            html.Div([
                            ], id='leave_approval_status_profile_rolesdiv'),
                            ], style={'line-height': ".75em", "display": "block"}),
                        ], style={'line-height': ".75em", "display": "block"}),
                        dbc.Card([
                            dbc.CardHeader(
                                html.H4("Remove Role from Approval Status", id="leave_approval_status_profile_remove_role_to_status"),
                                style={"background-color": "rgb(123,20,24)", 'color': 'white', 'height':45}
                            ),

                            dbc.CardBody([
                                html.H5("To remove a role associated from the table above, select a role below and click Remove Role.", style={'font-style': 'italic'}),
                                html.Br(),
                                dbc.FormGroup(
                                    [
                                     dbc.Label("Remove Approving Role to Status", width=2, style={"text-align": "left"},
                                               id='leave_approval_status_profile_role_label'),
                                     dbc.Col([
                                         dcc.Dropdown(
                                             id="leave_approval_status_profile_removerole",
                                             options=[
                                                 # {'label': 'Faculty', 'value': '1'},
                                                 # {'label': 'Administrative Personnel', 'value': '2'},
                                                 # {'label': 'Research and Extension Professional Staff (REPS)', 'value': '3'},
                                                 # {'label': 'Others', 'value': '11'}
                                             ],
                                             searchable=False
                                         ),
                                         # dbc.FormFeedback("Too short or already taken", valid = False)
                                     ],
                                         width=8
                                     )],
                                    row=True
                                ),

                            dbc.Button("Remove Role", id="leave_approval_status_profile_removerolebtn", color="warning", block=False),
                            dbc.Tooltip("This removes the role selected (in the dropdown) from the above table.", target = 'leave_approval_status_profile_removerolebtn',placement = "right"),
                            html.Br(),
                            html.Br(),
                            html.Hr(),
                            ], style={'line-height': ".75em", "display": "block"}),
                        ], id = 'card_remove_role_from_approval_statuses', style={'line-height': ".75em", "display": "block"}),
                        ], id='div_leave_approval_status_profile_roles',
                            # style={'display':'none'}
                    ),
                    html.Div([
                        dcc.Checklist(
                            options=[
                                {'label': ' Delete the Approval Status?', 'value': '1'},
                            ], id='leave_approval_status_profile_chkmarkfordeletion', value=[]
                        ),
                    ], id='leave_approval_status_profile_deletediv',  style={'text-align': 'middle', 'display': 'inline'}),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save New Leave Approval Status", id="leave_approval_status_profile_submitbtn",
                                   color="primary", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="leave_approval_status_profile_cancel",
                                   href='/settings/settings_leave_approval_statuses', color="secondary", className="ml-auto")
                    ]),
                ], style={'width': '100%'}),


                dbc.Modal(
                    [
                        dbc.ModalHeader("Leave Approval Status Encoding Confirmation", id='leave_approval_status_profile_submitmodal1header'),
                        dbc.ModalBody("Confirm Leave Approval Status Entry Submission",
                                      id='leave_approval_status_profile_submitmodal1body'),
                        dbc.ModalFooter([
                            dbc.Button("Confirm", id="leave_approval_status_profile_submitmodal1go", className="mr-1",
                                       color='primary'),
                            dbc.Button("Back", id='leave_approval_status_profile_submitmodal1back', className="ml-auto")

                            # dbc.Button("Back to Home", id='leave_approval_status_profile_submitmodal2_returnbtn', className="ml-auto", href = '/')
                        ]),
                    ],
                    id="leave_approval_status_profile_submitmodal1",
                ),

                dbc.Modal(
                    [
                        dbc.ModalHeader("Leave Approval Status Encoding", id='leave_approval_status_profile_submitmodal2_header'),
                        dbc.ModalBody("Leave Approval Statuses has been successfully updated.",
                                      id='leave_approval_status_profile_submitmodal2_body'),
                        dbc.ModalFooter([
                            dbc.Button(
                                "Back to Leave Approval Statuses", id='leave_approval_status_profile_submitmodal2_closebtn', className="ml-auto", color = 'primary',
                                # href = '/settings/settings_person_employee_encoding',
                                href='/settings/settings_leave_approval_statuses',
                            ),
                            dbc.Button(
                                "Close", id='leave_approval_status_profile_submitmodal2_closebtn', className="ml-auto",color = 'primary',
                                # href = '/settings/settings_person_employee_encoding',
                                href='/home',
                            ),
                            # dbc.Button("Back to Home", id='leave_approval_status_profile_submitmodal2_returnbtn', className="ml-auto", href = '/')
                        ]),
                    ],
                    id="leave_approval_status_profile_submitmodal2",
                ),

                dbc.Input(id = 'leave_approval_status_profile_proxyinput', value = 0, style = {'display':'none'})


            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )


    ]),


])


@app.callback(
    [
        Output('leave_approval_status_profile_proxyinput', 'value')
    ],
    [
        Input('leave_approval_status_profile_addrolebtn', 'n_clicks'),
        Input('leave_approval_status_profile_removerolebtn', 'n_clicks'),
    ],
    [
        State('url', 'search'),
        State('leave_approval_status_profile_addrole', 'value'),
        State('leave_approval_status_profile_removerole', 'value'),
        State('current_user_id', 'data'),
    ]
)
def leavestatus_updateaddremoveroles(leave_approval_status_profile_addrolebtn, leave_approval_status_profile_removerolebtn,
                         url, leave_approval_status_profile_addrole, leave_approval_status_profile_removerole, current_user_id):

    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)

    if parse_qs(parsed.query):
        mode = str(parse_qs(parsed.query)['mode'][0])
        if mode == "edit":
            leave_status_id = str(parse_qs(parsed.query)['leave_status_id'][0])

        if ctx.triggered:
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]

            if eventid == 'leave_approval_status_profile_addrolebtn':
                sqlupdate = '''
                            INSERT INTO leave_status_roles (leave_status_id, role_id, leave_status_role_module_type, leave_status_role_inserted_by, leave_status_role_inserted_on, leave_status_role_delete_ind)
                            VALUES (%s, %s, %s, %s, %s, %s)

                '''
                values = (leave_status_id, leave_approval_status_profile_addrole, 1, current_user_id, datetime.now(), False)

                modifydatabase(sqlupdate, values)

            elif eventid == 'leave_approval_status_profile_removerolebtn':

                sqlupdate = '''
                        UPDATE leave_status_roles
                           SET leave_status_role_delete_ind = %s,
                               leave_status_role_last_modified_by = %s,
                               leave_status_role_last_modified_on = %s
                         WHERE leave_status_id = %s
                           AND role_id = %s
                            '''
                values = (True, current_user_id, datetime.now(), leave_status_id, leave_approval_status_profile_removerole )
                dataframe = modifydatabase(sqlupdate, values)


            return [1]

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('leave_approval_status_profile_rolesdiv', 'children'),
        Output('leave_approval_status_profile_addrole', 'options'),
        Output('leave_approval_status_profile_removerole', 'options'),
    ],
    [
        Input("url", "search"),
        Input('leave_approval_status_profile_addrolebtn', 'n_clicks'),
        Input('leave_approval_status_profile_removerolebtn', 'n_clicks'),
    ]
)
def leavestatus_loadrolestable(url, leave_approval_status_profile_addrolebtn, leave_approval_status_profile_removerolebtn):
    addroleoptions = []
    removeroleoptions = []
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":

            leave_status_id = str(parse_qs(parsed.query)['leave_status_id'][0])
            sql1 = '''
                        SELECT lsr.role_id, r.role_name
                          FROM leave_status_roles lsr
                        LEFT JOIN roles r ON r.role_id = lsr.role_id
                         WHERE lsr.leave_status_id = %s
                           AND lsr.leave_status_role_delete_ind = %s

                '''

            addroleoptions = commonmodules.queryfordropdown('''
                        SELECT role_name as label, role_id as value
                          FROM roles
                         WHERE role_delete_ind = %s
                           AND role_id NOT IN (
                                    SELECT r.role_id
                                      FROM leave_status_roles lsr
                                    LEFT JOIN roles r ON r.role_id = lsr.role_id
                                     WHERE lsr.leave_status_id = %s
                                       AND lsr.leave_status_role_delete_ind = %s

                        )
                        ORDER BY role_name
                   ''', (False, leave_status_id, False))

            removeroleoptions = commonmodules.queryfordropdown('''

                        SELECT r.role_name as label, lsr.role_id as value
                          FROM leave_status_roles lsr
                        LEFT JOIN roles r ON r.role_id = lsr.role_id
                         WHERE lsr.leave_status_id = %s
                           AND lsr.leave_status_role_delete_ind = %s

                   ''', (leave_status_id, False))

            values1 = (leave_status_id, False)
            columns1 = ['role_id', 'role_name']
            df = securequerydatafromdatabase(sql1, values1, columns1)
            df.columns = ['Role ID', 'Role']

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

        elif parse_qs(parsed.query)['mode'][0] == "add":


            addroleoptions = commonmodules.queryfordropdown('''
                        SELECT role_name as label, role_id as value
                          FROM roles
                         WHERE role_delete_ind = %s
                        ORDER BY role_name
                   ''', (False, ))

            # removeroleoptions = commonmodules.queryfordropdown('''
            #             SELECT r.role_name as label, lsr.role_id as value
            #               FROM leave_status_roles lsr
            #             LEFT JOIN roles r ON r.role_id = lsr.role_id
            #              WHERE lsr.leave_status_id = %s
            #                AND lsr.leave_status_role_delete_ind = %s
            #
            #        ''', (leave_status_id, False))
            removeroleoptions = ""

            sql1 = '''
                        SELECT lsr.role_id, r.role_name
                          FROM leave_status_roles lsr
                        LEFT JOIN roles r ON r.role_id = lsr.role_id
                         WHERE lsr.leave_status_role_delete_ind = %s

                '''

            values1 = (False,)
            columns1 = ['role_id', 'role_name']
            df = securequerydatafromdatabase(sql1, values1, columns1)
            df.columns = ['Role ID', 'Role']

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

        else:
            table = []

        return [table, addroleoptions, removeroleoptions]

    else:
        raise PreventUpdate


@app.callback(
    [
        Output('leave_approval_status_profile_name', 'value'),
        Output('leave_approval_status_profile_description', 'value'),
        Output('leave_approval_status_profile_pastname', 'value'),
        Output('leave_approval_status_profile_type', 'value'),
        Output('leave_approval_status_profile_addrole', 'value'),


        Output("leave_approval_status_profile_editmodalhead", "children"),
        Output("leave_approval_status_profile_submitbtn", "children"),
        Output("leave_approval_status_profile_chkmarkfordeletion", "style"),
        Output('div_leave_approval_status_profile_roles', 'style'),

        Output('card_remove_role_from_approval_statuses', 'style')
    ],
    [
        Input("url", "search"),
    ],
    [

    ]

)
def clearleavestatusapprovaldata(url,
              ):
    div_leave_approval_status_profile_roles_style = {'display':'inline'}
    table = []

    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":


            leave_status_id = str(parse_qs(parsed.query)['leave_status_id'][0])
            div_leave_approval_status_profile_roles_style = {'display': 'inlne'}
            leave_approval_status_profile_editmodalhead = "Edit Existing Leave Approval Status"
            leave_approval_status_profile_submit = "Save Changes"
            leave_approval_status_profile_chkmarkfordeletion_style = {"display": "inline"}
            leave_status_id = parse_qs(parsed.query)['leave_status_id'][0]

            sql = '''

            SELECT leave_status_name, leave_status_desc, leave_status_past_name, leave_status_type, r.role_id
              FROM leave_statuses ls
            LEFT JOIN leave_status_roles lsr ON ls.leave_status_id = lsr.leave_status_id
            LEFT JOIN roles r ON r.role_id = lsr.role_id
             WHERE leave_status_delete_ind = %s
               AND ls.leave_status_id = %s
            '''
            values = (False, leave_status_id,)
            columns = ['leave_status_name', 'leave_status_desc', 'leave_status_past_name', 'leave_status_type', 'role_id']
            df = securequerydatafromdatabase(sql, values, columns)

            leave_status_name = df["leave_status_name"][0]
            leave_status_desc = df["leave_status_desc"][0]
            leave_status_past_name = df["leave_status_past_name"][0]
            leave_status_type = df["leave_status_type"][0]
            role_id = df["role_id"][0]

            card_remove_role_from_approval_statuses_style = {'display':'inline'}


        elif parse_qs(parsed.query)['mode'][0] == "add":

            div_leave_approval_status_profile_roles_style = {'display': 'none'}
            leave_approval_status_profile_editmodalhead = "Add New Leave Approval Status"
            leave_approval_status_profile_submit = "Save New Leave Approval Status"
            leave_approval_status_profile_chkmarkfordeletion_style = {"display": "none"}
            card_remove_role_from_approval_statuses_style = {"display": "none"}
            leave_status_name = ""
            leave_status_desc= ""
            leave_status_past_name= ""
            leave_status_type = ""
            role_id= ""
        else:
            raise PreventUpdate

        return [leave_status_name, leave_status_desc, leave_status_past_name,leave_status_type, role_id,
                leave_approval_status_profile_editmodalhead, leave_approval_status_profile_submit, leave_approval_status_profile_chkmarkfordeletion_style,
                div_leave_approval_status_profile_roles_style, card_remove_role_from_approval_statuses_style]

    else:

        raise PreventUpdate


@app.callback(
    [
        Output('leave_approval_status_profile_name', 'valid'),
        Output('leave_approval_status_profile_name', 'invalid'),
        Output('leave_approval_status_profile_description', 'valid'),
        Output('leave_approval_status_profile_description', 'invalid'),
        Output('leave_approval_status_profile_pastname', 'valid'),
        Output('leave_approval_status_profile_pastname', 'invalid'),
        Output('leave_approval_status_profile_type_label', 'style'),
        Output('leave_approval_status_profile_submitmodal1', 'is_open')
    ],
    [
        Input('leave_approval_status_profile_submitbtn', 'n_clicks'),
        Input('leave_approval_status_profile_submitmodal1go', 'n_clicks'),
        Input('leave_approval_status_profile_submitmodal1back', 'n_clicks')
    ],
    [
        State('leave_approval_status_profile_name', 'value'),
        State('leave_approval_status_profile_description', 'value'),
        State('leave_approval_status_profile_pastname', 'value'),
        State('leave_approval_status_profile_type', 'value'),
    ]
)
def leave_approval_status_validity(leave_approval_status_profile_submitbtn, leave_approval_status_profile_submitmodal1go, leave_approval_status_profile_submitmodal1back,
                          leave_approval_status_profile_name, leave_approval_status_profile_description, leave_approval_status_profile_pastname, leave_approval_status_profile_type):

    leave_approval_status_profile_submitmodal1 = False
    ctx = dash.callback_context
    if ctx.triggered:

        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        leave_approval_status_profile_namevalid = checkiflengthzero2(leave_approval_status_profile_name)
        leave_approval_status_profile_descriptionvalid = checkiflengthzero2(leave_approval_status_profile_description)
        leave_approval_status_profile_pastnamevalid = checkiflengthzero2(leave_approval_status_profile_pastname)
        leave_approval_status_profile_typevalid = checkiflengthzero2(leave_approval_status_profile_type+1)

        leave_approval_status_profile_type_label = checkstyle2(leave_approval_status_profile_typevalid)


        allvalid = [leave_approval_status_profile_namevalid, leave_approval_status_profile_descriptionvalid, leave_approval_status_profile_pastnamevalid, leave_approval_status_profile_typevalid]


        if all(allvalid):

            leave_approval_status_profile_submitmodal1 = True

        if eventid in ['leave_approval_status_profile_submitbtn','leave_approval_status_profile_submitmodal1go', 'leave_approval_status_profile_submitmodal1back']:
            if eventid in ['leave_approval_status_profile_submitmodal1go', 'leave_approval_status_profile_submitmodal1back']:

                leave_approval_status_profile_submitmodal1 = False

            return [leave_approval_status_profile_namevalid, not leave_approval_status_profile_namevalid,
                    leave_approval_status_profile_descriptionvalid, not leave_approval_status_profile_descriptionvalid,
                    leave_approval_status_profile_pastnamevalid, not leave_approval_status_profile_pastnamevalid,
                    leave_approval_status_profile_type_label,
                    leave_approval_status_profile_submitmodal1]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('leave_approval_status_profile_submitmodal2', 'is_open')
    ],
    [
        Input('leave_approval_status_profile_submitmodal1go', 'n_clicks'),
        Input('leave_approval_status_profile_submitmodal2_closebtn', 'n_clicks')
    ],
    [
        State('leave_approval_status_profile_name', 'value'),
        State('leave_approval_status_profile_description', 'value'),
        State('leave_approval_status_profile_pastname', 'value'),
        State('leave_approval_status_profile_type', 'value'),
        State('leave_approval_status_profile_addrole', 'value'),
        State('leave_approval_status_profile_chkmarkfordeletion', 'value'),
        State('url', 'search'),
        State('current_user_id', 'data'),
    ]
)

def leave_approval_status_profile_submitmodal2(leave_approval_status_profile_submitmodal1go, leave_approval_status_profile_submitmodal2_closebtn,
                            leave_approval_status_profile_name, leave_approval_status_profile_description, leave_approval_status_profile_pastname, leave_approval_status_profile_type, leave_approval_status_profile_role,
                            leave_approval_status_profile_chkmarkfordeletion,
                            url,
                            current_user_id):

    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parse_qs(parsed.query):
        if ctx.triggered:
            mode = str(parse_qs(parsed.query)['mode'][0])
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]
            if eventid == 'leave_approval_status_profile_submitmodal1go':

                if mode == "add":

                    sql1 = """
                        INSERT INTO leave_statuses(leave_status_name, leave_status_desc, leave_status_past_name,
                                                leave_status_inserted_by, leave_status_inserted_on, leave_status_delete_ind, leave_status_type)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    values1 = [leave_approval_status_profile_name, leave_approval_status_profile_description, leave_approval_status_profile_pastname,
                               current_user_id, datetime.now(), False, leave_approval_status_profile_type]
                    modifydatabase(sql1, values1)

                    sql = '''
                    SELECT leave_status_id
                      FROM leave_statuses
                     WHERE leave_status_delete_ind = %s
                       AND leave_status_name = %s
                       AND leave_status_desc = %s
                       AND leave_status_past_name = %s
                       AND leave_status_type = %s
                    '''
                    values = (False, leave_approval_status_profile_name,leave_approval_status_profile_description, leave_approval_status_profile_pastname, leave_approval_status_profile_type)
                    columns = ['leave_status_id']
                    df = securequerydatafromdatabase(sql, values, columns)

                    leave_status_id = int(df['leave_status_id'][0])

                elif mode == "edit":

                    leave_status_id = str(parse_qs(parsed.query)['leave_status_id'][0])

                    leave_approval_status_profile_deletevalue = False

                    if 1 in leave_approval_status_profile_chkmarkfordeletion or '1' in leave_approval_status_profile_chkmarkfordeletion:
                        leave_approval_status_profile_deletevalue = True

                    sql1 = """
                        UPDATE leave_statuses
                           SET leave_status_name = %s,
                               leave_status_desc=%s,
                               leave_status_past_name=%s,
                               leave_status_last_modified_by = %s,
                               leave_status_last_modified_on = %s,
                               leave_status_delete_ind = %s,
                               leave_status_type = %s
                         WHERE leave_status_id=%s
                    """
                    values1 = [leave_approval_status_profile_name, leave_approval_status_profile_description, leave_approval_status_profile_pastname,
                                current_user_id, datetime.now(), leave_approval_status_profile_deletevalue, leave_approval_status_profile_type,
                               leave_status_id]
                    modifydatabase(sql1, values1)

                    # if leave_approval_status_profile_type == 0:
                    #     sql2 = """
                    #         UPDATE leave_status_roles
                    #            SET role_id = %s,
                    #                leave_status_role_last_modified_by = %s,
                    #                leave_status_role_last_modified_on = %s,
                    #                leave_status_role_delete_ind = %s
                    #          WHERE leave_status_id=%s
                    #     """
                    #     values2 = [leave_approval_status_profile_role,
                    #                 current_user_id, datetime.now(), leave_approval_status_profile_deletevalue,
                    #                leave_status_id
                    #                ]
                    #     modifydatabase(sql2, values2)
                    # else:
                    #     pass
                return [True]

            elif eventid == "leave_approval_status_profile_submitmodal2_closebtn":
                return [False]

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
