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

    dcc.Store(id='bp_approval_flows_profile_sessionproxy', storage_type='session'),

    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Add New Basic Paper Approval Flow", id="approvalflow_process_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.Modal([
                dbc.ModalHeader("Process BP Approval Flows", id="approvalflows_results_head"),
                dbc.ModalBody([
                ], id="approvalflow_results_body"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Close", id="btn_approvalflow_head_close",
                                       color="primary", block=True, href = "/settings/settings_bp_approval_flows_profile"),
                        ], id="approvalflow_results_head_close", style={'display': 'none'}),
                        dbc.Col([
                            dbc.Button("Return", id="btn_approvalflows_results_head_return",
                                       color="primary", block=True, href='/settings/settings_bp_approval_flows'),
                        ], id="approvalflow_results_head_return", style={'display': 'none'}),
                    ], style={'width': '100%'}),
                ]),
            ], id="approvalflow_results_modal"),
            dbc.CardBody([
                dcc.Link('← Back to BP Approval Flows', href='/settings/settings_bp_approval_flows'),
                html.Br(),
                html.Br(),
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("Approval Flow Name*", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="approvalflow_name", placeholder="Enter Approval Flow Name"
                             ),
                             dbc.FormFeedback("Please enter a valid flow name", valid=False)
                         ],
                            width=8
                        )],
                        row=True
                    ),

                    dbc.FormGroup(
                        [dbc.Label("Approval Flow Code*", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="approvalflow_code", placeholder="Enter Approval Flow Code"
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
                                    id='addstep_stepnumbers'
                                ),
                            ], width=1),
                        ], row=True),

                        dbc.FormGroup([
                            dbc.Label("Select BP Status:", width=2, style={"text-align": "left"}),
                            dbc.Col([
                                dcc.Dropdown(
                                    id='addstep_statuses'
                                ),
                            ], width=4),
                        ], row=True),

                        dbc.Row([
                            dbc.Col([
                                dbc.Button("Add Step", id="approvalflow_addstep_btn",
                                           color="primary", block=False),
                            ]),

                        ], style={'width': '100%'}),

                        html.Br(),
                        html.Br(),

                        dbc.FormGroup([
                             dbc.Label("Step No. to Delete:", width=2, style={"text-align": "left"}),
                             dbc.Col([
                                 dcc.Dropdown(
                                     id='deletestep_stepnumbers'
                                 ),
                             ],width=1),


                        ],row=True),

                        dbc.Row([
                            dbc.Col([
                                dbc.Button("Delete Step", id="btn_deleteflowstep",
                                           color="primary", block=False),
                            ]),

                        ], style={'width': '100%'}),

                        html.Br(),
                        html.Br(),

                        dbc.FormGroup([
                            dbc.Label("Flow to Copy:", width=2, style={"text-align": "left"}),
                            dbc.Col([
                                dcc.Dropdown(
                                    id='flowapproval_copyflowdd'
                                ),
                            ], width=4),

                        ], row=True),

                        dbc.Row([
                            dbc.Col([
                                dbc.Button("Copy Flow", id="flowapproval_copyflowbtn",
                                           color="primary", block=False),
                            ]),

                        ], style={'width': '100%'}),

                    ], id = 'approval_flows_profile_editdiv', style = {'display': 'none'}),

                    html.Br(),
                    html.Br(),

                    html.Div([

                    ], id="bpflowstepsdt"),

                    html.Div([
                        dcc.Checklist(
                            options=[
                                {'label': 'Mark Entire BP Approval Flow for Deletion?', 'value': '1'},
                            ], id='approvalflow_chkmarkfordeletion', value=[]
                        ),
                    ], id='div_approvalflow_delete',  style={'text-align': 'middle', 'display': 'inline'}),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save New BP Approval Flow", id="approvalflow_submit_btn",
                                   color="primary", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="approvalflow_cancel",
                                   href='/settings/settings_bp_approval_flows', color="secondary", className="ml-auto")
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
        Output("addstep_stepnumbers", "options"),
        Output("deletestep_stepnumbers", "options")
    ],
    [
        Input("url", "search"),
        Input("bp_approval_flows_profile_sessionproxy", "data")
    ],

)

