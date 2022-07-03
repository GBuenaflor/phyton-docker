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
from apps.dbconnect import securequerydatafromdatabase, modifydatabase, modifydatabasereturnid, singularcommandupdatedatabase
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
                html.H4("Modify Documents For BP", id="bp_docs_process_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),

            dbc.Modal([
                dbc.ModalHeader("Process roles", id="bp_docs_results_head"),
                dbc.ModalBody([
                ], id="bp_docs_results_body"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Close", id="btn_bp_docs_head_close",
                                       color="primary", block=True),
                        ], id="bp_docs_results_head_close", style={'display': 'none'}),
                        dbc.Col([
                            dbc.Button("Return", id="btn_bp_docs_results_head_return",
                                       color="primary", block=True, href='/settings/settings_bp_docs'),
                        ], id="bp_docs_results_head_return", style={'display': 'none'}),
                    ], style={'width': '100%'}),
                ]),
            ], id="bp_docs_results_modal"),
            dbc.CardBody([
                dcc.Link('← Back to BP Required Documents', href='/settings/settings_bp_docs'),
                html.Br(),
                html.Br(),

                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("BP Document", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Label("Role Name", width=4, style={
                                       "text-align": "left"}, id="appt_type_name_docs_profile"),


                         ],
                            width=8
                        )],
                        row=True
                    ),
                ]),
                dbc.Card([
                    dbc.CardHeader(
                        html.H5("Document Requirement and Employee Class to Add"),
                        style={"background-color": "rgb(123,20,24)", 'color': 'white'}
                    ),
                    dbc.CardBody([
                        html.Hr(),
                        dbc.Label("Select Employee Class:", width=3, style={"text-align": "left"}),
                        dbc.Row([  # Dropdown for add employee class
                            dbc.Col([
                                dcc.Dropdown(
                                    id='ddlistofempclasses',
                                    options=[
                                    ],
                                    searchable=True,
                                    clearable=True
                                ),
                            ]),
                            dbc.Col([

                            ]),
                        ], style={'width': '100%'}),
                        html.Br(),
                        html.Br(),
                        dbc.Label("Select Document Requirement:",
                                  width=3, style={"text-align": "left"}),
                        dbc.Row([  # Dropdown for Add Selected Document
                            dbc.Col([
                                dbc.Spinner(
                                    dcc.Dropdown(
                                        id='ddlistofbpdocs',
                                        options=[
                                        ],
                                        searchable=True,
                                        clearable=True
                                    ), color='danger'
                                ),
                            ]),
                            dbc.Col([

                            ]),
                        ], style={'width': '100%'}),
                        html.Br(),
                        html.Br(),
                        html.Div([
                            dcc.Checklist(
                                options=[
                                    {'label': '  Check for Mandatory Requirement', 'value': '1'},
                                ], id='bpdocs_markchkhard', value=[]
                            ),
                        ], id='divbpdocs_chkhard',  style={'text-align': 'middle', 'display': 'inline'}),
                        html.Br(),
                        html.Br(),
                        # dbc.Row([
                        #
                        # ], style={'width': '100%'}),
                        dbc.Col([
                            dbc.Button("Add Selected Document",
                                       id="bp_docs_submit", color="info"),
                        ]),
                        dbc.Row([
                            dbc.Col([

                            ]),
                            dbc.Col([
                                # dbc.Button("Cancel", id="module_role_cancel", color="warning", className="ml-auto")
                            ]),
                        ], style={'width': '100%'}),
                        html.Br(),
                        html.Br(),
                    ], style={'line-height': "1em", "display": "block"}),
                ], color="secondary",
                    outline=True
                ),
                html.Hr(),

                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            dbc.Row([
                                dbc.Col([
                                    html.H4(
                                        "See Current Required Documents for Employee Type Selected Above:"),
                                    dbc.FormText("Select Employee Class first to display current required documents",
                                                 color="secondary",
                                                 ),
                                    html.Div([
                                        html.Div([

                                        ], id="existingbpdocsdatatableprofile"),
                                    ], style={'width': '100%', 'padding': '10px'}),
                                ]),
                            ], style={'width': '100%'}),
                        ]),
                    ])
                ], color="secondary",
                    outline=True),


            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"},

        )
    ]),
])


