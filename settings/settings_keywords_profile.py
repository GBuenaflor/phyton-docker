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
    html.H3('Keyword Classes'),
    commonmodules.get_settings_menu(),
    #dbc.Button("Magrehistro", id="btninput2", color="primary", block=True),


    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Add Keyword Class", id = "class_keywords_editmodalhead"),
                className = 'text-white bg-dark'
            ),
            dcc.ConfirmDialog(
                id='keywordclassmessage',
            ),
            dbc.Modal([
                dbc.ModalHeader("Process Class Keywords", id = "class_keywords_results_head"),
                dbc.ModalBody([
                ], id = "class_keywords_results_body"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Close", id="btn_class_keywords_head_close", color="primary", block=True),
                        ], id="class_keywords_results_head_close", style={'display':'none'} ),
                        dbc.Col([
                            dbc.Button("Return", id="btn_results_head_return", color="primary", block=True, href ='/settings/settings_keywords'),
                        ], id="class_keywords_results_head_return", style={'display':'none'} ),
                    ], style={'width':'100%'}),
                ]),
            ], id="class_keywords_results_modal"),
            dbc.Modal([
                dbc.ModalHeader("Process Keywords", id = "keywords_results_head"),
                dbc.ModalBody([

                    dbc.Form([
                        dbc.FormGroup(
                            [dbc.Label("Keyword Name", width=2, style={"text-align":"left"}),
                            dbc.Col([
                                dbc.Input(
                                    type="text", id="keyword_name", placeholder="Enter Class Keyword Name"
                                ),
                                dbc.FormFeedback("Please enter a keyword name", valid = False)
                            ],
                            width=8
                            )],
                            row = True
                        ),

                    ]),

                ], id = "keywords_results_body"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Save", id="btn_keywords_submit", color="primary", block=True),
                        ], id="class_keywords_results_head_close", style={'display':'inline'} ),
                        dbc.Col([
                            dbc.Button("Cancel", id="btn_keywords_head_close", color="primary", block=True),
                        ], id="keywords_results_head_return", style={'display':'inline'} ),
                    ], style={'width':'100%'}),
                ]),
            ], id="keywords_results_modal", size="lg",),


            dbc.CardBody([
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("Name", width=2, style={"text-align":"left"}),
                        dbc.Col([
                            dbc.Input(
                                type="text", id="class_keyword_name", placeholder="Enter Class Keyword Name"
                            ),
                            dbc.FormFeedback("Please enter a class keyword name", valid = False)
                        ],
                        width=8
                        )],
                        row = True
                    ),
                    html.Div([
                        dcc.Checklist(
                                options=[
                                    {'label': 'Mark for Deletion?', 'value': '1'},
                                ], id='class_keyword_chkusermarkfordeletion', value=[]
                            ),
                    ],id='divclass_keyworddelete',  style={'text-align':'middle', 'display':'inline'}),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save New Class Keyword", id="class_keyword_btnsubmit", color="info", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="class_keyword_btncancel", color="warning", className="ml-auto")
                    ]),
                ], style={'width':'100%'}),
                dbc.Col([

                    html.Div([
                        dcc.Input(id='class_keyword_submitstatus', type='text', value="0")
                    ], style={'display':'none'}),
                    html.Div([
                        dcc.Input(id='class_keywordid', type='text', value="0")
                    ], style={'display':'none'}),
                    dcc.ConfirmDialog(
                        id='class_keywordmessage',
                    ),], width=2
                ),

                html.Hr(),
                html.Div([
                    html.H4("Existing Keywords"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Add New Keyword", id="add_keyword_btnsubmit", color="info", block=True),
                        ]),
                        dbc.Col([
                            dbc.Button("Delete Selected Keyword", id="delete_keyword_btnsubmit", color="info", block=True),
                        ]),
                        dbc.Col([

                        ]),
                    ], style={'width':'100%'}),
                    html.Hr(),
                    html.Div([
                        dash_table.DataTable(
                            id='dteditkeyworddatatable',
                            row_selectable="single",
                            #style_table={'overflowX': 'scroll'},
                            style_cell={
                                'minWidth': '10px', 'maxWidth': '90px',
                                'whiteSpace': 'normal'
                            },
                            css=[{
                                'selector': '.dash-cell div.dash-cell-value',
                                'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                            }],
                            )
                    ],id="editkeyworddatatable", style={'width':'50%'}),
                ],id="diveditkeyworddatatable"),

            ], style = {'line-height':"1em", "display":"block"}),
        ], style = {'line-height':"1em", "display":"block"}
        )
     ]),
])