def returnapprovalflowdata2(
                     url,bp_approval_flows_profile_sessionproxy
):

    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)

    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":

            approval_flow_id = str(parse_qs(parsed.query)['approval_flow_id'][0])

            sql2 = '''
            SELECT MAX(approval_flow_step_number) as step_count
            FROM bp_approval_flow_steps
            WHERE approval_flow_id = %s
            AND approval_flow_step_delete_ind = %s
              '''

            values2 = (approval_flow_id, False)
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
        Output('approvalflow_name', 'value'),
        Output('approvalflow_code', 'value'),
        Output("approvalflow_process_editmodalhead", "children"),
        Output("approvalflow_submit_btn", "children"),
        Output("approvalflow_chkmarkfordeletion", "value"),
        Output("div_approvalflow_delete", "style"),
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
        State('approvalflow_name', 'value'),
        State('approvalflow_code', 'value'),
        State('approvalflow_process_editmodalhead', "children"),
        State("approvalflow_submit_btn", "children"),
        State("approvalflow_chkmarkfordeletion", "value"),
    ]

)
def returnapprovalflowdata(
                     url,
                     approvalflow_name, approvalflow_code,
                     approvalflow_process_editmodalhead, approvalflow_submit_btn,
                     approvalflow_chkmarkfordeletion):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)

    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":
            approval_flow_id = str(parse_qs(parsed.query)['approval_flow_id'][0])
            sql = '''
                        SELECT approval_flow_name, approval_flow_code
                        FROM bp_approval_flows
                        WHERE approval_flow_id = %s
                        AND approval_flow_delete_ind = %s
                  '''
            values = (approval_flow_id, False)
            columns = ['approval_flow_name', 'approval_flow_code']
            df = securequerydatafromdatabase(sql, values, columns)
            approval_flow_name = df["approval_flow_name"][0]
            approval_flow_code = df["approval_flow_code"][0]


            values = [approval_flow_name, approval_flow_code,
                      "Edit Existing Approval Flow",
                      "Save Changes", [], {'text-align': 'middle', 'display': 'inline'}]
            return values
        elif parse_qs(parsed.query)['mode'][0] == "add":
            values = ["", "", approvalflow_process_editmodalhead,
                      approvalflow_submit_btn, [], {'display': 'none'}]
            return values
    else:
        raise PreventUpdate


@ app.callback(
    [
        Output("approvalflow_name", "valid"),
        Output("approvalflow_name", "invalid"),
        # Output("approvalflow_city", "valid"),
        # Output("approvalflow_city", "invalid"),
        Output("approvalflow_code", "valid"),
        Output("approvalflow_code", "invalid"),

        Output('approvalflow_results_modal', "is_open"),
        Output('approvalflow_results_body', "children"),
        Output('approvalflow_results_head_close', "style"),
        Output('approvalflow_results_head_return', "style"),
    ],
    [
        Input('approvalflow_submit_btn', 'n_clicks'),
        Input('btn_approvalflow_head_close', 'n_clicks'),
        Input('btn_approvalflows_results_head_return', 'n_clicks'),
    ],
    [
        State('current_user_id', 'data'),
        State('approvalflow_name', 'value'),
        # State('approvalflow_province', 'value'),
        State("approvalflow_code", "value"),

        State("approvalflow_submit_btn", "children"),
        State("approvalflow_chkmarkfordeletion", "value"),
        State("url", "search"),

    ]

)
def processdata(approvalflow_submit_btn, btn_approvalflow_head_close, btn_approvalflows_results_head_return,
                current_user_id,
                approvalflow_name,  # approvalflow_province,
                approvalflow_code,
                mode, approvalflow_chkmarkfordeletion, url):
    ctx = dash.callback_context
    stylehead_close = {'display': 'none'}
    stylehead_return = {'display': 'none'}
    parsed = urlparse.urlparse(url)

    if ctx.triggered:
        validity = [
            False, False, False, False,
        ]
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'approvalflow_submit_btn':
            if approvalflow_name:
                is_valid_approvalflow_name = True
            else:
                is_valid_approvalflow_name = False

            if approvalflow_code:
                is_valid_approvalflow_code = True
            else:
                is_valid_approvalflow_code = False

            validity = [
                is_valid_approvalflow_name, not is_valid_approvalflow_name,
                is_valid_approvalflow_code, not is_valid_approvalflow_code,
            ]
            allvalid = [is_valid_approvalflow_name,
                        is_valid_approvalflow_code]

            if all(allvalid):
                if mode == "Save New BP Approval Flow":
                    sql = """
                        INSERT INTO bp_approval_flows (approval_flow_name, approval_flow_code, approval_flow_inserted_by, approval_flow_inserted_on, approval_flow_delete_ind)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING approval_flow_id

                    """
                    values = (approvalflow_name, approvalflow_code,
                              current_user_id, datetime.now(), False)

                    approval_flow_id = modifydatabasereturnid(sql, values)

                    #####

                    sql = """
                        INSERT INTO bp_approval_flow_steps (approval_flow_id, approval_flow_step_number, bp_status_id,
                        approval_flow_step_inserted_by, approval_flow_step_inserted_on, approval_flow_step_delete_ind)
                        VALUES (%s, %s, %s, %s, %s, %s)

                    """
                    values = (approval_flow_id, 1, 26,
                              current_user_id, datetime.now(), False)

                    modifydatabase(sql, values)


                    #####



                    displayed = True
                    message = "Successfully added new BP approval flow"
                    status = "1"
                    stylehead_close = {'display': 'none'}
                    stylehead_return = {'display': 'inline'}

                else:

                    parsed = urlparse.urlparse(url)
                    approval_flow_id = int(parse_qs(parsed.query)['approval_flow_id'][0])

                    sql = """
                        UPDATE bp_approval_flows SET approval_flow_name = %s, approval_flow_code = %s, approval_flow_inserted_by = %s,
                            approval_flow_inserted_on = %s, approval_flow_delete_ind = %s
                             WHERE approval_flow_id = %s
                    """
                    if '1' in approvalflow_chkmarkfordeletion:
                        fordelete = True
                    else:
                        fordelete = False
                    values = (approvalflow_name, approvalflow_code,
                              current_user_id, datetime.now(), fordelete, approval_flow_id)
                    modifydatabase(sql, values)
                    validity = [
                        False, False, False, False,
                    ]
                    stylehead_close = {'display': 'none'}
                    stylehead_return = {'display': 'inline'}
                    displayed = True
                    message = "Successfully edited BP approval flow information"
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
        elif eventid == 'btn_approvalflow_head_close':
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
        Output('bpflowstepsdt', 'children')
    ],
    [
        Input('url', 'search'),
        Input('bp_approval_flows_profile_sessionproxy', 'data'),
        Input('btn_deleteflowstep', 'n_clicks')

    ]

)