@app.callback([
    Output('existingbpdocsdatatableprofile', 'children'),
    Output('ddlistofbpdocs', 'options'),
    Output('appt_type_name_docs_profile', 'children'),
    Output('ddlistofempclasses', 'options'),
    Output("bpdocs_markchkhard", 'value')
],
    [
    Input("url", "search"),
    Input("bp_docs_submit", 'n_clicks'),
    Input("ddlistofempclasses", 'value')
],
    [
    State("ddlistofbpdocs", 'value'),
    State("ddlistofempclasses", 'value'),
    State("bpdocs_markchkhard", 'value'),
    State("current_user_id", 'data')

],)
def processmoduleroles(url, bp_docs_submit, empclassid, ddlistofbpdocs, ddlistofempclasses, bpdocs_markchkhard, current_user_id):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    bp_name = ""
    emp_name = ""
    if 'bp_type_id' in parse_qs(parsed.query):
        bp_type_id = parse_qs(parsed.query)['bp_type_id'][0]
        sql = "SELECT appt_type_name FROM appointment_types WHERE appt_type_id = %s "
        values = (bp_type_id,)
        columns = ["appt_type_name"]
        bp_name = securequerydatafromdatabase(sql, values, columns)["appt_type_name"][0]

    else:
        bp_type_id = "0"
    if 'emp_class_id' in parse_qs(parsed.query):
        emp_class_id = parse_qs(parsed.query)['emp_class_id'][0]
        sql = "SELECT emp_class_name FROM emp_classes WHERE emp_class_id = %s"
        values = (emp_class_id,)
        columns = ["emp_class_name"]
        emp_class_name = securequerydatafromdatabase(sql, values, columns)["emp_class_name"][0]

    else:
        emp_class_id = "0"
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'bp_docs_submit':
            if ddlistofbpdocs:
                sql = """
                    INSERT INTO bp_document_requirements (bp_type_id, bp_emp_class_id, doc_requirement_id,  bp_document_requirement_hard_required, bp_doc_requirement_inserted_by, bp_doc_requirement_inserted_on, bp_doc_requirement_delete_ind)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING bp_document_requirement_id
                """
                if '1' in bpdocs_markchkhard:
                    forhardreq = True
                else:
                    forhardreq = False

                values = (bp_type_id, ddlistofempclasses, ddlistofbpdocs, forhardreq,
                          current_user_id, datetime.now(), False)
                bp_document_requirement_id = modifydatabasereturnid(sql, values)
            else:
                raise PreventUpdate
        elif eventid == 'url':
            if 'process' in parse_qs(parsed.query):

                doc_requirement_id = parse_qs(parsed.query)['doc_requirement_id'][0]
                sql = """
                    DELETE
                      FROM bp_document_requirements
                     WHERE bp_type_id = %s
                       AND doc_requirement_id = %s
                """
                values = (bp_type_id, doc_requirement_id,)
                modifydatabase(sql, values)
                # singularcommandupdatedatabase(sql)
    else:
        pass
    df2 = queryempclasses("", emp_class_id)
    df = queryavailabledocuments("", bp_type_id, empclassid)
    table = queryaddeddocuments("", bp_type_id, ddlistofempclasses)
    return [table, df, bp_name, df2, ""]