@app.callback(
    [
        Output('keywords_results_modal','is_open'),
        Output('dteditkeyworddatatable','columns'),
        Output('dteditkeyworddatatable','data'),

        Output('keyword_name', 'value'),
        Output('dteditkeyworddatatable','selected_rows')
    ],
    [

        Input('btn_keywords_head_close', 'n_clicks'),
        Input('add_keyword_btnsubmit', 'n_clicks'),
        Input('btn_keywords_submit', 'n_clicks'),
        Input("class_keyword_submitstatus", "value"),
        Input("delete_keyword_btnsubmit", 'n_clicks'),
    ],
    [
        State('url', 'search'),
        State('keyword_name', 'value'),
        State('dteditkeyworddatatable','columns'),
        State('dteditkeyworddatatable','data'),
        State('dteditkeyworddatatable','selected_rows')
    ]
)
def processaddkeyword(btn_keywords_head_close ,add_keyword_btnsubmit,btn_keywords_submit,class_keyword_submitstatus,delete_keyword_btnsubmit,
    url,keyword_name, columns, data,selected_rows
    ):
    ctx = dash.callback_context
    df = pd.DataFrame(columns=[])

    # columns = [{"name":i, "id":i, 'editable': False} for i in df.columns]
    # data = df.to_dict("rows")
    if ctx.triggered:

        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == "btn_keywords_head_close":
            return [False,columns, data,"",[]]
            columns, data = queryallkeywordsfromclass(url)
        elif eventid == "add_keyword_btnsubmit":
            columns, data = queryallkeywordsfromclass(url)
            return [True,columns, data,"",[]]
        elif eventid == "btn_keywords_submit":

            if keyword_name:
                parsed = urlparse.urlparse(url)
                classkeywordid = parse_qs(parsed.query)['keywordclass_id'][0]
                sql = """
                    INSERT INTO keywords (keyword_class_id, keyword_name, keyword_delete_ind)
                    VALUES (%s, %s, %s)
                    RETURNING keyword_id
                """
                values = (classkeywordid, keyword_name,  False)
                classkeywordid = modifydatabasereturnid(sql,values)
                columns, data = queryallkeywordsfromclass(url)
                return [False,columns, data,"",[]]
            else:
                raise PreventUpdate
        elif eventid == "delete_keyword_btnsubmit":
            if selected_rows:
                parsed = urlparse.urlparse(url)
                classkeywordid = parse_qs(parsed.query)['keywordclass_id'][0]
                sql = """
                    UPDATE keywords SET  keyword_delete_ind = %s WHERE keyword_id = %s
                """
                values = (True,data[selected_rows[0]]["Keyword Id"])
                modifydatabase(sql,values)
                columns, data = queryallkeywordsfromclass(url)
                return [False,columns, data,"",[]]
            else:
                raise PreventUpdate
        else:
            raise PreventUpdate
    else:

        columns, data = queryallkeywordsfromclass(url)
        return [False,columns, data,"",[]]


def queryallkeywordsfromclass(url):
    parsed = urlparse.urlparse(url)
    classkeywordid = parse_qs(parsed.query)['keywordclass_id'][0]
    sql = ''' Select keyword_id, keyword_name FROM keywords
        WHERE keyword_delete_ind = %s and keyword_class_id = %s '''
    values = (False, classkeywordid)
    columns = ["keyword_id", "keyword_name"]
    df = securequerydatafromdatabase(sql, values,columns)
    df.columns = ["Keyword Id","Keyword Name"]
    columns = [{"name":i, "id":i} for i in df.columns]
    data = df.to_dict("rows")
    return columns, data