def loadstepsdt(url,
                approvalflow_addstep_btn,
                btn_deleteflowstep
                ):

    parsed = urlparse.urlparse(url)
    if parse_qs(parsed.query):
        mode = str(parse_qs(parsed.query)['mode'][0])
        if mode == "edit":
            approval_flow_id = str(parse_qs(parsed.query)['approval_flow_id'][0])



            sql1 = '''
                    SELECT afs.approval_flow_step_number, bs.bp_status_name
                    FROM bp_approval_flow_steps afs
                    INNER JOIN bp_statuses bs ON bs.bp_status_id = afs.bp_status_id
                    WHERE approval_flow_step_delete_ind = %s
                    AND afs.approval_flow_id = %s
                    ORDER BY approval_flow_step_number ASC
                        '''

            values1 = (False, approval_flow_id, )
            columns1 = ['approval_flow_step_number', 'bp_status_name']
            df = securequerydatafromdatabase(sql1, values1, columns1)
            df.columns = ['Step No.', 'BP Status']


            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

            return [table]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback([

    Output('addstep_statuses', 'options'),
    Output('flowapproval_copyflowdd', 'options')

],
    [
    Input('url', 'search'),
],

)

def fillindropdowns(url):
    parsed = urlparse.urlparse(url)

    if parse_qs(parsed.query):
        mode = str(parse_qs(parsed.query)['mode'][0])
        if mode == "edit":

            approval_flow_id = str(parse_qs(parsed.query)['approval_flow_id'][0])
            addstep_statuses = commonmodules.queryfordropdown('''
                        SELECT bp_status_name as label, bp_status_id as value
                        FROM bp_statuses
                        WHERE bp_status_delete_ind = %s
                        AND bp_status_id NOT IN %s
                   ''', (False,(1, 20, 27, 28, 29, 34)))


            copyflow_options = commonmodules.queryfordropdown('''

                        SELECT approval_flow_name as label, approval_flow_id as value
                        FROM bp_approval_flows
                        WHERE approval_flow_delete_ind = %s

                   ''', (False,))

            return [addstep_statuses, copyflow_options]
        else:
            raise PreventUpdate

    else:
        raise PreventUpdate

@app.callback(
    [
        Output('approval_flows_profile_editdiv', 'style')
    ],
    [
        Input('url', 'search')
    ]

)

