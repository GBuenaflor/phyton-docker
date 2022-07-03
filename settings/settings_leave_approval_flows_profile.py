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

    dcc.Store(id='leave_approval_flows_profile_sessionproxy', storage_type='session'),
    html.H1("Leave Approval Flows"),
    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Add New Leave Approval Flow", id="leave_approvalflow_process_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.Modal([
                dbc.ModalHeader("Process Leave Approval Flows", id="leave_approvalflows_results_head"),
                dbc.ModalBody([
                ], id="leave_approvalflow_results_body"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Close", id="leave_btn_approvalflow_head_close",
                                       color="primary", block=True, href = "/settings/settings_leave_approval_flows_profile"),
                        ], id="leave_approvalflow_results_head_close", style={'display': 'none'}),
                        dbc.Col([
                            dbc.Button("Return", id="leave_btn_approvalflows_results_head_return",
                                       color="primary", block=True, href='/settings/settings_leave_approval_flows'),
                        ], id="leave_approvalflow_results_head_return", style={'display': 'none'}),
                    ], style={'width': '100%'}),
                ]),
            ], id="leave_approvalflow_results_modal"),
            dbc.CardBody([
                dcc.Link('← Back to Leave Approval Flows', href='/settings/settings_leave_approval_flows'),
                html.Br(),
                html.Br(),
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("Leave Approval Flow Name*", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="leave_approvalflow_name", placeholder="Enter Leave Approval Flow Name"
                             ),
                             dbc.FormFeedback("Please enter a valid flow name", valid=False)
                         ],
                            width=8
                        )],
                        row=True
                    ),

                    dbc.FormGroup(
                        [dbc.Label("Leave Approval Flow Code*", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="leave_approvalflow_code", placeholder="Enter Leave Approval Flow Code"
                             ),
                             dbc.FormFeedback("Please enter a valid flow code", valid=False)
                         ],
                             width=8
                         )],
                        row=True
                    ),




                    html.Div([

                        html.Br(),
                        html.Hr(),
                        html.Br(),

                        dbc.FormGroup([
                            dbc.Label("Step No. to Add:", width=2, style={"text-align": "left"}),
                            dbc.Col([
                                dcc.Dropdown(
                                    id='leave_addstep_stepnumbers'
                                ),
                            ], width=1),
                        ], row=True),

                        dbc.FormGroup([
                            dbc.Label("Select Leave Status:", width=2, style={"text-align": "left"}),
                            dbc.Col([
                                dcc.Dropdown(
                                    id='leave_addstep_statuses'
                                ),
                            ], width=4),
                        ], row=True),

                        dbc.Row([
                            dbc.Col([
                                dbc.Button("Add Step", id="leave_approvalflow_addstep_btn",
                                           color="primary", block=False),
                            ]),

                        ], style={'width': '100%'}),

                        html.Br(),
                        html.Br(),

                        dbc.FormGroup([
                             dbc.Label("Step No. to Delete:", width=2, style={"text-align": "left"}),
                             dbc.Col([
                                 dcc.Dropdown(
                                     id='leave_deletestep_stepnumbers'
                                 ),
                             ],width=1),


                        ],row=True),

                        dbc.Row([
                            dbc.Col([
                                dbc.Button("Delete Step", id="leave_btn_deleteflowstep",
                                           color="primary", block=False),
                            ]),

                        ], style={'width': '100%'}),

                        html.Br(),
                        html.Br(),

                        dbc.FormGroup([
                            dbc.Label("Flow to Copy:", width=2, style={"text-align": "left"}),
                            dbc.Col([
                                dcc.Dropdown(
                                    id='leavesflowapproval_copyflowdd'
                                ),
                            ], width=4),

                        ], row=True),

                        dbc.Row([
                            dbc.Col([
                                dbc.Button("Copy Flow", id="leavesflowapproval_copyflowbtn",
                                           color="primary", block=False),
                            ]),

                        ], style={'width': '100%'}),

                    ], id = 'leave_approval_flows_profile_editdiv', style = {'display': 'none'}),

                    html.Br(),
                    html.Br(),

                    html.Div([

                    ], id="leaveflowstepsdt"),

                    html.Div([
                        dcc.Checklist(
                            options=[
                                {'label': ' Mark Entire Leave Approval Flow for Deletion?', 'value': '1'},
                            ], id='leave_approvalflow_chkmarkfordeletion', value=[]
                        ),
                    ], id='leave_div_approvalflow_delete',  style={'text-align': 'middle', 'display': 'inline'}),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save New Leave Approval Flow", id="leave_approvalflow_submit_btn",
                                   color="primary", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="leave_approvalflow_cancel",
                                   href='/settings/settings_leave_approval_flows', color="secondary", className="ml-auto")
                    ]),
                ], style={'width': '100%'}),
                # dbc.Col([
                #
                #     html.Div([
                #         dcc.Input(id='approvalflow_submit_status', type='text', value="0")
                #     ], style={'display': 'none'}),
                #     html.Div([
                #         dcc.Input(id='approvalflow_id', type='text', value="0")
                #     ], style={'display': 'none'}),
                #     dcc.ConfirmDialog(
                #         id='approvalflow_message',
                #     ), ], width=2
                # )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])

