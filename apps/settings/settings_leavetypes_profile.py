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
    html.H1("Leave Types"),
    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Add New Leave Type", id="leavetype_process_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.Modal([
                dbc.ModalHeader("Process Leave Types", id="leavetype_results_head"),
                dbc.ModalBody([
                ], id="leavetype_results_body"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Close", id="btn_leavetype_head_close",
                                       color="primary", block=True),
                        ], id="leavetype_results_head_close", style={'display': 'none'}),
                        dbc.Col([
                            dbc.Button("Return", id="btn_leavetype_results_head_return",
                                       color="primary", block=True, href='/settings/settings_leavetypes'),
                        ], id="leavetype_results_head_return", style={'display': 'none'}),
                    ], style={'width': '100%'}),
                ]),
            ], id="leavetype_results_modal"),
            dbc.CardBody([
                dcc.Link('← Back to Leave Types', href='/settings/settings_leavetypes'),
                html.Br(),
                html.Br(),
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("Leave Type Name", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="leavetype_name", placeholder="Enter Leave Type Name"
                             ),
                             dbc.FormFeedback("Too short or already taken", valid=False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Leave Type Code", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="leavetype_code", placeholder="Enter Leave Type Code"
                             ),
                             #dbc.FormFeedback("Too short or already taken", valid = False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Leave Category", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dcc.Dropdown(
                                 id="leavetype_categ_id",
                                 options=[
                                    {'label': 'Personal Leave', 'value': 1},
                                    {'label': 'Offical Leave', 'value': 2},
                                    {'label': 'Others', 'value': 3},

                                 ],
                                 searchable=False
                             ),
                             #dbc.FormFeedback("Too short or already taken", valid = False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Available to", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dcc.Dropdown(
                                 id="leavetype_available",
                                 options=[
                                    {'label': 'Faculty (Full-Time)', 'value': 1},
                                    {'label': 'Faculty (Administrator)', 'value': 4}, #2
                                    {'label': 'Admin', 'value': 2},#3
                                    {'label': 'REPS', 'value': 3},#4
                                    {'label': 'None', 'value': 5},#5

                                 ],
                                 searchable=False,
                                 multi=True
                             ),
                             #dbc.FormFeedback("Too short or already taken", valid = False)
                         ],
                            width=8
                        )],
                        row=True
                    ),

                    dbc.FormGroup(
                        [dbc.Label("Leave Classification:", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dcc.Dropdown(
                                 id="leavetype_class",
                                 options=[
                                    {'label': 'Deduct From Vacation Leave (VL) Credits', 'value': 1},
                                    {'label': 'Deduct From Sick Leave (SL) Credits', 'value': 2},#3
                                    {'label': 'None', 'value': 3},#3

                                 ],
                                 searchable=False,

                             ),
                             #dbc.FormFeedback("Too short or already taken", valid = False)
                             dbc.FormText("The # of days availed will be directly deducted from the credits of the selected classification.")
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Leave Inclusivity:", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dcc.Dropdown(
                                 id="leave_type_inclusivity_id",
                                 options=[
                                    {'label': 'Always Inclusive', 'value': 1},
                                    {'label': 'Always Exclusive', 'value': 2},#3
                                    {'label': 'Can be INCL/EXCL', 'value': 3},#3

                                 ],
                                 searchable=True,

                             ),
                             #dbc.FormFeedback("Too short or already taken", valid = False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Excess Leave will become:", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dcc.Dropdown(
                                 id="leave_type_excess_will_be_id",
                                 options=[
                                 {'label': 'Vacation Leave with pay', 'value': 1},
                                 {'label': 'Sick Leave with pay', 'value': 2},#3
                                 {'label': 'Vacation Leave without pay', 'value': 3},#3
                                 {'label': 'Sick Leave without pay', 'value': 4},#3
                                 # {'label': 'None', 'value': 5},#3

                                 ],
                                 searchable=True,
                                 multi=True

                             ),
                             dbc.FormText("Choose the leave type in order of charging.")
                         ],
                            width=8
                        )],
                        row=True,
                        style = {'display':'none'}
                    ),


                    dbc.FormGroup(
                        dbc.Row([
                                dbc.Label(html.Div("Make inactive", id='leavetype_labelinactive'), width=2,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                 dcc.Checklist(
                                    options=[
                                        {'label': ' Inactive?', 'value': '1'},
                                    ], id='leavetype_chkmarkforinactive', value=[]
                                 ),
                                ], id='divleavetypeinactive',width=8, style={'text-align': 'middle', 'display': 'inline'}),
                         # dbc.Col([
                         #
                         #     # html.Div([
                         #
                         #     # ], id='divleavetypeinactive', style={'text-align': 'middle', 'display': 'inline'}),
                         # ], width=8
                         # ),

                        ],),
                        id='divleavetypeinactiveformgroup',
                    ),
                    # dbc.FormGroup(
                    #     [dbc.Label(html.Div("Make inactive", id='labelleavetypeinactive'), width=2, style={"text-align": "left"}),
                    #      dbc.Col([
                    #          html.Div([
                    #              dcc.Checklist(
                    #                  options=[
                    #                      {'label': ' Inactive?', 'value': '1'},
                    #                  ], id='designation_chkmarkforinactive', value=[]
                    #              ),
                    #          ], id='divdesignationinactive', style={'text-align': 'middle', 'display': 'inline'}),
                    #      ],
                    #         width=8
                    #     )],
                    #     row=True,

                    # ),

                    html.Br(),
                    html.Div([
                        dcc.Checklist(
                            options=[
                                {'label': ' Mark for Deletion?', 'value': '1'},
                            ], id='leavetype_chkmarkfordeletion', value=[]
                        ),
                    ], id='divleavetypedelete',  style={'text-align': 'middle', 'display': 'inline'}),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save New Leave Type", id="leavetype_submit",
                                   color="info", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="leavetype_cancel",
                                   href='/settings/settings_leavetypes', color="warning", className="ml-auto")
                    ]),
                ], style={'width': '100%'}),
                dbc.Col([

                    html.Div([
                        dcc.Input(id='leavetype_submit_status', type='text', value="0")
                    ], style={'display': 'none'}),
                    html.Div([
                        dcc.Input(id='leavetype_id', type='text', value="0")
                    ], style={'display': 'none'}),
                    dcc.ConfirmDialog(
                        id='leavetype_message',
                    ), ], width=2
                )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback(
    [
        Output('leavetype_name', 'value'),
        Output('leavetype_code', 'value'),
        Output('leavetype_categ_id', 'value'),
        Output('leavetype_available', 'value'),
        Output('leavetype_class', 'value'),
        Output('leave_type_inclusivity_id', 'value'),
        # Output('leave_type_excess_will_be_id', 'value'),
        Output("leavetype_process_editmodalhead", "children"),
        Output("leavetype_submit", "children"),
        Output("leavetype_id", 'value'),
        #Output("designation_chkmarkforinactive", "value"),
        Output("leavetype_chkmarkfordeletion", "value"),
        Output("leavetype_chkmarkforinactive", "value"),
        #Output("labelleavetypeinactive", "style"),
        #Output("divleavetypeinactive", "style"),
        Output("divleavetypedelete", "style"),
        Output("divleavetypeinactiveformgroup", "style"),
    ],
    [
        Input('leavetype_submit_status', 'value'),
        Input('btn_leavetype_head_close', 'n_clicks'),
        Input("url", "search"),
    ],
    [
        State('leavetype_name', 'value'),
        State('leavetype_code', 'value'),
        State('leavetype_categ_id', 'value'),
        State('leavetype_available', 'value'),
        State('leavetype_class', 'value'),
        State('leave_type_inclusivity_id', 'value'),
        # State('leave_type_excess_will_be_id', 'value'),
        State('leavetype_process_editmodalhead', "children"),
        State("leavetype_submit", "children"),
        State("leavetype_id", 'value'),
        # State("designation_chkmarkforinactive", "value"),
        State("leavetype_chkmarkfordeletion", "value"),
        State("leavetype_chkmarkforinactive", "value"),
    ]

)
def leavetype_cleardata(leavetype_submit_status, btn_leavetype_head_close, url,
              leavetype_name, leavetype_code, leavetype_categ_id, leavetype_available, leavetype_class, leave_type_inclusivity_id, #leave_type_excess_will_be_id,
              leavetype_process_editmodalhead, leavetype_submit, leavetype_id, leavetype_chkmarkfordeletion, leavetype_chkmarkforinactive):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":
            leavetype_id = parse_qs(parsed.query)['leave_type_id'][0]
            sql = '''SELECT leave_type_name, leave_type_code, leave_type_categ_id, leave_type_emp_class_id, leave_type_current_ind, leave_type_class_id, leave_type_inclusivity_id, leave_excess_type_id
            FROM leave_types
            WHERE leave_type_id=%s'''
            values = (leavetype_id,)
            columns = ['leave_type_name', 'leave_type_code', 'leave_type_categ_id', 'leave_type_emp_class_id', 'leave_type_current_ind', 'leave_type_class_id', 'leave_type_inclusivity_id', 'leave_excess_type_id']
            df = securequerydatafromdatabase(sql, values, columns)
            leavetype_name = df["leave_type_name"][0]
            leavetype_code = df["leave_type_code"][0]
            leavetype_categ_id = df["leave_type_categ_id"][0]
            leave_type_emp_class = df["leave_type_emp_class_id"][0]
            leave_type_class_id = df['leave_type_class_id'][0]
            leave_type_inclusivity_id = df['leave_type_inclusivity_id'][0]
            # leave_type_excess_will_be_id = df['leave_excess_type_id'][0]

            if leave_type_emp_class == None:
                leave_type_emp_class = None
            else:

                leave_type_emp_class = re.split("[{|}|;|,]", leave_type_emp_class)
                leave_type_emp_class = list(filter(None, leave_type_emp_class))

            # if leave_type_excess_will_be_id == None:
            #     leave_type_excess_will_be_id = None
            # else:
            #
            #     leave_type_excess_will_be_id = re.split("[{|}|;|,]", leave_type_excess_will_be_id)
            #     leave_type_excess_will_be_id = list(filter(None, leave_type_excess_will_be_id))

            leave_type_chkmarkforinactive = df["leave_type_current_ind"][0]

            if leave_type_chkmarkforinactive==True:
                forinactive = []
            elif leave_type_chkmarkforinactive==False:
                forinactive = ['1']
            else:
                forinactive = []

            values = [leavetype_name, leavetype_code, leavetype_categ_id, leave_type_emp_class, leave_type_class_id, leave_type_inclusivity_id, #leave_type_excess_will_be_id,
                    "Edit Existing Leave Type", "Save Changes", leavetype_id, [], forinactive, {'text-align': 'middle', 'display': 'inline'}, {'text-align': 'middle', 'display': 'inline'}]
            return values
        elif parse_qs(parsed.query)['mode'][0] == "add":
            values = ["", "", "", "","", "", leavetype_process_editmodalhead,
                      leavetype_submit, leavetype_id, [], [], {'display': 'none'}, {'display': 'none'}]
            return values
    else:
        raise PreventUpdate