def showeditdiv(url):

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
        Output('bp_approval_flows_profile_sessionproxy', 'data')

    ],
    [
        Input('approvalflow_addstep_btn', 'n_clicks'),
        Input('btn_deleteflowstep', 'n_clicks'),
        Input('flowapproval_copyflowbtn', 'n_clicks')

    ],
    [
        State('addstep_stepnumbers', 'value'),
        State('addstep_statuses', 'value'),
        State('deletestep_stepnumbers', 'value'),
        State('url', 'search'),
        State('current_user_id', 'data'),
        State('flowapproval_copyflowdd', 'value')


    ]

)

def executestepmods(approvalflow_addstep_btn, btn_deleteflowstep, flowapproval_copyflowbtnm,
                    addstep_stepnumbers, addstep_statuses, deletestep_stepnumbers, url, current_user_id, flowapproval_copyflowdd):

    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parse_qs(parsed.query):
        # approval_flow_id = parse_qs(parsed.query)['approval_flow_id'][0]
        if ctx.triggered:
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]
            if eventid == 'approvalflow_addstep_btn':
                approval_flow_id = parse_qs(parsed.query)['approval_flow_id'][0]
                sqlupdate = '''
                    UPDATE bp_approval_flow_steps
                    SET approval_flow_step_number = approval_flow_step_number + 1
                    WHERE approval_flow_id = %s
                    AND approval_flow_step_number >= %s
                    AND approval_flow_step_delete_ind = %s

                '''
                values = (approval_flow_id, addstep_stepnumbers, False)
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

                addstep_statuses

                sqlupdate2 = '''
                INSERT INTO bp_approval_flow_steps(
                    approval_flow_id, approval_flow_step_number, bp_status_id, approval_flow_step_inserted_by, approval_flow_step_inserted_on,
                    approval_flow_step_delete_ind)
                    VALUES (%s, %s, %s, %s, %s, %s);
                '''
                values2 = (approval_flow_id, addstep_stepnumbers, addstep_statuses, current_user_id, datetime.now(), False)
                modifydatabase(sqlupdate2, values2)

            elif eventid == 'btn_deleteflowstep':
                approval_flow_id = parse_qs(parsed.query)['approval_flow_id'][0]
                sqlupdate = '''
                    UPDATE bp_approval_flow_steps
                    SET approval_flow_step_delete_ind = %s
                    WHERE approval_flow_id = %s
                    AND approval_flow_step_number = %s

                '''
                values = (True, approval_flow_id, deletestep_stepnumbers)
                modifydatabase(sqlupdate, values)

                sqlupdate2 = '''
                                UPDATE bp_approval_flow_steps
                                SET approval_flow_step_number = approval_flow_step_number - 1
                                WHERE approval_flow_step_number > %s
                                AND approval_flow_id = %s
                                AND approval_flow_step_delete_ind = %s

                            '''

                values2 = (deletestep_stepnumbers, approval_flow_id, False)
                modifydatabase(sqlupdate2, values2)

            elif eventid == 'flowapproval_copyflowbtn':
                approval_flow_id = parse_qs(parsed.query)['approval_flow_id'][0]
                sqlupdate2 = '''
                                UPDATE bp_approval_flow_steps
                                SET approval_flow_step_delete_ind = %s
                                WHERE approval_flow_id = %s
                            '''
                values2 = (True, approval_flow_id)
                modifydatabase(sqlupdate2, values2)

                sql1 = '''
					SELECT approval_flow_step_number, bp_status_id
					FROM bp_approval_flow_steps
					WHERE approval_flow_step_delete_ind = %s
					AND approval_flow_id = %s
					ORDER BY approval_flow_step_number ASC
                        '''

                values1 = (False, flowapproval_copyflowdd)
                columns1 = ['approval_flow_step_number', 'bp_status_id']

                df = securequerydatafromdatabase(sql1, values1, columns1)

                df_list = df.values.tolist()


                for i in df_list:


                    sql = """
                        INSERT INTO bp_approval_flow_steps (approval_flow_id, approval_flow_step_number, bp_status_id,
                        approval_flow_step_inserted_by, approval_flow_step_inserted_on, approval_flow_step_delete_ind)
                        VALUES (%s, %s, %s, %s, %s, %s)

                    """
                    values = (approval_flow_id, i[0], i[1], current_user_id, datetime.now(), False)

                    modifydatabase(sql, values)

            return [[1]]

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