@app.callback(
    [
        Output("leave_addstep_stepnumbers", "options"),
        Output("leave_deletestep_stepnumbers", "options")
    ],
    [
        Input("url", "search"),
        Input("leave_approval_flows_profile_sessionproxy", "data")
    ],

)

def leave_stepnumberoptions(
                     url,leave_approval_flows_profile_sessionproxy
):

    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)

    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":

            leave_approval_flow_id = str(parse_qs(parsed.query)['leave_approval_flow_id'][0])

            sql2 = '''
            SELECT MAX(leave_approval_flow_step_number) as step_count
            FROM leave_approval_flow_steps
            WHERE leave_approval_flow_id = %s
            AND leave_approval_flow_step_delete_ind = %s
              '''

            values2 = (leave_approval_flow_id, False)
            columns2 = ['step_count']
            df2 = securequerydatafromdatabase(sql2, values2, columns2)

            if df2["step_count"][0] is not None:
            # if not df2.empty:
                step_count = df2["step_count"][0]
            else:
                step_count = 0

            stepoptions = []
            for i in range(1, step_count+1+1):
                stepoptions.append({'label': i, 'value': i})

            stepoptions2 = []
            for i in range(1, step_count+1):
                stepoptions2.append({'label': i, 'value': i})


            values = [stepoptions, stepoptions2]
            return values
        elif parse_qs(parsed.query)['mode'][0] == "add":
            values = [[], []]
            return values
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('leave_approvalflow_name', 'value'),
        Output('leave_approvalflow_code', 'value'),
        Output("leave_approvalflow_process_editmodalhead", "children"),
        Output("leave_approvalflow_submit_btn", "children"),
        Output("leave_approvalflow_chkmarkfordeletion", "value"),
        Output("leave_div_approvalflow_delete", "style"),
        # Output("addstep_stepnumbers", "options"),
        # Output("deletestep_stepnumbers", "options")

        # Output('approvalflow_city', 'options'),
    ],
    [
        # Input('approvalflow_submit_status', 'value'),
        # Input('btn_approvalflow_head_close', 'n_clicks'),
        Input("url", "search"),
    ],
    [
        State('leave_approvalflow_name', 'value'),
        State('leave_approvalflow_code', 'value'),
        State('leave_approvalflow_process_editmodalhead', "children"),
        State("leave_approvalflow_submit_btn", "children"),
        State("leave_approvalflow_chkmarkfordeletion", "value"),
    ]

)
def leave_returnapprovalflowdata(
                     url,
                     leave_approvalflow_name, leave_approvalflow_code,
                     leave_approvalflow_process_editmodalhead, leave_approvalflow_submit_btn,
                     leave_approvalflow_chkmarkfordeletion):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)

    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":
            leave_approval_flow_id = str(parse_qs(parsed.query)['leave_approval_flow_id'][0])
            sql = '''
                        SELECT leave_approval_flow_name, leave_approval_flow_code
                        FROM leave_approval_flows
                        WHERE leave_approval_flow_id = %s
                        AND leave_approval_flow_delete_ind = %s
                  '''
            values = (leave_approval_flow_id, False)
            columns = ['leave_approval_flow_name', 'leave_approval_flow_code']
            df = securequerydatafromdatabase(sql, values, columns)
            leave_approval_flow_name = df["leave_approval_flow_name"][0]
            leave_approval_flow_code = df["leave_approval_flow_code"][0]


            values = [leave_approval_flow_name, leave_approval_flow_code,
                      "Edit Existing Approval Flow",
                      "Save Changes", [], {'text-align': 'middle', 'display': 'inline'}]
            return values
        elif parse_qs(parsed.query)['mode'][0] == "add":
            values = ["", "", leave_approvalflow_process_editmodalhead,
                      leave_approvalflow_submit_btn, [], {'display': 'none'}]
            return values
    else:
        raise PreventUpdate


