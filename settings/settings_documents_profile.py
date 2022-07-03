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
                html.H4("Add New Document", id = "document_process_editmodalhead_set"),
                style={"background-color": "rgb(123,20,24)", 'color':'white'}
            ),
            dcc.ConfirmDialog(
                id='document_usermessage',
            ),
            dbc.Modal([
                dbc.ModalHeader("Process Documents", id = "document_results_head"),
                dbc.ModalBody([
                ], id = "document_results_body_set"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Close", id="btn_document_head_close", color="primary", block=True),
                        ], id="documents_results_head_close_set", style={'display':'none'} ),
                        dbc.Col([
                            dbc.Button("Return", id="btn_document_results_head_return", color="primary", block=True, href ='/settings/settings_documents'),
                        ], id="documents_results_head_return_set", style={'display':'none'} ),
                    ], style={'width':'100%'}),
                ]),
            ], id="documents_results_modal_set"),
            dbc.CardBody([
                dcc.Link('← Back to Documents', href='/settings/settings_documents'),
                html.Br(),
                html.Br(),
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("Document Name", width=2, style={"text-align":"left"}),
                        dbc.Col([
                            dbc.Input(
                                type="text", id="document_name_set", placeholder="Enter document Name"
                            ),
                            dbc.FormFeedback("Too short, already taken, or has spaces", valid = False)
                        ],
                        width=8
                        )],
                        row = True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Document Submission Instructions", width=2, style={"text-align":"left"}),
                        dbc.Col([
                            dbc.Input(
                                type="text", id="document_name_inst", placeholder="Enter document submission instructions"
                            ),
                            dbc.FormFeedback("Too short, already taken, or has spaces", valid = False)
                        ],
                        width=8
                        )],
                        row = True
                    ),

                    html.Div([
                        dcc.Checklist(
                                options=[
                                    {'label': 'Mark for Deletion?', 'value': '1'},
                                ], id='document_chkmarkfordeletion_set', value=[]
                            ),
                    ],id='divdocumentdelete_set',  style={'text-align':'middle', 'display':'inline'}),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save New document", id="document_submit_set", color="info", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="document_cancel", color="warning", className="ml-auto")
                    ]),
                ], style={'width':'100%'}),
                dbc.Col([

                    html.Div([
                        dcc.Input(id='document_submit_set_status', type='text', value="0")
                    ], style={'display':'none'}),
                    html.Div([
                        dcc.Input(id='document_id_set', type='text', value="0")
                    ], style={'display':'none'}),
                    dcc.ConfirmDialog(
                        id='document_message',
                    ),], width=2
                )
            ], style = {'line-height':"1em", "display":"block"}),
        ], style = {'line-height':"1em", "display":"block"}
        )
     ]),
])

@app.callback(
    [
        Output('document_name_set', 'value'),
        Output("document_process_editmodalhead_set", "children"),
        Output("document_submit_set", "children"),
        Output("document_id_set",'value'),
        Output("document_chkmarkfordeletion_set", "value"),
        Output("divdocumentdelete_set", "style"),
        Output('document_name_inst','value'),
    ],
    [
        Input('document_submit_set_status', 'value'),
        Input('btn_document_head_close', 'n_clicks'),
        Input("url", "search"),
    ],
    [
        State('document_name_set', 'value'),
        State('document_process_editmodalhead_set',"children"),
        State("document_submit_set", "children"),
        State("document_id_set",'value'),
        State("document_chkmarkfordeletion_set", "value"),
        State('document_name_inst','value'),
    ]

)
def clear_documents_data(document_submit_set_status,btn_document_head_close,url,
    document_name_set, document_process_editmodalhead_set,document_submit_set,document_id_set,document_chkmarkfordeletion_set,document_name_inst):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":
            document_id_set = parse_qs(parsed.query)['doc_id'][0]
            sql = '''SELECT doc_name, doc_instructions FROM documents WHERE doc_id=%s'''
            values = (document_id_set, )
            columns = ['document_name','doc_instructions']
            df = securequerydatafromdatabase(sql,values,columns)
            document_name_set = df["document_name"][0]
            doc_instructions = df["doc_instructions"][0]
            values = [document_name_set,"Edit Existing document:","Save Changes",document_id_set,[],{'text-align':'middle', 'display':'inline'},doc_instructions]
            return values
        elif parse_qs(parsed.query)['mode'][0] == "add":
            values = ["",document_process_editmodalhead_set,document_submit_set,document_id_set,[],{'display':'none'},""]
            return values
    else:
        raise PreventUpdate

@app.callback(
    [
        Output("document_name_set", "valid"),
        Output("document_name_set", "invalid"),
        Output('document_submit_set_status',"value"),
        Output('documents_results_modal_set',"is_open"),
        Output('document_results_body_set',"children"),
        Output('documents_results_head_close_set',"style"),
        Output('documents_results_head_return_set',"style"),
    ],
    [
        Input('document_submit_set', 'n_clicks'),
        Input('btn_document_head_close', 'n_clicks'),
        Input('btn_document_results_head_return', 'n_clicks'),
    ],
    [
        State('current_user_id', 'data'),
        State('document_name_set', 'value'),
        State("document_submit_set", "children"),
        State("document_chkmarkfordeletion_set", "value"),
        State("url", "search"),
        State('document_id_set', 'value'),
        State('document_name_inst','value'),
    ]

)
def process_documents_data(document_submit_set,btn_document_head_close,btn_document_results_head_return,
    current_user_id, document_name_set, mode, document_chkmarkfordeletion_set,url,document_id_set,document_name_inst):
    ctx = dash.callback_context
    stylehead_close = {'display':'none'}
    stylehead_return = {'display':'none'}
    parsed = urlparse.urlparse(url)

    if ctx.triggered:
        validity = [
            False, False
            ]
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'document_submit_set':
            if document_name_set:
                is_valid_document_name_set= True
            else:
                is_valid_document_name_set= False

            validity = [
                is_valid_document_name_set, not is_valid_document_name_set,

            ]
            allvalid = [is_valid_document_name_set]
            if all(allvalid):
                if mode =="Save New document":
                    sql = """
                        INSERT INTO documents (doc_name, doc_delete_ind,
                        doc_inserted_by, doc_inserted_on, doc_instructions)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING doc_id
                    """
                    values = (document_name_set, False, current_user_id, datetime.now(),document_name_inst)
                    document_id_set = modifydatabasereturnid(sql,values)
                    displayed = True
                    message = "Successfully added new document"
                    status = "1"
                    stylehead_close = {'display':'inline'}
                    stylehead_return = {'display':'none'}
                else:
                    sql = """
                        UPDATE documents SET doc_name = %s,
                            doc_delete_ind= %s, doc_inserted_by= %s, doc_inserted_on= %s, doc_instructions=%s WHERE
                            doc_id = %s
                    """
                    if '1' in document_chkmarkfordeletion_set:
                        fordelete = True
                    else:
                        fordelete= False
                    values = (document_name_set, fordelete, current_user_id, datetime.now(), document_name_inst,document_id_set)
                    modifydatabase(sql,values)
                    validity = [
                        False, False
                        ]
                    stylehead_close = {'display':'none'}
                    stylehead_return = {'display':'inline'}
                    displayed = True
                    message = "Successfully edited document"
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
        elif eventid == 'btn_document_head_close':
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
