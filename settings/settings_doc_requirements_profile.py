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
                html.H4("Add New Document Requirement", id="document_process_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.Modal([
                dbc.ModalHeader("Process Document Requirement", id="role_results_head"),
                dbc.ModalBody([
                ], id="document_results_body"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Close", id="btn_document_head_close",
                                       color="primary", block=True),
                        ], id="document_results_head_close", style={'display': 'none'}),
                        dbc.Col([
                            dbc.Button("Return", id="btn_document_results_head_return", color="primary",
                                       block=True, href='/settings/settings_doc_requirements'),
                        ], id="document_results_head_return", style={'display': 'none'}),
                    ], style={'width': '100%'}),
                ]),
            ], id="document_results_modal"),
            dbc.CardBody([
                dcc.Link('← Back to List of Documentary Requirements', href='/settings/settings_doc_requirements'),
                html.Br(),
                html.Br(),

                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("Document Name", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="document_name", placeholder="Enter Document Name"
                             ),
                             dbc.FormFeedback(
                                 "Too short, already taken, or has spaces", valid=False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(  # Added for document description
                        [dbc.Label("Document Description", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="document_description", placeholder="Enter Document Description"
                             ),
                             dbc.FormFeedback(
                                 "Too short, already taken, or has spaces", valid=False)
                         ],
                            width=8
                        )],
                        row=True
                    ),


                    html.Div([
                        dcc.Checklist(
                            options=[
                                {'label': 'Mark for Deletion?', 'value': '1'},
                            ], id='document_chkmarkfordeletion', value=[]
                        ),
                    ], id='divdocumentdelete',  style={'text-align': 'middle', 'display': 'inline'}),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save New Document", id="document_submit",
                                   color="primary", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="document_cancel", color="secondary",
                                   className="ml-auto", href='/settings/settings_doc_requirements')
                    ]),
                ], style={'width': '100%'}),
                dbc.Col([

                    html.Div([
                        dcc.Input(id='document_submit_status', type='text', value="0")
                    ], style={'display': 'none'}),
                    html.Div([
                        dcc.Input(id='document_id', type='text', value="0")
                    ], style={'display': 'none'}),
                    dcc.ConfirmDialog(
                        id='document_message',
                    ), ], width=2
                )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback(
    [
        Output('document_name', 'value'),
        Output("document_process_editmodalhead", "children"),
        Output("document_submit", "children"),
        Output("document_id", 'value'),
        Output("document_chkmarkfordeletion", "value"),
        Output("divdocumentdelete", "style"),
        Output('document_description', 'value'),
    ],
    [
        Input('document_submit_status', 'value'),
        Input('btn_document_head_close', 'n_clicks'),
        Input("url", "search"),
    ],
    [
        State('document_name', 'value'),
        State('document_process_editmodalhead', "children"),
        State("document_submit", "children"),
        State("document_id", 'value'),
        State("document_chkmarkfordeletion", "value"),
    ]

)
def clear_doc_requirements_data(document_submit_status, btn_document_head_close, url,
              document_name, document_process_editmodalhead, document_submit, document_id, document_chkmarkfordeletion):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":
            document_id = parse_qs(parsed.query)['document_id'][0]
            sql = '''SELECT doc_requirement_name, doc_requirement_description
                       FROM document_requirements
                      WHERE doc_requirement_id=%s
                  '''
            values = (document_id,)
            columns = ['doc_requirement_name', 'doc_requirement_description']
            df = securequerydatafromdatabase(sql, values, columns)
            document_name = df["doc_requirement_name"][0]
            document_description = df["doc_requirement_description"][0]
            values = [document_name, "Edit Existing Document", "Save Changes",
                      document_id, [], {'text-align': 'middle', 'display': 'inline'}, document_description]
            return values
        elif parse_qs(parsed.query)['mode'][0] == "add":
            values = ["", document_process_editmodalhead,
                      document_submit, document_id, [], {'display': 'none'}, ""]
            return values
    else:
        raise PreventUpdate


@app.callback(
    [
        Output("document_name", "valid"),
        Output("document_name", "invalid"),
        Output('document_submit_status', "value"),
        Output('document_results_modal', "is_open"),
        Output('document_results_body', "children"),
        Output('document_results_head_close', "style"),
        Output('document_results_head_return', "style"),
    ],
    [
        Input('document_submit', 'n_clicks'),
        Input('btn_document_head_close', 'n_clicks'),
        Input('btn_document_results_head_return', 'n_clicks'),
    ],
    [
        State('current_user_id', 'data'),
        State('document_name', 'value'),
        State("document_submit", "children"),
        State("document_chkmarkfordeletion", "value"),
        State("url", "search"),
        State('document_id', 'value'),
        State('document_description', 'value'),
    ]

)
def process_doc_requirements_data(document_submit, btn_document_head_close, btn_document_results_head_return,
                current_user_id, document_name, mode, document_chkmarkfordeletion, url, document_id, document_description):
    ctx = dash.callback_context
    stylehead_close = {'display': 'none'}
    stylehead_return = {'display': 'none'}
    parsed = urlparse.urlparse(url)

    if ctx.triggered:
        validity = [
            False, False
        ]
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == 'document_submit':
            if document_name:
                is_valid_document_name = True
            else:
                is_valid_document_name = False

            validity = [
                is_valid_document_name, not is_valid_document_name,
            ]
            allvalid = [is_valid_document_name]
            if all(allvalid):
                if mode == "Save New Document":
                    sql = """
                        INSERT INTO document_requirements(doc_requirement_name, doc_requirement_delete_ind,
                        doc_requirement_modified_by, doc_requirement_modified_on, doc_requirement_description)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING doc_requirement_id
                    """
                    values = (document_name, False, current_user_id,
                              datetime.now(), document_description)
                    document_id = modifydatabasereturnid(sql, values)
                    displayed = True
                    message = "Successfully added new document"
                    status = "1"
                    stylehead_close = {'display': 'inline'}
                    stylehead_return = {'display': 'none'}
                else:
                    sql = """
                        UPDATE document_requirements
                        SET doc_requirement_name = %s,
                            doc_requirement_delete_ind= %s,
                            doc_requirement_modified_by= %s,
                            doc_requirement_modified_on= %s,
                            doc_requirement_description = %s
                        WHERE doc_requirement_id = %s
                    """
                    if '1' in document_chkmarkfordeletion:
                        fordelete = True
                    else:
                        fordelete = False
                    values = (document_name, fordelete, current_user_id,
                              datetime.now(), document_description, document_id)
                    modifydatabase(sql, values)
                    validity = [
                        False, False
                    ]
                    stylehead_close = {'display': 'none'}
                    stylehead_return = {'display': 'inline'}
                    displayed = True
                    message = "Successfully edited document"
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
        elif eventid == 'btn_document_head_close':
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