@ app.callback(
    [
        Output("leave_approvalflow_name", "valid"),
        Output("leave_approvalflow_name", "invalid"),
        # Output("approvalflow_city", "valid"),
        # Output("approvalflow_city", "invalid"),
        Output("leave_approvalflow_code", "valid"),
        Output("leave_approvalflow_code", "invalid"),

        Output('leave_approvalflow_results_modal', "is_open"),
        Output('leave_approvalflow_results_body', "children"),
        Output('leave_approvalflow_results_head_close', "style"),
        Output('leave_approvalflow_results_head_return', "style"),
    ],
    [
        Input('leave_approvalflow_submit_btn', 'n_clicks'),
        Input('leave_btn_approvalflow_head_close', 'n_clicks'),
        Input('leave_btn_approvalflows_results_head_return', 'n_clicks'),
    ],
    [
        State('current_user_id', 'data'),
        State('leave_approvalflow_name', 'value'),
        # State('approvalflow_province', 'value'),
        State("leave_approvalflow_code", "value"),

        State("leave_approvalflow_submit_btn", "children"),
        State("leave_approvalflow_chkmarkfordeletion", "value"),
        State("url", "search"),

    ]

)
def leave_approvalvalidity(leave_approvalflow_submit_btn, leave_btn_approvalflow_head_close, leave_btn_approvalflows_results_head_return,
                current_user_id,
                leave_approvalflow_name,  # approvalflow_province,
                leave_approvalflow_code,
                mode, leave_approvalflow_chkmarkfordeletion, url):
    ctx = dash.callback_context
    stylehead_close = {'display': 'none'}
    stylehead_return = {'display': 'none'}
    parsed = urlparse.urlparse(url)

    if ctx.triggered:
        validity = [
            False, False, False, False,
        ]
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'leave_approvalflow_submit_btn':
            if leave_approvalflow_name:
                is_valid_leave_approvalflow_name = True
            else:
                is_valid_leave_approvalflow_name = False

            if leave_approvalflow_code:
                is_valid_leave_approvalflow_code = True
            else:
                is_valid_leave_approvalflow_code = False

            validity = [
                is_valid_leave_approvalflow_name, not is_valid_leave_approvalflow_name,
                is_valid_leave_approvalflow_code, not is_valid_leave_approvalflow_code,
            ]
            allvalid = [is_valid_leave_approvalflow_name,
                        is_valid_leave_approvalflow_code]

            if all(allvalid):
                if mode == "Save New Leave Approval Flow":
                    sql = """
                        INSERT INTO leave_approval_flows (leave_approval_flow_name, leave_approval_flow_code, leave_approval_flow_inserted_by, leave_approval_flow_inserted_on, leave_approval_flow_delete_ind)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING leave_approval_flow_id

                    """
                    values = (leave_approvalflow_name, leave_approvalflow_code,
                              current_user_id, datetime.now(), False)

                    leave_approval_flow_id = modifydatabasereturnid(sql, values)

                    #auto insert
                    #####

                    sql = """
                        INSERT INTO leave_approval_flow_steps (leave_approval_flow_id, leave_approval_flow_step_number, leave_status_id,
                        leave_approval_flow_step_inserted_by, leave_approval_flow_step_inserted_on, leave_approval_flow_step_delete_ind)
                        VALUES (%s, %s, %s, %s, %s, %s)

                    """
                    values = (leave_approval_flow_id, 1, 7,
                              current_user_id, datetime.now(), False)

                    modifydatabase(sql, values)


                    #####
                    #####

                    sql = """
                        INSERT INTO leave_approval_flow_steps (leave_approval_flow_id, leave_approval_flow_step_number, leave_status_id,
                        leave_approval_flow_step_inserted_by, leave_approval_flow_step_inserted_on, leave_approval_flow_step_delete_ind)
                        VALUES (%s, %s, %s, %s, %s, %s)

                    """
                    values = (leave_approval_flow_id, 2, 8,
                              current_user_id, datetime.now(), False)

                    modifydatabase(sql, values)


                    #####
                    #####

                    sql = """
                        INSERT INTO leave_approval_flow_steps (leave_approval_flow_id, leave_approval_flow_step_number, leave_status_id,
                        leave_approval_flow_step_inserted_by, leave_approval_flow_step_inserted_on, leave_approval_flow_step_delete_ind)
                        VALUES (%s, %s, %s, %s, %s, %s)

                    """
                    values = (leave_approval_flow_id, 3, 9,
                              current_user_id, datetime.now(), False)

                    modifydatabase(sql, values)


                    #####

                    sql = """
                        INSERT INTO leave_approval_flow_steps (leave_approval_flow_id, leave_approval_flow_step_number, leave_status_id,
                        leave_approval_flow_step_inserted_by, leave_approval_flow_step_inserted_on, leave_approval_flow_step_delete_ind)
                        VALUES (%s, %s, %s, %s, %s, %s)

                    """
                    values = (leave_approval_flow_id, 4, 2,
                              current_user_id, datetime.now(), False)

                    modifydatabase(sql, values)


                    #####



                    displayed = True
                    message = "Successfully added new Leave approval flow"
                    status = "1"
                    stylehead_close = {'display': 'none'}
                    stylehead_return = {'display': 'inline'}

                else:

                    parsed = urlparse.urlparse(url)
                    leave_approval_flow_id = int(parse_qs(parsed.query)['leave_approval_flow_id'][0])

                    sql = """
                        UPDATE leave_approval_flows SET leave_approval_flow_name = %s, leave_approval_flow_code = %s, leave_approval_flow_inserted_by = %s,
                            leave_approval_flow_inserted_on = %s, leave_approval_flow_delete_ind = %s
                             WHERE leave_approval_flow_id = %s
                    """
                    if '1' in leave_approvalflow_chkmarkfordeletion:
                        fordelete = True
                    else:
                        fordelete = False
                    values = (leave_approvalflow_name, leave_approvalflow_code,
                              current_user_id, datetime.now(), fordelete, leave_approval_flow_id)
                    modifydatabase(sql, values)
                    validity = [
                        False, False, False, False,
                    ]
                    stylehead_close = {'display': 'none'}
                    stylehead_return = {'display': 'inline'}
                    displayed = True
                    message = "Successfully edited Leave approval flow information"
                    status = "1"
            else:
                status = "2"
                displayed = True
                message = "Please review input data"
                stylehead_close = {'display': 'inline'}
                stylehead_return = {'display': 'none'}
            out = [displayed, message, stylehead_close, stylehead_return]
            out = validity+out
            return out
        elif eventid == 'leave_btn_approvalflow_head_close':
            status = "0"
            displayed = False
            message = "Please review input data"
            stylehead_close = {'display': 'inline'}
            stylehead_return = {'display': 'none'}
            out = [displayed, message, stylehead_close, stylehead_return]
            out = validity+out
            return out
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
#

