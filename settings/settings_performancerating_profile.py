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
from datetime import date as date
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
                html.H4("Add Performance Rating", id = "perf_process_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color':'white'}
            ),
            dbc.Modal([
                dbc.ModalHeader("Process Performance Rating", id = "perf_results_head"),
                dbc.ModalBody([
                ], id = "perf_results_body"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Close", id="btn_perf_head_close", color="primary", block=True),
                        ], id="perf_results_head_close", style={'display':'none'} ),
                        dbc.Col([
                            dbc.Button("Return", id="btn_perf_results_head_return", color="primary", block=True, href ='/settings/settings_performancerating'),
                        ], id="perf_results_head_return", style={'display':'none'} ),
                    ], style={'width':'100%'}),
                ]),
            ], id="perf_results_modal"),
            dbc.CardBody([
                dcc.Link('← Back to Performance Rating', href='/settings/settings_performancerating'),
                html.Br(),
                html.Br(),
                dbc.Form([
                    dbc.FormGroup(
                        [
                            dbc.Label("Employee", width=2, style={"text-align": "left"}),
                            dbc.Col([
                                dcc.Dropdown(
                                    id="perf_emp",
                                    options=[
                                    ],
                                    # value="",
                                    searchable=True,
                                    clearable=True
                                )
                                #dbc.FormFeedback("Too short or already taken", valid = False)
                            ],
                                width=8
                            )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [
                            dbc.Label("Employee #", width=2, style={"text-align": "left"}),
                            dbc.Col([
                                html.P(" ", id="perf_empno", style={"font-weight":"bold"}),
                            ], width=8)
                            ],
                        row=True
                    ),
                    dbc.FormGroup(
                        [
                            dbc.Label("Designation", width=2, style={"text-align": "left"}),
                            dbc.Col([
                                html.P(" ", id="perf_desig", style={"font-weight":"bold"}),
                            ], width=8)
                            ],
                        row=True
                    ),

                    dbc.FormGroup(
                        [dbc.Label("Performance Rating", width=2, style={"text-align":"left"}),
                        dbc.Col([
                            dbc.Input(
                                type="text", id="perf_rating", placeholder="Enter Performance Rating"
                            ),
                            dbc.FormFeedback("Too short or already taken", valid = False)
                        ],
                        width=8
                        )],
                        row = True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Start Period", width=2, style={"text-align":"left"}),
                        dbc.Col([
                            dcc.DatePickerSingle(id='perf_rating_start_period', placeholder="mm/dd/yyyy"),
                            dbc.FormFeedback("Please enter start date.", valid = False)
                        ],width=8)
                        # dbc.Col([
                        #     dbc.Input(
                        #         type="text", id="perf_rating_start_period", placeholder="Enter start period"
                        #     ),
                        #     dbc.FormFeedback("Too short or already taken", valid = False)
                        # ],
                        # width=8
                        # )

                        ],
                        row = True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("End Period", width=2, style={"text-align":"left"}),
                        dbc.Col([
                            dcc.DatePickerSingle(id='perf_rating_end_period', placeholder="mm/dd/yyyy"),

                            dbc.FormFeedback("Please enter end date.", valid = False)
                        ],width=8)
                        # dbc.Col([
                        #     dbc.Input(
                        #         type="text", id="perf_rating_end_period", placeholder="Enter end period"
                        #     ),
                        #     dbc.FormFeedback("Too short or already taken", valid = False)
                        # ],
                        # width=8
                        # )

                        ],
                        row = True
                    ),




                    html.Div([
                        dcc.Checklist(
                                options=[
                                    {'label': ' Mark for Deletion?', 'value': '1'},
                                ], id='perf_chkmarkfordeletion', value=[]
                            ),
                    ],id='divperfdelete',  style={'text-align':'middle', 'display':'inline'}),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save New Performance Rating", id="perf_submit", color="info", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="perf_cancel", color="warning", className="ml-auto")
                    ]),
                ], style={'width':'100%'}),
                dbc.Col([

                    html.Div([
                        dcc.Input(id='perf_submit_status', type='text', value="0")
                    ], style={'display':'none'}),
                    html.Div([
                        dcc.Input(id='perf_rating_id', type='text', value="0")
                    ], style={'display':'none'}),
                    dcc.ConfirmDialog(
                        id='perf_message',
                    ),], width=2
                )
            ], style = {'line-height':"1em", "display":"block"}),
        ], style = {'line-height':"1em", "display":"block"}
        )
     ]),
])

