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
                html.H4("Add New Designation", id="designation_process_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.Modal([
                dbc.ModalHeader("Process Designations", id="designation_results_head"),
                dbc.ModalBody([
                ], id="designation_results_body"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Close", id="btn_designation_head_close",
                                       color="primary", block=True),
                        ], id="designation_results_head_close", style={'display': 'none'}),
                        dbc.Col([
                            dbc.Button("Return", id="btn_designation_results_head_return",
                                       color="primary", block=True, href='/settings/settings_designations'),
                        ], id="designation_results_head_return", style={'display': 'none'}),
                    ], style={'width': '100%'}),
                ]),
            ], id="designation_results_modal"),
            dbc.CardBody([
                dcc.Link('← Back to Designations', href='/settings/settings_designations'),
                html.Br(),
                html.Br(),
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("Designation Name", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="designation_name", placeholder="Enter Designation Name"
                             ),
                             dbc.FormFeedback("Too short or already taken", valid=False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Description", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="designation_description", placeholder="Enter Designation description"
                             ),
                             #dbc.FormFeedback("Too short or already taken", valid = False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Employee Class", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dcc.Dropdown(
                                 id="designation_emp_class_id",
                                 options=[
                                    {'label': 'Faculty', 'value': '1'},
                                    {'label': 'Administrative Personnel', 'value': '2'},
                                    {'label': 'Research and Extension Professional Staff (REPS)', 'value': '3'},
                                    {'label': 'Others', 'value': '11'}
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
                        [dbc.Label("Regularity", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dcc.Dropdown(
                                 id="designation_reg_id",
                                 options=[
                                     {'label': 'Regular', 'value': '1'},
                                     {'label': 'Non-regular', 'value': '2'},
                                 ],
                                 searchable=False
                             ),
                             # dbc.FormFeedback("Too short or already taken", valid = False)
                         ],
                             width=8
                         )],
                        row=True
                    ),

                    dbc.FormGroup(
                        [dbc.Label(html.Div("Make DBM position", id='labeldesignationinactive'), width=2,
                                   style={"text-align": "left"}),
                         dbc.Col([
                             # html.Div([
                             dcc.Checklist(
                                 options=[
                                     {'label': ' DBM Position?', 'value': '1'},
                                 ], id='designation_chkmarkfordbm', value=[]
                             ),
                             # ], id='divdesignationinactive', style={'text-align': 'middle', 'display': 'inline'}),
                         ],
                             width=8
                         )],
                        row=True,
                    ),

                    dbc.FormGroup(
                        [dbc.Label(html.Div("Make inactive", id='labeldesignationinactive'), width=2,
                                   style={"text-align": "left"}),
                         dbc.Col([
                             html.Div([
                                 dcc.Checklist(
                                     options=[
                                         {'label': ' Inactive?', 'value': '1'},
                                     ], id='designation_chkmarkforinactive', value=[]
                                 ),
                             ], id='divdesignationinactive', style={'text-align': 'middle', 'display': 'inline'}),
                         ],
                             width=8
                         )],
                        row=True,

                    ),

                    html.Div([
                        dcc.Checklist(
                            options=[
                                {'label': ' Mark for Deletion?', 'value': '1'},
                            ], id='designation_chkmarkfordeletion', value=[]
                        ),
                    ], id='divdesignationdelete',  style={'text-align': 'middle', 'display': 'inline'}),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save New Designation", id="designation_submit",
                                   color="primary", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="designation_cancel",
                                   href='/settings/settings_designations', color="secondary", className="ml-auto")
                    ]),
                ], style={'width': '100%'}),
                dbc.Col([

                    html.Div([
                        dcc.Input(id='designation_submit_status', type='text', value="0")
                    ], style={'display': 'none'}),
                    html.Div([
                        dcc.Input(id='designation_id', type='text', value="0")
                    ], style={'display': 'none'}),
                    dcc.ConfirmDialog(
                        id='designation_message',
                    ), ], width=2
                )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback(
    [
        Output('designation_name', 'value'),
        Output('designation_description', 'value'),
        Output('designation_emp_class_id', 'value'),
        Output("designation_process_editmodalhead", "children"),
        Output("designation_submit", "children"),
        Output("designation_id", 'value'),
        Output("designation_reg_id", 'value'),
        Output("designation_chkmarkfordbm", 'value'),
        Output("designation_chkmarkforinactive", "value"),
        Output("designation_chkmarkfordeletion", "value"),
        Output("labeldesignationinactive", "style"),
        Output("divdesignationinactive", "style"),
        Output("divdesignationdelete", "style"),
    ],
    [
        Input('designation_submit_status', 'value'),
        Input('btn_designation_head_close', 'n_clicks'),
        Input("url", "search"),
    ],
    [
        State('designation_name', 'value'),
        State('designation_description', 'value'),
        State('designation_emp_class_id', 'value'),
        State('designation_chkmarkforinactive', 'value'),
        State('designation_process_editmodalhead', "children"),
        State("designation_submit", "children"),
        State("designation_id", 'value'),
        State("designation_reg_id", 'value'),
        State("designation_chkmarkfordbm", 'value'),
        State("designation_chkmarkfordeletion", "value"),
    ]

)
def clear_designations_data(designation_submit_status, btn_designation_head_close, url,
              designation_name, designation_description, designation_emp_class_id, designation_chkmarkforinactive,
              designation_process_editmodalhead, designation_submit, designation_id, designation_reg_id, designation_chkmarkfordbm,
              designation_chkmarkfordeletion):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":
            designation_id = parse_qs(parsed.query)['designation_id'][0]
            sql = '''SELECT designation_name, designation_description, designation_emp_class_id, designation_regularity_id, designation_dbm_position_ind, designation_current_ind
            FROM designations
            WHERE designation_id=%s'''
            values = (designation_id,)
            columns = ['designation_name', 'designation_description', 'designation_emp_class_id', 'designation_regularity_id', 'designation_dbm_position_ind', 'designation_current_ind']
            df = securequerydatafromdatabase(sql, values, columns)

            designation_name = df["designation_name"][0]
            designation_description = df["designation_description"][0]
            designation_emp_class_id = df["designation_emp_class_id"][0]

            designation_chkmarkforinactive = df["designation_current_ind"][0]

            if designation_chkmarkforinactive==True:
                forinactive = []
            else:
                forinactive = ['1']

            designation_regularity_id = df["designation_regularity_id"][0]

            designation_dbm_position_ind = df["designation_dbm_position_ind"][0]

            if designation_dbm_position_ind==True:
                fordbm = ['1']
            else:
                fordbm = []

            designation_current_ind = df["designation_current_ind"][0]


            values = [designation_name, designation_description, designation_emp_class_id,
                      "Edit Existing Designation",
                      "Save Changes", designation_id, designation_regularity_id, fordbm, forinactive,
                     [], {'text-align': 'middle', 'display': 'inline'}, {'text-align': 'middle', 'display': 'inline'}, {'text-align': 'middle', 'display': 'inline'}]
            return values
        elif parse_qs(parsed.query)['mode'][0] == "add":
            values = ["", "", "", designation_process_editmodalhead,
                      designation_submit, designation_id, "", [], [], [], {'display': 'none'}, {'display': 'none'}, {'display': 'none'}]
            return values
    else:
        raise PreventUpdate