@app.callback(
    [
        Output('leaveflowstepsdt', 'children')
    ],
    [
        Input('url', 'search'),
        Input('leave_approval_flows_profile_sessionproxy', 'data'),
        Input('leave_btn_deleteflowstep', 'n_clicks')

    ]

)

def leave_flowloadstepsdt(url,
                leave_approvalflow_addstep_btn,
                leave_btn_deleteflowstep
                ):

    parsed = urlparse.urlparse(url)
    if parse_qs(parsed.query):
        mode = str(parse_qs(parsed.query)['mode'][0])
        if mode == "edit":
            leave_approval_flow_id = str(parse_qs(parsed.query)['leave_approval_flow_id'][0])



            sql1 = '''
                    SELECT afs.leave_approval_flow_step_number, bs.leave_status_name
                    FROM leave_approval_flow_steps afs
                    INNER JOIN leave_statuses bs ON bs.leave_status_id = afs.leave_status_id
                    WHERE leave_approval_flow_step_delete_ind = %s
                    AND afs.leave_approval_flow_id = %s
                    ORDER BY leave_approval_flow_step_number ASC
                        '''

            values1 = (False, leave_approval_flow_id, )
            columns1 = ['leave_approval_flow_step_number', 'leave_status_name']
            df = securequerydatafromdatabase(sql1, values1, columns1)
            df.columns = ['Step No.', 'Leave Status']


            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

            return [table]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback([

    Output('leave_addstep_statuses', 'options'),
    Output('leavesflowapproval_copyflowdd', 'options')

],
    [
    Input('url', 'search'),
],

)