@app.callback(
    [
        Output('class_keyword_name', 'value'),

        Output("class_keywords_editmodalhead", "children"),
        Output("class_keyword_btnsubmit", "children"),
        Output("class_keywordid",'value'),
        Output("class_keyword_chkusermarkfordeletion", "value"),
        Output("divclass_keyworddelete", "style"),
        Output("diveditkeyworddatatable", "style"),
    ],
    [
        Input('class_keyword_submitstatus', 'value'),
        #Input('btnaddnewuser', 'n_clicks'),
        Input('btn_class_keywords_head_close', 'n_clicks'),
        Input("url", "search"),
    ],
    [
        State('class_keyword_name', 'value'),


        State('class_keywords_editmodalhead',"children"),
        State("class_keyword_btnsubmit", "children"),
        State("class_keywordid",'value'),
        State("class_keyword_chkusermarkfordeletion", "value"),
    ]

)
def cleardata(class_keyword_submitstatus,btn_class_keywords_head_close,url,
    class_keyword_name,class_keywords_editmodalhead,class_keyword_btnsubmit,keywordid,class_keyword_chkusermarkfordeletion):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)

    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":
            #raise PreventUpdate
            keywordid = parse_qs(parsed.query)['keywordclass_id'][0]
            sql = '''SELECT keyword_class_name FROM keyword_classes WHERE keyword_class_id=%s'''
            values = (keywordid,)
            columns = ["keyword_class_name"]
            df = securequerydatafromdatabase(sql, values,columns)

            keyword_class_name = df["keyword_class_name"][0]
            displayed = {'text-align':'middle', 'display':'inline'}
            values = [keyword_class_name,"Edit Existing Keyword:","Save Changes",keywordid,[],displayed,displayed]
            return values
        elif parse_qs(parsed.query)['mode'][0] == "add":
            values = ["",class_keywords_editmodalhead,class_keyword_btnsubmit,keywordid,[],{'display':'none'},{'display':'none'}]
            return values
            #raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback(
    [
        Output("class_keyword_name", "valid"),
        Output("class_keyword_name", "invalid"),


        Output('class_keyword_submitstatus',"value"),
        Output('class_keywords_results_modal',"is_open"),
        Output('class_keywords_results_body',"children"),
        Output('class_keywords_results_head_close',"style"),
        Output('class_keywords_results_head_return',"style"),
    ],
    [
        Input('class_keyword_btnsubmit', 'n_clicks'),
        Input('btn_class_keywords_head_close', 'n_clicks'),
        Input('btn_results_head_return', 'n_clicks'),
    ],
    [
        State('current_user_id', 'data'),
        State('class_keyword_name', 'value'),

        State("class_keyword_btnsubmit", "children"),
        State("class_keyword_chkusermarkfordeletion", "value"),
        State("url", "search"),
        State('class_keywordid', 'value'),
    ]

)
def processdata(class_keyword_btnsubmit,btn_class_keywords_head_close,btn_results_head_return,
    current_user_id, class_keyword_name, mode, class_keyword_chkusermarkfordeletion,url,keywordid):
    ctx = dash.callback_context
    stylehead_close = {'display':'none'}
    stylehead_return = {'display':'none'}
    parsed = urlparse.urlparse(url)

    if ctx.triggered:
        validity = [
            False, False
            ]
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'class_keyword_btnsubmit':
            if class_keyword_name:
                is_valid_keyword_name= True
            else:
                is_valid_keyword_name= False

            validity = [
                is_valid_keyword_name, not is_valid_keyword_name,
            ]
            allvalid = [is_valid_keyword_name]

            if all(allvalid):

                if mode =="Save New Class Keyword":
                    sql = """
                        INSERT INTO keyword_classes (keyword_class_name, keyword_class_delete_ind)
                        VALUES (%s, %s)
                        RETURNING keyword_class_id
                    """
                    values = (class_keyword_name, False)
                    keyword_id = modifydatabasereturnid(sql,values)
                    displayed = True
                    message = "Successfully added new keyword class"
                    status = "1"
                    stylehead_close = {'display':'inline'}
                    stylehead_return = {'display':'none'}
                else:
                    sql = """
                        UPDATE keyword_classes SET keyword_class_name = %s, keyword_class_delete_ind= %s WHERE
                            keyword_class_id = %s
                    """
                    if '1' in class_keyword_chkusermarkfordeletion:
                        fordelete = True
                    else:
                        fordelete= False
                    values = (class_keyword_name, fordelete,keywordid)
                    modifydatabase(sql,values)
                    validity = [
                        False, False

                        ]
                    stylehead_close = {'display':'none'}
                    stylehead_return = {'display':'inline'}
                    displayed = True
                    message = "Successfully edited keyword class"
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
        elif eventid == 'btn_class_keywords_head_close':
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