def queryaddeddocuments(sql, bp_type_id, ddlistofempclasses):
    if ddlistofempclasses is None:
        sqlcommand = '''SELECT ec.emp_class_name, bdr.doc_requirement_id, doc_requirement_name, doc_requirement_description,
                        CASE
                            WHEN bdr.bp_document_requirement_hard_required = True THEN 'True'
                            WHEN bdr.bp_document_requirement_hard_required = False THEN 'False'
                            ELSE ''
                        END AS bp_document_requirement_hard_required
                        FROM bp_document_requirements bdr
                        INNER JOIN document_requirements dr ON dr.doc_requirement_id = bdr.doc_requirement_id
                        INNER JOIN emp_classes ec ON ec.emp_class_id = bdr.bp_emp_class_id
                        WHERE doc_requirement_delete_ind = %s
                        AND bdr.bp_type_id = %s
                        ORDER BY ec.emp_class_name ASC, doc_requirement_name ASC'''
        values = (False, bp_type_id)
    elif ddlistofempclasses is not None:
        sqlcommand = '''SELECT ec.emp_class_name, bdr.doc_requirement_id, doc_requirement_name, doc_requirement_description,
                        CASE
                            WHEN bdr.bp_document_requirement_hard_required = True THEN 'True'
                            WHEN bdr.bp_document_requirement_hard_required = False THEN 'False'
                            ELSE ''
                        END AS bp_document_requirement_hard_required
                        FROM bp_document_requirements bdr
                        INNER JOIN document_requirements dr ON dr.doc_requirement_id = bdr.doc_requirement_id
                        INNER JOIN emp_classes ec ON ec.emp_class_id = bdr.bp_emp_class_id
                        WHERE doc_requirement_delete_ind = %s
                        AND bdr.bp_type_id = %s
                        AND ec.emp_class_id = %s
                        ORDER BY ec.emp_class_name ASC, doc_requirement_name ASC'''
        values = (False, bp_type_id, ddlistofempclasses)
    columns = ["emp_class_name", "doc_requirement_id",
               "doc_requirement_name", "doc_requirement_description", "bp_document_requirement_hard_required"]
    df = securequerydatafromdatabase(sqlcommand, values, columns)
    df.columns = ["Employee Class", "Document Requirement ID",
                  "Doc Requirement Name", "Description", "Mandatory Required?"]
    # table = addcolumntodf(df, 'Delete', 'Delete', '/settings/settings_bp_docs_profile?bp_type_id=' +
    #                       bp_type_id+'&process=delete&doc_requirement_id=', "Document Requirement ID") #removed temporarily
    data_dict = df.to_dict()
    # dictionarydata = {collabel: linkcolumn}
    # data_dict.update(dictionarydata)
    df = pd.DataFrame.from_dict(data_dict)
    return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    # return table


def queryavailabledocuments(sql, bp_type_id, empclassid):
    sql = """SELECT doc_requirement_name as label, doc_requirement_id as value
       FROM document_requirements
       WHERE doc_requirement_id NOT IN (SELECT doc_requirement_id
                                          FROM bp_document_requirements
                                         WHERE bp_type_id = %s
                                           AND bp_emp_class_id = %s)
        AND doc_requirement_delete_ind = %s
	   ORDER BY doc_requirement_name
      """
    values = (bp_type_id, empclassid, False)
    columns = ['label', 'value']
    dfsql = securequerydatafromdatabase(sql, values, columns)
    return dfsql.to_dict('records')


def queryempclasses(sql, bp_type_id):
    sql = """SELECT emp_class_name as label, emp_class_id as value
        FROM emp_classes
       WHERE emp_class_id NOT IN (SELECT emp_class_id FROM bp_document_requirements WHERE bp_type_id= %s)
         AND emp_class_delete_ind = %s
         AND (emp_class_id = %s OR emp_class_id = %s OR emp_class_id = %s)
	   ORDER BY emp_class_name
      """
    values = (bp_type_id, False, 1, 2, 3)
    columns = ['label', 'value']
    dfsql = securequerydatafromdatabase(sql, values, columns)
    return dfsql.to_dict('records')


def addcolumntodf(df, collabel, label, hrefvar, pkid):
    linkcolumn = {}
    for index, row in df.iterrows():
        # hrefvar = hrefvar
        linkcolumn[index] = dcc.Link(label, href=hrefvar+str(row[pkid]))
    data_dict = df.to_dict()
    dictionarydata = {collabel: linkcolumn}
    data_dict.update(dictionarydata)
    df = pd.DataFrame.from_dict(data_dict)
    return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