@app.callback(
    [
        Output('perf_emp', 'value'),
        Output('perf_empno', 'value'),
        Output('perf_desig', 'value'),
        Output('perf_rating', 'value'),
        Output('perf_rating_start_period', 'value'),
        Output('perf_rating_end_period', 'value'),
        Output("perf_process_editmodalhead", "children"),
        Output("perf_submit", "children"),
        Output("perf_rating_id",'value'),
        Output("perf_chkmarkfordeletion", "value"),
        Output("divperfdelete", "style"),
    ],
    [
        Input('perf_submit_status', 'value'),
        Input('btn_perf_head_close', 'n_clicks'),
        Input("url", "search"),
    ],
    [
        State('perf_emp', 'value'),
        State('perf_empno', 'value'),
        State('perf_rating', 'value'),
        State('perf_rating_start_period', 'value'),
        State('perf_rating_end_period', 'value'),
        State('perf_process_editmodalhead',"children"),
        State("perf_submit", "children"),
        State("perf_rating_id",'value'),
        State("perf_chkmarkfordeletion", "value"),
    ]

)
def cleardata(perf_submit_status,btn_perf_head_close,url,
    perf_emp, perf_empno,
    perf_rating, perf_rating_start_period,
    perf_rating_end_period,
    perf_process_editmodalhead,perf_submit,perf_rating_id,perf_chkmarkfordeletion):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":
            perf_rating_id = parse_qs(parsed.query)['perf_rating_id'][0]
            sql = '''SELECT pr.emp_id, emp_number, designation_name, perf_rating, perf_rating_start_period, perf_rating_end_period
                FROM performance_ratings pr
                INNER JOIN employees e ON pr.emp_id = e.emp_id
                LEFT JOIN designations d ON d.designation_id = e.emp_primary_designation_id
                WHERE perf_rating_id=%s'''
            values = (perf_rating_id, )
            columns = ['emp_id', 'emp_number', 'designation_name', 'perf_rating', 'perf_rating_start_period', 'perf_rating_end_period']
            df = securequerydatafromdatabase(sql,values,columns)
            perf_emp = df["emp_id"][0]
            perf_empno = df["emp_number"][0]
            perf_desig = df["designation_name"][0]
            perf_rating = df["perf_rating"][0]
            perf_rating_start_period = df["perf_rating_start_period"][0]
            perf_rating_end_period = df["perf_rating_end_period"][0]
            values = [perf_emp, perf_empno, perf_desig, perf_rating, perf_rating_start_period, perf_rating_end_period, "Edit Existing Performance Rating:","Save Changes",perf_rating_id,[],{'text-align':'middle', 'display':'inline'}]
            return values
        elif parse_qs(parsed.query)['mode'][0] == "add":
            values = ["","", "","","","", perf_process_editmodalhead,perf_submit,perf_rating_id,[],{'display':'none'}]
            return values
    else:
        raise PreventUpdate