@app.callback(
    [
        Output("designation_name", "valid"),
        Output("designation_name", "invalid"),
        Output("designation_description", "valid"),
        Output("designation_description", "invalid"),
        Output("designation_emp_class_id", "valid"),
        Output("designation_emp_class_id", "invalid"),

        Output('designation_submit_status', "value"),
        Output('designation_results_modal', "is_open"),
        Output('designation_results_body', "children"),
        Output('designation_results_head_close', "style"),
        Output('designation_results_head_return', "style"),
    ],
    [
        Input('designation_submit', 'n_clicks'),
        Input('btn_designation_head_close', 'n_clicks'),
        Input('btn_designation_results_head_return', 'n_clicks'),
    ],
    [
        State('current_user_id', 'data'),
        State('designation_name', 'value'),
        State("designation_description", "value"),
        State("designation_emp_class_id", "value"),
        State("designation_reg_id", 'value'),
        State("designation_chkmarkfordbm", 'value'),
        State("designation_submit", "children"),
        State("designation_chkmarkforinactive", "value"),
        State("designation_chkmarkfordeletion", "value"),
        State("url", "search"),
        State('designation_id', 'value'),
    ]

)
def process_designations_data(designation_submit, btn_designation_head_close, btn_designation_results_head_return,
                current_user_id, designation_name, designation_description,
                designation_emp_class_id, designation_reg_id, designation_chkmarkfordbm, mode, designation_chkmarkforinactive, designation_chkmarkfordeletion, url, designation_id):
    ctx = dash.callback_context
    stylehead_close = {'display': 'none'}
    stylehead_return = {'display': 'none'}
    parsed = urlparse.urlparse(url)

    if ctx.triggered:
        validity = [
            False, False, False, False,  False, False
        ]
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'designation_submit':

            if designation_name:
                designation_name = designation_name.upper()
                is_valid_designation_name = True
            else:
                is_valid_designation_name = False
            if designation_description:
                is_valid_designation_description= True
            else:
                is_valid_designation_description= True
            if designation_emp_class_id:
                is_valid_designation_emp_class_id = True
            else:
                is_valid_designation_emp_class_id = False

            validity = [
                is_valid_designation_name, not is_valid_designation_name,
                is_valid_designation_description, not is_valid_designation_description,
                is_valid_designation_emp_class_id, not is_valid_designation_emp_class_id,

            ]
            allvalid = [is_valid_designation_name,  is_valid_designation_description,
                        is_valid_designation_emp_class_id]
            if all(allvalid):
                if mode == "Save New Designation":

                    sql = """
                        INSERT INTO designations (designation_name, designation_description, designation_emp_class_id,
                        designation_regularity_id, designation_dbm_position_ind,
                        designation_delete_ind,
                        designation_inserted_by, designation_inserted_on, designation_current_ind)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING designation_id
                    """

                    if '1' in designation_chkmarkfordbm:
                        fordbm = True
                    else:
                        fordbm = False

                    values = (designation_name, designation_description,
                              designation_emp_class_id, designation_reg_id, fordbm,
                              False, current_user_id, datetime.now(), True)
                    designation_id = modifydatabasereturnid(sql, values)
                    displayed = True
                    message = "Successfully added new designation"
                    status = "1"
                    stylehead_close = {'display': 'inline'}
                    stylehead_return = {'display': 'none'}
                else:
                    sql = """
                        UPDATE designations SET designation_name = %s, designation_description = %s, designation_emp_class_id = %s,
                            designation_regularity_id = %s, designation_dbm_position_ind = %s,
                            designation_delete_ind= %s, designation_inserted_by= %s, designation_inserted_on= %s, designation_current_ind = %s WHERE
                            designation_id = %s
                    """


                    if designation_chkmarkforinactive:
                        if '1' in designation_chkmarkforinactive:
                            forinactive = False
                        else:
                            forinactive = True
                    else:
                        forinactive = True

                    if '1' in designation_chkmarkfordeletion:
                        fordelete = True
                    else:
                        fordelete = False

                    if '1' in designation_chkmarkfordbm:
                        fordbm = True
                    else:
                        fordbm = False


                    values = (designation_name, designation_description, designation_emp_class_id, designation_reg_id, fordbm,
                              fordelete, current_user_id, datetime.now(), forinactive, designation_id)
                    modifydatabase(sql, values)
                    validity = [
                        False, False, False, False,  False, False
                    ]
                    stylehead_close = {'display': 'none'}
                    stylehead_return = {'display': 'inline'}
                    displayed = True
                    message = "Successfully edited designation"
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
        elif eventid == 'btn_designation_head_close':
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