def leave_statusfillindropdowns(url):
    parsed = urlparse.urlparse(url)

    if parse_qs(parsed.query):
        mode = str(parse_qs(parsed.query)['mode'][0])
        if mode == "edit":

            leave_approval_flow_id = str(parse_qs(parsed.query)['leave_approval_flow_id'][0])

            leave_addstep_statuses = commonmodules.queryfordropdown('''
                        SELECT leave_status_name as label, leave_status_id as value
                        FROM leave_statuses
                        WHERE leave_status_delete_ind = %s
                        AND leave_status_id NOT IN %s



                   ''', (False,(1, 3, 18, 19, 20, 21)))

            copyflow_options = commonmodules.queryfordropdown('''

                        SELECT leave_approval_flow_name as label, leave_approval_flow_id as value
                        FROM leave_approval_flows
                        WHERE leave_approval_flow_delete_ind = %s

                   ''', (False,))



            return [leave_addstep_statuses, copyflow_options]
        else:
            raise PreventUpdate

    else:
        raise PreventUpdate

@app.callback(
    [
        Output('leave_approval_flows_profile_editdiv', 'style')
    ],
    [
        Input('url', 'search')
    ]

)

def leave_showeditdiv(url):

    parsed = urlparse.urlparse(url)
    if parse_qs(parsed.query):
        mode = str(parse_qs(parsed.query)['mode'][0])
        if mode == "edit":
            returnstyle = {'display':'inline'}

        else:
            returnstyle = {'display': 'none'}
        return [returnstyle]

    else:
        raise PreventUpdate

@app.callback(
    [
        Output('leave_approval_flows_profile_sessionproxy', 'data')

    ],
    [
        Input('leave_approvalflow_addstep_btn', 'n_clicks'),
        Input('leave_btn_deleteflowstep', 'n_clicks'),
        Input('leavesflowapproval_copyflowbtn', 'n_clicks'),


    ],
    [
        State('leave_addstep_stepnumbers', 'value'),
        State('leave_addstep_statuses', 'value'),
        State('leave_deletestep_stepnumbers', 'value'),
        State('url', 'search'),
        State('current_user_id', 'data'),
        State('leavesflowapproval_copyflowdd', 'value')


    ]

)