@app.callback(
    [
        Output("perf_emp", "valid"),
        Output("perf_emp", "invalid"),
        # Output("perf_empno", "valid"),
        # Output("perf_empno", "invalid"),
        # Output("perf_desig", "valid"),
        # Output("perf_desig", "invalid"),
        Output("perf_rating", "valid"),
        Output("perf_rating", "invalid"),
        # Output("perf_rating_start_period", "valid"),
        # Output("perf_rating_start_period", "invalid"),
        # Output("perf_rating_end_period", "valid"),
        # Output("perf_rating_end_period", "invalid"),
        Output('perf_submit_status',"value"),
        Output('perf_results_modal',"is_open"),
        Output('perf_results_body',"children"),
        Output('perf_results_head_close',"style"),
        Output('perf_results_head_return',"style"),
    ],
    [
        Input('perf_submit', 'n_clicks'),
        Input('btn_perf_head_close', 'n_clicks'),
        Input('btn_perf_results_head_return', 'n_clicks'),
    ],
    [
        State('current_user_id', 'data'),
        State('perf_emp', 'value'),
        # State('perf_empno', 'value'),
        # State('perf_desig', 'value'),
        State('perf_rating', 'value'),
        State('perf_rating_start_period', 'date'),
        State("perf_rating_end_period", "date"),
        State("perf_submit", "children"),
        State("perf_chkmarkfordeletion", "value"),
        State("url", "search"),
        State('perf_rating_id', 'value'),
    ]

)
def processdata(perf_submit,btn_perf_head_close,btn_perf_results_head_return,
    current_user_id, perf_emp, #perf_empno, perf_desig,
    perf_rating, perf_rating_start_period,
    perf_rating_end_period,
    mode, perf_chkmarkfordeletion,url,perf_rating_id):
    ctx = dash.callback_context
    stylehead_close = {'display':'none'}
    stylehead_return = {'display':'none'}
    parsed = urlparse.urlparse(url)

    if ctx.triggered:
        validity = [
            False, False,
            False, False,
            # False, False,
            # False, False,
            # False, False,
            # False, False
            ]
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'perf_submit':
            if perf_emp:
                is_valid_perf_emp = True
            else:
                is_valid_perf_emp = False

            # if perf_empno:
            #     is_valid_perf_empno = True
            # else:
            #     is_valid_perf_empno = False
            #
            # if perf_desig:
            #     is_valid_perf_desig = True
            # else:
            #     is_valid_perf_desig = False


            if perf_rating:
                is_valid_perf_rating = True
            else:
                is_valid_perf_rating = False

            # if perf_rating_start_period:
            #     is_valid_perf_rating_start_period = True
            # else:
            #     is_valid_perf_rating_start_period = False
            #
            # if perf_rating_end_period:
            #     is_valid_perf_rating_end_period = True
            # else:
            #     is_valid_perf_rating_end_period = False


            validity = [
                is_valid_perf_emp, not is_valid_perf_emp,
                # is_valid_perf_empno, not is_valid_perf_empno,
                # is_valid_perf_desig, not is_valid_perf_desig,
                is_valid_perf_rating, not is_valid_perf_rating,
                # is_valid_perf_rating_start_period, not is_valid_perf_rating_start_period,
                # is_valid_perf_rating_end_period, not is_valid_perf_rating_end_period

            ]
            allvalid = [is_valid_perf_emp, is_valid_perf_rating] #, is_valid_perf_rating_start_period, is_valid_perf_rating_end_period]
            if all(allvalid):
                if mode =="Save New Performance Rating":
                    sql = """
                        INSERT INTO performance_ratings (emp_id, perf_rating, perf_rating_start_period, perf_rating_end_period, perf_rating_delete_ind,
                        perf_rating_inserted_by, perf_rating_inserted_on)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        RETURNING perf_rating_id
                    """
                    values = (perf_emp, perf_rating, perf_rating_start_period, perf_rating_end_period, False, current_user_id, datetime.now())
                    perf_rating_id = modifydatabasereturnid(sql,values)
                    displayed = True
                    message = "Successfully added new performance rating"
                    status = "1"
                    stylehead_close = {'display':'inline'}
                    stylehead_return = {'display':'none'}
                else:
                    sql = """
                        UPDATE performance_ratings SET emp_id = %s, perf_rating = %s, perf_rating_start_period = %s, perf_rating_end_period = %s,
                            perf_rating_delete_ind= %s, perf_rating_inserted_by= %s, perf_rating_inserted_on= %s WHERE
                            perf_rating_id = %s
                    """
                    if '1' in perf_chkmarkfordeletion:
                        fordelete = True
                    else:
                        fordelete= False
                    values = (perf_emp, perf_rating, perf_rating_start_period, perf_rating_end_period, fordelete, current_user_id, datetime.now(), perf_rating_id)
                    modifydatabase(sql,values)
                    validity = [
                        False, False,
                        False, False,
                        # False, False,
                        # False, False,
                        # False, False,
                        # False, False
                        ]
                    stylehead_close = {'display':'none'}
                    stylehead_return = {'display':'inline'}
                    displayed = True
                    message = "Successfully edited performance rating"
                    status = "1"
            else:
                status = "2"
                displayed = True
                message = "Please review input data"
                stylehead_close = {'display':'inline'}
                stylehead_return = {'display':'none'}
            out = [status, displayed, message, stylehead_close, stylehead_return]
            out = validity+out

            return out
        elif eventid == 'btn_perf_head_close':
            status = "0"
            displayed = False
            message = "Please review input data"
            stylehead_close = {'display':'inline'}
            stylehead_return = {'display':'none'}
            out = [status, displayed, message, stylehead_close, stylehead_return]
            out = validity+out
            return out
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback([
    Output('perf_emp', 'options'),

],
    [
    Input('url', 'pathname'),
],
    [
    State('url', 'search'),
    State('sessioncurrentunit', 'data'),
    State('sessionlistofunits', 'data'),
    # State('admin_pos_id', 'data')

],)
def perf_level_fillindropdowns(path, url, sessioncurrentunit,sessionlistofunits):
    parsed = urlparse.urlparse(url)
    if path == "/settings/settings_performancerating_profile":
        # mode = str(parse_qs(parsed.query)['mode'][0])
        # if mode == "edit":
        #     admin_pos_load_data = 1
        # else:
        #     admin_pos_load_data = 2
        # listofallowedunits = tuple(sessionlistofunits[str(sessioncurrentunit)])

        listofallowedunits = tuple(sessionlistofunits[str(sessioncurrentunit)])
        #print("listofallowedunits",listofallowedunits)
        employees = commonmodules.queryfordropdown('''
            SELECT person_last_name || ', ' || person_first_name as label, emp_id as value
           FROM employees e INNER JOIN persons p ON p.person_id = e.person_id
           WHERE emp_delete_ind = %s AND (emp_class_id = %s OR emp_class_id = %s) AND emp_primary_home_unit_id IN %s
           ORDER BY person_last_name
        ''', (False, 2, 3, listofallowedunits ))

        # degreelevel = commonmodules.queryfordropdown('''
        #     SELECT degree_level as label, degree_level_id as value
        #       FROM degree_levels dl
        #      WHERE dl.degree_level_delete_int = %s
        #    ORDER BY degree_level
        # ''', (False, ))



        return [employees]
    else:
        raise PreventUpdate

@app.callback([Output('perf_empno', 'children'),
            Output('perf_desig', 'children')
               ],
              [
    Input('perf_emp', 'value'),
    Input('perf_submit_status', 'value'),
],
    [
],)
def querymodulesfordtcall(perf_emp, perf_submit_status):
    # if sdesignationname:
    #     sdesignationname = "%"+sdesignationname+"%"
    #     sqlcommand = "SELECT designation_id, designation_name FROM designations WHERE designation_delete_ind = %s and designation_current_ind = %s and designation_name ILIKE %s ORDER By designation_name"
    #     values = (False, True, sdesignationname)
    # else:

    if perf_emp:

        sqlcommand = '''SELECT emp_number, designation_name from employees e
            LEFT JOIN designations d ON d.designation_id = e.emp_primary_designation_id
            where emp_id = %s'''
        values = (perf_emp,)

        columns = ["emp_id", "designation_name"]
        df = securequerydatafromdatabase(sqlcommand, values, columns)
        perf_empno = df['emp_id'][0]
        perf_desig = df['designation_name'][0]




        return [perf_empno, perf_desig]
    else:
        raise PreventUpdate