@app.callback(
    [
        Output("leavetype_name", "valid"),
        Output("leavetype_name", "invalid"),
        Output("leavetype_code", "valid"),
        Output("leavetype_code", "invalid"),
        Output("leavetype_categ_id", "valid"),
        Output("leavetype_categ_id", "invalid"),
        Output("leavetype_available", "valid"),
        Output("leavetype_available", "invalid"),
        Output("leavetype_class", "valid"),
        Output("leavetype_class", "invalid"),
        Output("leave_type_inclusivity_id", "valid"),
        Output("leave_type_inclusivity_id", "invalid"),
        # Output("leave_type_excess_will_be_id", "valid"),
        # Output("leave_type_excess_will_be_id", "invalid"),



        Output('leavetype_submit_status', "value"),
        Output('leavetype_results_modal', "is_open"),
        Output('leavetype_results_body', "children"),
        Output('leavetype_results_head_close', "style"),
        Output('leavetype_results_head_return', "style"),
    ],
    [
        Input('leavetype_submit', 'n_clicks'),
        Input('btn_leavetype_head_close', 'n_clicks'),
        Input('btn_leavetype_results_head_return', 'n_clicks'),
    ],
    [
        State('current_user_id', 'data'),
        State('leavetype_name', 'value'),
        State("leavetype_code", "value"),
        State("leavetype_categ_id", "value"),
        State("leavetype_available", "value"),
        State("leavetype_class", "value"),
        State("leave_type_inclusivity_id", "value"),
        # State("leave_type_excess_will_be_id", "value"),
        State("leavetype_submit", "children"),
        #State("designation_chkmarkforinactive", "value"),
        State("leavetype_chkmarkfordeletion", "value"),
        State("leavetype_chkmarkforinactive", "value"),
        State("url", "search"),
        State('leavetype_id', 'value'),
    ]

)
def leavetype_processdata(leavetype_submit, btn_leavetype_head_close, btn_leavetype_results_head_return,
                current_user_id, leavetype_name, leavetype_code,
                leavetype_categ_id, leavetype_available, leavetype_class,leave_type_inclusivity_id, #leave_type_excess_will_be_id,
                mode, leavetype_chkmarkfordeletion, leavetype_chkmarkforinactive, url, leavetype_id):
    ctx = dash.callback_context
    stylehead_close = {'display': 'none'}
    stylehead_return = {'display': 'none'}
    parsed = urlparse.urlparse(url)

    if ctx.triggered:
        validity = [
            False, False, False, False,  False, False, False, False, False, False, False, False
        ]
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'leavetype_submit':
            if leavetype_name:
                is_valid_leavetype_name = True
            else:
                is_valid_leavetype_name = False
            if leavetype_code:
                is_valid_leavetype_code= True
            else:
                is_valid_leavetype_code= True
            if leavetype_categ_id:
                is_valid_leavetype_categ_id = True
            else:
                is_valid_leavetype_categ_id = False
            if leavetype_available:
                is_valid_leavetype_available = True
            else:
                is_valid_leavetype_available = False

            if leavetype_class:
                is_valid_leavetype_class = True
            else:
                is_valid_leavetype_class = False
            if leave_type_inclusivity_id:
                is_valid_leave_type_inclusivity_id = True
            else:
                is_valid_leave_type_inclusivity_id = False
            # if leave_type_excess_will_be_id:
            #     is_valid_leave_type_excess_will_be_id = True
            # else:
            #     is_valid_leave_type_excess_will_be_id = False

            validity = [
                is_valid_leavetype_name, not is_valid_leavetype_name,
                is_valid_leavetype_code, not is_valid_leavetype_code,
                is_valid_leavetype_categ_id, not is_valid_leavetype_categ_id,
                is_valid_leavetype_available, not is_valid_leavetype_available,
                is_valid_leavetype_class, not is_valid_leavetype_class,
                is_valid_leave_type_inclusivity_id, not is_valid_leave_type_inclusivity_id
                # is_valid_leave_type_excess_will_be_id, not is_valid_leave_type_excess_will_be_id

            ]

            allvalid = [is_valid_leavetype_name, is_valid_leavetype_code, is_valid_leavetype_categ_id, is_valid_leavetype_available, is_valid_leave_type_inclusivity_id] #, is_valid_leave_type_excess_will_be_id]
            if all(allvalid):
                if mode == "Save New Leave Type":

                    sql = """
                        INSERT INTO leave_types (leave_type_name, leave_type_code, leave_type_categ_id, leave_type_emp_class_id, leave_type_delete_ind,
                        leave_type_inserted_by, leave_type_inserted_on, leave_type_current_ind, leave_type_class_id, leave_type_inclusivity_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING leave_type_id
                    """
                    values = (leavetype_name, leavetype_code,
                              leavetype_categ_id, leavetype_available, False, current_user_id, datetime.now(), True, leavetype_class, leave_type_inclusivity_id) #, leave_type_excess_will_be_id)
                    leavetype_id = modifydatabasereturnid(sql, values)
                    displayed = True
                    message = "Successfully added new leave type"
                    status = "1"
                    stylehead_close = {'display': 'inline'}
                    stylehead_return = {'display': 'none'}
                else:
                    sql = """
                        UPDATE leave_types SET leave_type_name = %s, leave_type_code = %s, leave_type_categ_id = %s, leave_type_emp_class_id = %s,
                            leave_type_delete_ind= %s, leave_type_inserted_by= %s, leave_type_inserted_on= %s, leave_type_current_ind = %s, leave_type_class_id = %s, leave_type_inclusivity_id=%s
                             WHERE leave_type_id = %s
                    """

                    if leavetype_chkmarkforinactive:
                        if '1' in leavetype_chkmarkforinactive:
                            forinactive = False
                        else:
                            forinactive = True
                    else:
                        forinactive = True


                    if '1' in leavetype_chkmarkfordeletion:
                        fordelete = True
                    else:
                        fordelete = False
                    values = (leavetype_name, leavetype_code, leavetype_categ_id, leavetype_available,
                              fordelete, current_user_id, datetime.now(), forinactive, leavetype_class, leave_type_inclusivity_id, leavetype_id)
                    modifydatabase(sql, values)
                    validity = [
                        False, False, False, False,  False, False, False, False, False, False, False, False
                    ]
                    stylehead_close = {'display': 'none'}
                    stylehead_return = {'display': 'inline'}
                    displayed = True
                    message = "Successfully edited leave type"
                    status = "1"
            else:
                status = "2"
                displayed = True
                message = "Please review input data"
                stylehead_close = {'display': 'inline'}
                stylehead_return = {'display': 'none'}
            out = [status, displayed, message, stylehead_close, stylehead_return]
            out = validity+out

            return out
        elif eventid == 'btn_leavetype_head_close':
            status = "0"
            displayed = False
            message = "Please review input data"
            stylehead_close = {'display': 'inline'}
            stylehead_return = {'display': 'none'}
            out = [status, displayed, message, stylehead_close, stylehead_return]
            out = validity+out
            return out
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

# @app.callback([
#
#     Output('leave_type_excess_will_be_id', 'options'),
#
# ],
#     [
#     Input('url', 'pathname'),
# ],
#     [
#     State('url', 'search'),
#
#     # State('admin_pos_id', 'data')
#
# ],)
# def perf_level_fillindropdowns(path, url):
#     parsed = urlparse.urlparse(url)
#     if path == "/settings/settings_leavetypes_profile":
#         # mode = str(parse_qs(parsed.query)['mode'][0])
#         # if mode == "edit":
#         #     admin_pos_load_data = 1
#         # else:
#         #     admin_pos_load_data = 2
#         # listofallowedunits = tuple(sessionlistofunits[str(sessioncurrentunit)])
#
#         leavetypesoptions = commonmodules.queryfordropdown('''
#             SELECT leave_type_name || ' (' || leave_type_code || ') ' as label, leave_type_id as value
#            FROM leave_types
#            WHERE leave_type_delete_ind = %s and leave_type_id IN %s
#            and leave_type_current_ind = %s
#            ORDER BY leave_type_name
#         ''', (False, (19, 20), True))
#
#         return [leavetypesoptions]
#     else:
#         raise PreventUpdate