def leave_flowexecutestepmods(leave_approvalflow_addstep_btn, leave_btn_deleteflowstep, leavesflowapproval_copyflowbtn,
                    leave_addstep_stepnumbers, leave_addstep_statuses, leave_deletestep_stepnumbers, url, current_user_id, leavesflowapproval_copyflowdd):

    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parse_qs(parsed.query):
        # approval_flow_id = parse_qs(parsed.query)['approval_flow_id'][0]
        if ctx.triggered:
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]
            if eventid == 'leave_approvalflow_addstep_btn':
                leave_approval_flow_id = parse_qs(parsed.query)['leave_approval_flow_id'][0]
                sqlupdate = '''
                    UPDATE leave_approval_flow_steps
                    SET leave_approval_flow_step_number = leave_approval_flow_step_number + 1
                    WHERE leave_approval_flow_id = %s
                    AND leave_approval_flow_step_number >= %s
                    AND leave_approval_flow_step_delete_ind = %s

                '''
                values = (leave_approval_flow_id, leave_addstep_stepnumbers, False)
                modifydatabase(sqlupdate, values)

                # sql1 = '''
                #         SELECT bs.bp_status_id
                #         FROM bp_statuses bs
                #         INNER JOIN bp_status_roles bsr ON bsr.bp_status_id = bs.bp_status_id
                #         WHERE role_id = %s
                #         AND bs.bp_status_delete_ind = %s
                #         AND bp_status_role_delete_ind = %s
                # '''
                #
                # values1 = (addstep_statuses, False, False)
                # columns1 = ['bp_status_id']
                # df1 = securequerydatafromdatabase(sql1, values1, columns1)
                # bp_status_id = int(df1["bp_status_id"][0])

                leave_addstep_statuses

                sqlupdate2 = '''
                INSERT INTO leave_approval_flow_steps(
                    leave_approval_flow_id, leave_approval_flow_step_number, leave_status_id, leave_approval_flow_step_inserted_by, leave_approval_flow_step_inserted_on,
                    leave_approval_flow_step_delete_ind)
                    VALUES (%s, %s, %s, %s, %s, %s);
                '''
                values2 = (leave_approval_flow_id, leave_addstep_stepnumbers, leave_addstep_statuses, current_user_id, datetime.now(), False)
                modifydatabase(sqlupdate2, values2)

            elif eventid == 'leave_btn_deleteflowstep':
                leave_approval_flow_id = parse_qs(parsed.query)['leave_approval_flow_id'][0]
                sqlupdate = '''
                    UPDATE leave_approval_flow_steps
                    SET leave_approval_flow_step_delete_ind = %s
                    WHERE leave_approval_flow_id = %s
                    AND leave_approval_flow_step_number = %s

                '''
                values = (True, leave_approval_flow_id, leave_deletestep_stepnumbers)
                modifydatabase(sqlupdate, values)

                sqlupdate2 = '''
                                UPDATE leave_approval_flow_steps
                                SET leave_approval_flow_step_number = leave_approval_flow_step_number - 1
                                WHERE leave_approval_flow_step_number > %s
                                AND leave_approval_flow_id = %s
                                AND leave_approval_flow_step_delete_ind = %s

                            '''

                values2 = (leave_deletestep_stepnumbers, leave_approval_flow_id, False)
                modifydatabase(sqlupdate2, values2)

            elif eventid == 'leavesflowapproval_copyflowbtn':
                leave_approval_flow_id = parse_qs(parsed.query)['leave_approval_flow_id'][0]
                sqlupdate2 = '''
                        UPDATE leave_approval_flow_steps
                        SET leave_approval_flow_step_delete_ind = %s
                        WHERE leave_approval_flow_id = %s
                    '''
                values2 = (True, leave_approval_flow_id)
                modifydatabase(sqlupdate2, values2)

                sql1 = '''
                    SELECT leave_approval_flow_step_number, leave_status_id
                    FROM leave_approval_flow_steps
                    WHERE leave_approval_flow_step_delete_ind = %s
                    AND leave_approval_flow_id = %s
                    ORDER BY leave_approval_flow_step_number ASC
                        '''

                values1 = (False, leavesflowapproval_copyflowdd)
                columns1 = ['leave_approval_flow_step_number', 'leave_status_id']

                df = securequerydatafromdatabase(sql1, values1, columns1)

                df_list = df.values.tolist()


                for i in df_list:

                    sql = """
                    INSERT INTO leave_approval_flow_steps (leave_approval_flow_id, leave_approval_flow_step_number, leave_status_id,
                    leave_approval_flow_step_inserted_by, leave_approval_flow_step_inserted_on, leave_approval_flow_step_delete_ind)
                    VALUES (%s, %s, %s, %s, %s, %s)

                """
                    values = (leave_approval_flow_id, i[0], i[1], current_user_id, datetime.now(), False)

                    modifydatabase(sql, values)


            return [[1]]

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
