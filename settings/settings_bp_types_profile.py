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
                html.H4("Add New SR Type", id="bp_type_process_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.Modal([
                dbc.ModalHeader("Process SR Type"),
                dbc.ModalBody([
                ], id="bp_type_results_body"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Close", id="btn_bp_type_head_close",
                                       color="primary", block=True),
                        ], id="bp_type_results_head_close", style={'display': 'none'}),
                        dbc.Col([
                            dbc.Button("Return", id="btn_bp_type_results_head_return",
                                       color="primary", block=True, href='/settings/settings_bp_types'),
                        ], id="bp_type_results_head_return", style={'display': 'none'}),
                    ], style={'width': '100%'}),
                ]),
            ], id="bp_type_results_modal"),
            dbc.CardBody([
                dcc.Link('← Back to list of SR types', href='/settings/settings_bp_types'),
                html.Br(),
                html.Br(),

                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("SR Type Name", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="bp_type_name", placeholder="Enter BP Type Name"
                             ),
                             dbc.FormFeedback(
                                 "Too short, already taken, or has spaces", valid=False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label(html.Div("Is a Primary SR?", id='labelisaprimarytypeactive'), width=2, style={"text-align": "left"}),
                         dbc.Col([
                             html.Div([
                                 dcc.Checklist(
                                     options=[
                                         {'label': ' Check as Primary SR', 'value': '1'},
                                     ], id='isaprimarytype_chkmarkforactive', value=[]
                                 ),
                             ], id='divisaprimarytypeactive', style={'text-align': 'middle', 'display': 'inline'}),
                         ],
                            width=8
                        )],
                        row=True,
                    ),
                    dbc.FormGroup(
                        [dbc.Label(html.Div("Is a BP Type?", id='labelisabptypeactive'), width=2, style={"text-align": "left"}),
                         dbc.Col([
                             html.Div([
                                 dcc.Checklist(
                                     options=[
                                         {'label': ' Check as BP Type', 'value': '1'},
                                     ], id='isabptype_chkmarkforactive', value=[]
                                 ),
                             ], id='divisabptypeactive', style={'text-align': 'middle', 'display': 'inline'}),
                         ],
                            width=8
                        )],
                        row=True,
                    ),
                    dbc.FormGroup(
                        [dbc.Label(html.Div("Is a Separation Type?", id='labelisaseptypeactive'), width=2, style={"text-align": "left"}),
                         dbc.Col([
                             html.Div([
                                 dcc.Checklist(
                                     options=[
                                         {'label': ' Check as Separation Type', 'value': '1'},
                                     ], id='isaseptype_chkmarkforactive', value=[]
                                 ),
                             ], id='divisaseptypeactive', style={'text-align': 'middle', 'display': 'inline'}),
                         ],
                            width=8
                        )],
                        row=True,
                    ),
                    dbc.FormGroup(
                        [dbc.Label(html.Div("Is a GSIS Record Type?", id='labelisagsistypeactive'), width=2, style={"text-align": "left"}),
                         dbc.Col([
                             html.Div([
                                 dcc.Checklist(
                                     options=[
                                         {'label': ' Check as GSIS Record Type', 'value': '1'},
                                     ], id='isagsistype_chkmarkforactive', value=[]
                                 ),
                             ], id='divisagsistypeactive', style={'text-align': 'middle', 'display': 'inline'}),
                         ],
                            width=8
                        )],
                        row=True,
                    ),
                    dbc.FormGroup(
                        [dbc.Label(html.Div("Is Active?", id='labelisactive'), width=2, style={"text-align": "left"}),
                         dbc.Col([
                             html.Div([
                                 dcc.Checklist(
                                     options=[
                                         {'label': ' Check as Active Type', 'value': '1'},
                                     ], id='isactivetype_chkmarkforactive', value=[]
                                 ),
                             ], id='divistypeactive', style={'text-align': 'middle', 'display': 'inline'}),
                         ],
                            width=8
                        )],
                        row=True,
                    ),
                    html.Div([
                        dcc.Checklist(
                            options=[
                                {'label': 'Mark for Deletion?', 'value': '1'},
                            ], id='bp_type_chkmarkfordeletion', value=[]
                        ),
                    ], id='divbp_typedelete',  style={'text-align': 'middle', 'display': 'inline'}),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save New SR Type", id="bp_type_submit",
                                   color="primary", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="bp_type_cancel", color="secondary",
                                   className="ml-auto", href='/settings/settings_bp_types')
                    ]),
                ], style={'width': '100%'}),
                dbc.Col([

                    html.Div([
                        dcc.Input(id='bp_type_submit_status', type='text', value="0")
                    ], style={'display': 'none'}),
                    html.Div([
                        dcc.Input(id='bp_type_id', type='text', value="0")
                    ], style={'display': 'none'}),
                    dcc.ConfirmDialog(
                        id='bp_type_message',
                    ), ], width=2
                )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback(
    [
        Output('bp_type_name', 'value'),
        Output('isaprimarytype_chkmarkforactive', 'value'),
        Output('isabptype_chkmarkforactive', 'value'),
        Output('isaseptype_chkmarkforactive', 'value'),
        Output('isagsistype_chkmarkforactive', 'value'),
        Output('isactivetype_chkmarkforactive', 'value'),
        Output("bp_type_process_editmodalhead", "children"),
        Output("bp_type_submit", "children"),
        Output("bp_type_id", 'value'),
        Output("bp_type_chkmarkfordeletion", "value"),
        Output("divbp_typedelete", "style"),
    ],
    [
        Input('bp_type_submit_status', 'value'),
        Input('btn_bp_type_head_close', 'n_clicks'),
        Input("url", "search"),
    ],
    [
        State('bp_type_name', 'value'),
        State('bp_type_process_editmodalhead', "children"),
        State("bp_type_submit", "children"),
        State("bp_type_id", 'value'),
        State("bp_type_chkmarkfordeletion", "value"),
    ]

)
def cleardata(bp_type_submit_status, btn_bp_type_head_close, url,
              bp_type_name, bp_type_process_editmodalhead, bp_type_submit, bp_type_id, bp_type_chkmarkfordeletion):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":
            bp_type_id = parse_qs(parsed.query)['bp_type_id'][0]
            sql = '''SELECT appt_type_name, appt_type_is_primary, is_bp_type, is_sep_type, appt_type_is_gsis, appt_type_is_active
                       FROM appointment_types WHERE appt_type_id=%s'''
            values = (bp_type_id,)
            columns = ['appt_type_name', 'appt_type_is_primary', 'is_bp_type', 'is_sep_type', 'appt_type_is_gsis', 'appt_type_is_active']
            df = securequerydatafromdatabase(sql, values, columns)
            bp_type_name = df["appt_type_name"][0]
            is_primary = df["appt_type_is_primary"][0]
            is_bp_type = df["is_bp_type"][0]
            is_sep_type = df["is_sep_type"][0]
            is_gsis = df["appt_type_is_gsis"][0]
            is_active = df["appt_type_is_active"][0]
            if is_bp_type == True:
                is_bp_type = ['1']
            else:
                is_bp_type = ['0']

            if is_sep_type == True:
                is_sep_type = ['1']
            else:
                is_sep_type = ['0']

            if is_primary == True:
                is_primary = ['1']
            else:
                is_primary = ['0']

            if is_gsis == True:
                is_gsis = ['1']
            else:
                is_gsis = ['0']

            if is_active == True:
                is_active = ['1']
            else:
                is_active = ['0']

            values = [bp_type_name, is_primary, is_bp_type, is_sep_type, is_gsis, is_active, "Edit Existing SR Type", "Save Changes",
                      bp_type_id, [], {'text-align': 'middle', 'display': 'inline'}]
            return values
        elif parse_qs(parsed.query)['mode'][0] == "add":
            values = ["", "", "", "", "", "", bp_type_process_editmodalhead,
                      bp_type_submit, bp_type_id, [], {'display': 'none'}]
            return values
    else:
        raise PreventUpdate


