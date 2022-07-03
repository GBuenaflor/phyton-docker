import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash
import re
from dash.dependencies import Input, Output, State, MATCH, ALL
import json
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
    html.H1("Leave Available Days"),
    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Modify Available Days For Leave Type", id="leave_available_days_process_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),

            dbc.Modal([
                dbc.ModalHeader("Modify available days for leave type", id="bp_docs_results_head"),
                dbc.ModalBody([
                ], id="leave_available_days_results_body"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Close", id="btn_leave_available_days_head_close",
                                       color="primary", block=True),
                        ], id="leave_available_days_results_head_close", style={'display': 'none'}),
                        dbc.Col([
                            dbc.Button("Return", id="btn_leave_available_days_results_head_return",
                                       color="primary", block=True, href='/settings/settings_leave_available_days'),
                        ], id="leave_available_days_results_head_return", style={'display': 'none'}),
                    ], style={'width': '100%'}),
                ]),
            ], id="leave_available_days_results_modal"),
            dbc.CardBody([
                dcc.Link('← Back to Leave Available Days', href='/settings/settings_leave_available_days'),
                html.Br(),
                html.Br(),

                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("Leave Type/Particulars", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Label(" ", width=4, style={
                                       "text-align": "left"}, id="leave_type_name_leave_available_days_profile"),


                         ],
                            width=8
                        )],
                        row=True
                    ),
                ]),
                dbc.Card([
                    dbc.CardHeader(
                        html.H5("Available Number of Days per Leave Type and Employee Class"),
                        style={"background-color": "rgb(123,20,24)", 'color': 'white'}
                    ),
                    dbc.CardBody([
                        html.Hr(),
                        dbc.Label("Select employee class:", width=3, style={"text-align": "left"}),
                        dbc.Row([  # Dropdown for add employee class
                            dbc.Col([
                                dcc.Dropdown(
                                    id='ddlistofempclass',
                                    options=[
                                    {'label': 'Faculty (Full-time)', 'value': 1},
                                    {'label': 'Admin', 'value': 2},
                                    {'label': 'REPS', 'value': 3},
                                    {'label': 'Faculty (Administrator)', 'value': 4},
                                    ],
                                    searchable=True,
                                    # clearable=True
                                ),
                                # dbc.Input(
                                #     type="text", id="leave_numdays", placeholder="Enter number of days of leave"
                                # ),
                            ]),
                            dbc.Col([

                            ]),
                        ], style={'width': '100%'}),
                        html.Br(),
                        dbc.Label("Maximum # of days of leave for this employee class:", width=3, style={"text-align": "left"}),
                        dbc.Row([  # Dropdown for add employee class
                            dbc.Col([
                                dbc.Input(
                                    type="text", id="leave_available_days_maxdays", placeholder="Enter maximum number of days"),
                                # dbc.Input(
                                #     type="text", id="leave_numdays", placeholder="Enter number of days of leave"
                                # ),
                            ]),
                            dbc.Col([

                            ]),
                        ], style={'width': '100%'}),
                        html.Br(),
                        html.Br(),
                        dbc.Label("Working / Calendar Days:", width=3, style={"text-align": "left"}),
                        dbc.Row([  # Dropdown for add employee class
                            dbc.Col([
                                dcc.Dropdown(
                                    id='ddworkingcalendardays',
                                    options=[
                                    {'label': 'Working Day/s', 'value': 1},
                                    {'label': 'Calendar Day/s', 'value': 2},
                                    {'label': 'Not applicable', 'value': 3},

                                    ],
                                    searchable=True,
                                    # clearable=True
                                ),
                                # dbc.Input(
                                #     type="text", id="leave_numdays", placeholder="Enter number of days of leave"
                                # ),
                            ]),
                            dbc.Col([

                            ]),
                        ], style={'width': '100%'}),
                        html.Br(),
                        html.Br(),
                        dbc.Label("Remarks", width=3, style={"text-align": "left"}),
                        dbc.Row([  # Dropdown for add employee class
                            dbc.Col([
                                dbc.Textarea(
                                    id="leave_available_days_remarks",
                                    placeholder="Enter here",
                                    style={"height": "270px"},  # add
                                    bs_size="lg",
                                    className="mb-3",
                                    maxLength = 2000),
                                # dbc.Input(
                                #     type="text", id="leave_numdays", placeholder="Enter number of days of leave"
                                # ),
                            ]),
                            dbc.Col([

                            ]),
                        ], style={'width': '100%'}),
                        html.Br(),
                        html.Br(),

                        # dbc.Label("Select Document Requirement:",
                        #           width=3, style={"text-align": "left"}),
                        # dbc.Row([  # Dropdown for Add Selected Document
                        #     dbc.Col([
                        #         dbc.Spinner(
                        #             dcc.Dropdown(
                        #                 id='ddlistofleavedocs',
                        #                 options=[
                        #                 ],
                        #                 searchable=True,
                        #                 clearable=True
                        #             ), color='danger'
                        #         ),
                        #     ]),
                        #     dbc.Col([
                        #
                        #     ]),
                        # ], style={'width': '100%'}),
                        # html.Br(),
                        # html.Br(),
                        # html.Div([
                        #     dcc.Checklist(
                        #         options=[
                        #             {'label': '  Check for Mandatory Requirement', 'value': '1'},
                        #         ], id='bpdocs_markchkhard', value=[]
                        #     ),
                        # ], id='divbpdocs_chkhard',  style={'text-align': 'middle', 'display': 'inline'}),
                        # html.Br(),
                        # html.Br(),
                        # html.Div([
                        #     dcc.Checklist(
                        #         options=[
                        #             {'label': '  Check for Mandatory Requirement', 'value': '1'},
                        #         ], id='leavedocs_markchkhard', value=[]
                        #     ),
                        # ], id='divleavedocs_chkhard',  style={'text-align': 'middle', 'display': 'inline'}),
                        html.Br(),
                        html.Br(),
                        # dbc.Row([
                        #
                        # ], style={'width': '100%'}),
                        dbc.Col([
                            dbc.Button("Add Maximum # of Days",
                                       id="leave_available_days_submit", color="info"),
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
                                        "See Maximum # of Days per Employee Class:"),
                                    # dbc.FormText("Select # of days of leave first to display current required documents",
                                    #              color="secondary",
                                    #              ),
                                    html.Div([
                                        html.Div([

                                        ], id="leave_available_days_datatableprofile"),
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
    Output('leave_available_days_datatableprofile', 'children'),
    # Output('ddlistofempclass', 'options'),
    Output('leave_type_name_leave_available_days_profile', 'children'),
    # Output("leavedocs_markchkhard", 'value')
    # Output('ddlistofdays', 'options'),
    # Output("bpdocs_markchkhard", 'value')
],
    [
    Input("url", "search"),
    Input("leave_available_days_submit", 'n_clicks'),
    Input({'type': 'dynamic_delete_days', 'index': ALL}, 'n_clicks'),
    # Input("ddlistofdays", 'value')
],
    [
    State("ddlistofempclass", 'value'),
    State("leave_available_days_maxdays", 'value'),
    State("ddworkingcalendardays", 'value'),
    State("leave_available_days_remarks", 'value'),
    # State("leavedocs_markchkhard", 'value'),
    # State("bpdocs_markchkhard", 'value'),
    State("current_user_id", 'data')

],)
def processmoduleroles(url, leave_available_days_submit, dynamic_delete_days,
    # empclassid,
    ddlistofempclass, leave_available_days_maxdays, ddworkingcalendardays, leave_available_days_remarks,
    # leavedocs_markchkhard,
    # ddlistofempclasses, bpdocs_markchkhard,
    current_user_id):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    leave_name = ""
    num_days = ""
    if 'leave_type_id' in parse_qs(parsed.query):
        leave_type_id = parse_qs(parsed.query)['leave_type_id'][0]
        sql = "SELECT leave_type_name FROM leave_types WHERE leave_type_id = %s AND leave_type_delete_ind = %s"
        values = (leave_type_id, False)
        columns = ["leave_type_name"]
        leave_name = securequerydatafromdatabase(sql, values, columns)["leave_type_name"][0]

    else:
        leave_type_id = "0"
    # if 'emp_class_id' in parse_qs(parsed.query):
    #     emp_class_id = parse_qs(parsed.query)['emp_class_id'][0]
    #     sql = "SELECT emp_class_name FROM emp_classes WHERE emp_class_id = %s"
    #     values = (emp_class_id,)
    #     columns = ["emp_class_name"]
    #     emp_class_name = securequerydatafromdatabase(sql, values, columns)["emp_class_name"][0]
    #
    # else:
    #     emp_class_id = "0"
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'leave_available_days_submit':
            if ddlistofempclass:
                sql = """
                    INSERT INTO leave_available_days (leave_type_id, leave_emp_class_mod_id, leave_num_days_avail, leave_type_of_day_id, leave_available_remarks, leave_available_inserted_by, leave_available_inserted_on, leave_available_delete_ind)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING leave_available_id
                """
                # if '1' in leavedocs_markchkhard:
                #     forhardreq = True
                # else:
                #     forhardreq = False


                values = (leave_type_id, ddlistofempclass, leave_available_days_maxdays, ddworkingcalendardays, leave_available_days_remarks,
                          current_user_id, datetime.now(), False)
                leave_available_id = modifydatabasereturnid(sql, values)
            else:
                raise PreventUpdate
        elif eventid == 'url':
            if 'process' in parse_qs(parsed.query):

                leave_type_id = parse_qs(parsed.query)['leave_type_id'][0]
                leave_emp_class_mod_id = parse_qs(parsed.query)['leave_emp_class_mod_id'][0]
                sql = """
                    UPDATE leave_available_days
                    SET leave_available_delete_ind = True
                    where leave_type_id = """+leave_type_id+""" and leave_emp_class_mod_id = """+leave_emp_class_mod_id+"""

                """
                # values = (True, leave_type_id, doc_requirement_id)
                singularcommandupdatedatabase(sql)
                # singularcommandupdatedatabase(sql)
        else:
            index = json.loads(eventid)["index"]
            type = json.loads(eventid)["type"]
            # user_id = parse_qs(parsed.query)['user_id'][0]
            leave_type_id = parse_qs(parsed.query)['leave_type_id'][0]
            print(index, 'index')
            print(type, 'type')

            if type=="dynamic_delete_days":
                values=[True, index, leave_type_id]
                sqlupdate = ''' UPDATE leave_available_days
                        SET leave_available_delete_ind = %s
                        where leave_available_id = %s and leave_type_id = %s
                        '''
                modifydatabase(sqlupdate, values) #AND user_role_unit_id = %s
    else:
        pass
    # df2 = queryempclasses("", emp_class_id)
    # df = queryavailableempclass("", leave_type_id, ddlistofempclass) ###
    table = queryaddeddocuments("", leave_type_id, ddlistofempclass)
    return [table, leave_name]


def queryaddeddocuments(sql, leave_type_id, ddlistofempclass):
    sqlcommand = '''SELECT lad.leave_available_id,
                CASE WHEN leave_emp_class_mod_id = 1 THEN 'Faculty (Full-time)'
                WHEN leave_emp_class_mod_id = 2 THEN 'Admin'
                WHEN leave_emp_class_mod_id = 3 THEN 'REPS'
                WHEN leave_emp_class_mod_id = 4 THEN 'Faculty (Administrator)'
                ELSE '' END AS leave_emp_class_mod,

                leave_num_days_avail,
                CASE WHEN leave_type_of_day_id = 1 THEN 'Working Day/s'
                WHEN leave_type_of_day_id = 2 THEN 'Calendar Day/s'
                WHEN leave_type_of_day_id = 3 THEN 'Not Applicable'
                ELSE '' END AS leave_type_of_day,
                leave_available_remarks
                FROM leave_available_days lad
                WHERE leave_available_delete_ind = %s
                AND lad.leave_type_id = %s
                ORDER BY lad.leave_available_id ASC'''
    values = (False, leave_type_id)

    columns = ["lad.leave_available_id",
               "leave_emp_class_mod", "leave_num_days_avail", "leave_type_of_day", "leave_available_remarks"]
    df = securequerydatafromdatabase(sqlcommand, values, columns)
    df.columns = ["Leave Available ID",
                  "Employee Class", "Maximum # of Days", "Type of Day", 'Remarks']
    table = addcolumntodf(df, 'Delete', 'Delete')
    # table = addcolumntodf(df, 'Delete', 'Delete', '/settings/settings_leave_docs_profile?leave_type_id=' +
    #                       leave_type_id+'&process=delete&doc_requirement_id=', "Document Requirement ID")
    return table

    ###old
    # sqlcommand = '''SELECT ldr.leave_document_requirement_id, doc_requirement_name, doc_requirement_description,
    #                 CASE WHEN leave_numdays = 1.000 THEN 'Less than or equal to 5 days'
    #                 WHEN leave_numdays = 5.000 THEN 'More than 5 days'
    #                 WHEN leave_numdays = 30.000 THEN 'More than 1 month'
    #                 ELSE 'Any # of day' END AS leave_numdays,
    #                 CASE WHEN leave_doc_is_with_pay = 1 THEN 'With Pay'
    #                 WHEN leave_doc_is_with_pay = 2 THEN 'Without Pay'
    #                 ELSE 'With/Without Pay' END AS leave_doc_is_with_pay,
    #                 CASE WHEN leave_doc_is_advanced_filing = 1 THEN 'Yes'
    #                 WHEN leave_doc_is_advanced_filing = 2THEN 'No'
    #                 ELSE 'Any (regardless if advanced filing or not)' END AS leave_doc_is_advanced_filing,
    #
    #                 CASE WHEN ldr.leave_document_requirement_hard_required = True THEN 'True'
    #                 WHEN ldr.leave_document_requirement_hard_required = False THEN 'False'
    #                 ELSE ''
    #                 END AS leave_document_requirement_hard_required
    #
    #                 FROM leave_document_requirements ldr
    #                 INNER JOIN document_requirements dr ON dr.doc_requirement_id = ldr.doc_requirement_id
    #
    #                 WHERE doc_requirement_delete_ind = %s
    #                 AND leave_doc_requirement_delete_ind = %s
    #                 AND ldr.leave_type_id = %s
    #                 ORDER BY doc_requirement_name ASC'''
    # values = (False, False, leave_type_id)
    #
    # # if ddlistofdays is None:
    # #     sqlcommand = '''SELECT ldr.leave_document_requirement_id, doc_requirement_name, doc_requirement_description,
    # #                     CASE WHEN leave_numdays = 1.000 THEN 'Less than or equal to 5 days'
    # #                     WHEN leave_numdays = 5.000 THEN 'More than 5 days'
    # #                     WHEN leave_numdays = 30.000 THEN 'More than 1 month'
    # #                     ELSE 'Any # of day' END AS leave_numdays,
    # #                     CASE WHEN leave_doc_is_with_pay = 1 THEN 'With Pay'
    # #                     WHEN leave_doc_is_with_pay = 2 THEN 'Without Pay'
    # #                     ELSE 'With/Without Pay' END AS leave_doc_is_with_pay,
    # #                     CASE WHEN leave_doc_is_advanced_filing = 1 THEN 'Yes'
    # #                     WHEN leave_doc_is_advanced_filing = 2THEN 'No'
    # #                     ELSE 'Any (regardless if advanced filing or not)' END AS leave_doc_is_advanced_filing,
    # #
    # #                     CASE WHEN ldr.leave_document_requirement_hard_required = True THEN 'True'
    # #                     WHEN ldr.leave_document_requirement_hard_required = False THEN 'False'
    # #                     ELSE ''
    # #                     END AS leave_document_requirement_hard_required
    # #
    # #                     FROM leave_document_requirements ldr
    # #                     INNER JOIN document_requirements dr ON dr.doc_requirement_id = ldr.doc_requirement_id
    # #
    # #                     WHERE doc_requirement_delete_ind = %s
    # #                     AND leave_doc_requirement_delete_ind = %s
    # #                     AND ldr.leave_type_id = %s
    # #                     ORDER BY doc_requirement_name ASC'''
    # #     values = (False, False, leave_type_id)
    # # elif ddlistofdays is not None:
    # #     sqlcommand = '''SELECT ldr.leave_document_requirement_id, doc_requirement_name, doc_requirement_description,
    # #                     CASE  WHEN leave_numdays = 1.000 THEN 'Less than or equal to 5 days'
    # #                     WHEN leave_numdays = 5.000 THEN 'More than 5 days'
    # #                     WHEN leave_numdays = 30.000 THEN 'More than 1 month'
    # #                     ELSE 'Any # of day' END AS leave_numdays,
    # #                     CASE WHEN leave_doc_is_with_pay = 1 THEN 'With Pay'
    # #                     WHEN leave_doc_is_with_pay = 2 THEN 'Without Pay'
    # #                     ELSE 'With/Without Pay' END AS leave_doc_is_with_pay,
    # #                     CASE WHEN leave_doc_is_advanced_filing = 1 THEN 'Yes'
    # #                     WHEN leave_doc_is_advanced_filing = 2THEN 'No'
    # #                     ELSE 'Any (regardless if advanced filing or not)' END AS leave_doc_is_advanced_filing,
    # #
    # #                     CASE WHEN ldr.leave_document_requirement_hard_required = True THEN 'True'
    # #                     WHEN ldr.leave_document_requirement_hard_required = False THEN 'False'
    # #                     ELSE ''
    # #                     END AS leave_document_requirement_hard_required
    # #
    # #                     FROM leave_document_requirements ldr
    # #                     INNER JOIN document_requirements dr ON dr.doc_requirement_id = ldr.doc_requirement_id
    # #
    # #                     WHERE doc_requirement_delete_ind = %s
    # #                     AND leave_doc_requirement_delete_ind = %s
    # #                     AND ldr.leave_type_id = %s
    # #                     AND leave_numdays = %s
    # #                     ORDER BY doc_requirement_name ASC'''
    # #     values = (False, False, leave_type_id, ddlistofdays)
    # columns = ["leave_document_requirement_id",
    #            "doc_requirement_name", "doc_requirement_description", "leave_numdays", "leave_doc_is_with_pay", "leave_doc_is_advanced_filing", "leave_document_requirement_hard_required"]
    # df = securequerydatafromdatabase(sqlcommand, values, columns)
    # df.columns = ["Leave Document Requirement ID",
    #               "Doc Requirement Name", "Description", "# of Days of Leave", 'With/Without Pay', 'Advanced Filing?', 'Mandatory Required?']
    # table = addcolumntodf(df, 'Delete', 'Delete')
    # # table = addcolumntodf(df, 'Delete', 'Delete', '/settings/settings_leave_docs_profile?leave_type_id=' +
    # #                       leave_type_id+'&process=delete&doc_requirement_id=', "Document Requirement ID")
    # return table


def queryavailabledocuments(sql, leave_type_id, ddlistofempclass):
    # sql = """SELECT doc_requirement_name as label, doc_requirement_id as value
    #    FROM document_requirements
    #    WHERE doc_requirement_id NOT IN (SELECT doc_requirement_id
    #                                       FROM leave_document_requirements
    #                                      WHERE leave_type_id = %s
    #                                        AND leave_numdays = %s)
    #     AND doc_requirement_delete_ind = %s
	#    ORDER BY doc_requirement_name
    #   """
    sql = """SELECT doc_requirement_name as label, doc_requirement_id as value
       FROM document_requirements
       WHERE doc_requirement_delete_ind = %s
	   ORDER BY doc_requirement_name
      """
    values = (False,)
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


def addcolumntodf(df, collabel, label): #, hrefvar, pkid):
    linkcolumn = {}
    for index, row in df.iterrows():
        # hrefvar = hrefvar
        linkcolumn[index] =  dbc.Button("Delete",id={'index':str(row["Leave Available ID"]), 'type': 'dynamic_delete_days'}, color="primary", className="mr-1", block=True )
        # dcc.Link(label, href=hrefvar+str(row[pkid]))
    data_dict = df.to_dict()
    dictionarydata = {collabel: linkcolumn}
    data_dict.update(dictionarydata)
    df = pd.DataFrame.from_dict(data_dict)
    return dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