@app.callback(
    [
        Output("bp_type_name", "valid"),
        Output("bp_type_name", "invalid"),
        Output('bp_type_submit_status', "value"),
        Output('bp_type_results_modal', "is_open"),
        Output('bp_type_results_body', "children"),
        Output('bp_type_results_head_close', "style"),
        Output('bp_type_results_head_return', "style"),
    ],
    [
        Input('bp_type_submit', 'n_clicks'),
        Input('btn_bp_type_head_close', 'n_clicks'),
        Input('btn_bp_type_results_head_return', 'n_clicks'),
    ],
    [
        State('current_user_id', 'data'),
        State('bp_type_name', 'value'),
        State('isaprimarytype_chkmarkforactive', 'value'),
        State('isabptype_chkmarkforactive', 'value'),
        State('isaseptype_chkmarkforactive', 'value'),
        State('isagsistype_chkmarkforactive', 'value'),
        State('isactivetype_chkmarkforactive', 'value'),
        State("bp_type_submit", "children"),
        State("bp_type_chkmarkfordeletion", "value"),
        State("url", "search"),
        State('bp_type_id', 'value'),
    ]

)
def processdata(bp_type_submit, btn_bp_type_head_close, btn_bp_type_results_head_return,
                current_user_id, bp_type_name,isaprimarytype_chkmarkforactive, isabptype_chkmarkforactive,  isaseptype_chkmarkforactive,isagsistype_chkmarkforactive,
                isactivetype_chkmarkforactive,
                mode, bp_type_chkmarkfordeletion, url, bp_type_id):
    ctx = dash.callback_context
    stylehead_close = {'display': 'none'}
    stylehead_return = {'display': 'none'}
    parsed = urlparse.urlparse(url)

    if ctx.triggered:
        validity = [
            False, False
        ]
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == 'bp_type_submit':
            if bp_type_name:
                is_valid_bp_type_name = True
            else:
                is_valid_bp_type_name = False

            validity = [
                is_valid_bp_type_name, not is_valid_bp_type_name,
            ]
            allvalid = [is_valid_bp_type_name]

            if all(allvalid):
                if '1' in isabptype_chkmarkforactive:
                    forbptypeactive = True
                else:
                    forbptypeactive = False

                if '1' in isaseptype_chkmarkforactive:
                    forseptypeactive = True
                else:
                    forseptypeactive = False

                if '1' in isaprimarytype_chkmarkforactive:
                    forprimarytypeactive = True
                else:
                    forprimarytypeactive = False

                if '1' in isagsistype_chkmarkforactive:
                    forgsistypeactive = True
                else:
                    forgsistypeactive = False


                if '1' in isactivetype_chkmarkforactive:
                    foractivetype = True
                else:
                    foractivetype = False

                if mode == "Save New SR Type":
                    sql = """
                        INSERT INTO appointment_types(appt_type_name, appt_type_is_primary, is_bp_type, is_sep_type, appt_type_is_gsis, appt_type_is_active, appt_type_delete_ind,
                        appt_type_inserted_by, appt_type_inserted_on, appt_type_is_active)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING appt_type_id
                    """
                    values = (bp_type_name, forprimarytypeactive, forbptypeactive,
                              forseptypeactive, forgsistypeactive, foractivetype, False, current_user_id, datetime.now(), True)
                    bp_type_id = modifydatabasereturnid(sql, values)
                    displayed = True
                    message = "Successfully added new BP Type"
                    status = "1"
                    stylehead_close = {'display': 'inline'}
                    stylehead_return = {'display': 'none'}
                else:
                    sql = """
                        UPDATE appointment_types SET appt_type_name = %s, appt_type_is_primary = %s, is_bp_type = %s, is_sep_type = %s, appt_type_is_gsis = %s, appt_type_is_active = %s,
                            appt_type_delete_ind= %s, appt_type_inserted_by= %s,appt_type_inserted_on= %s, appt_type_is_active = %s WHERE
                            appt_type_id = %s
                    """
                    if '1' in bp_type_chkmarkfordeletion:
                        fordelete = True
                    else:
                        fordelete = False
                    values = (bp_type_name, forprimarytypeactive, forbptypeactive, forseptypeactive, forgsistypeactive, foractivetype,
                              fordelete, current_user_id, datetime.now(), fordelete, bp_type_id)
                    modifydatabase(sql, values)
                    validity = [
                        False, False
                    ]
                    stylehead_close = {'display': 'none'}
                    stylehead_return = {'display': 'inline'}
                    displayed = True
                    message = "Successfully edited BP Type"
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
        elif eventid == 'btn_bp_type_head_close':
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
