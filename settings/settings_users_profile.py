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
                html.H4("Add New User", id="users_userprocess_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dcc.ConfirmDialog(
                id='users_usermessage',
            ),
            dbc.Modal([
                dbc.ModalHeader("Process Users", id="users_results_head"),
                dbc.ModalBody([
                ], id="users_results_body"),
                dbc.ModalFooter([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Close", id="btn_results_head_close",
                                       color="primary", block=True),
                        ], id="users_results_head_close", style={'display': 'none'}),
                        dbc.Col([
                            dbc.Button("Return", id="btn_results_head_return",
                                       color="primary", block=True, href='/settings/settings_users'),
                        ], id="users_results_head_return", style={'display': 'none'}),
                    ], style={'width': '100%'}),
                ]),
            ], id="users_results_modal"),
            dbc.CardBody([
                dcc.Link('← Back to Users', href='/settings/settings_users'),
                html.Br(),
                html.Br(),
                dbc.Form([
                    dbc.FormGroup(
                        [
                            dbc.Label("Select Person to Link", width=2,
                                      style={"text-align": "left"}),
                            dbc.Col([

                                dcc.Dropdown(
                                    id="users_persondd"
                                ),
                                dbc.FormFeedback(
                                    "Please select a person to link to the user",
                                    valid=False),
                                dbc.FormText(
                                    "You can leave this blank if no person is to be linked.",
                                    color="secondary",
                                ),
                            ],
                                width=8
                            )
                        ],
                        row=True,
                        id = 'users_persondd_formgroup'
                    ),
                    dbc.FormGroup(
                        [
                            dbc.Label("Linked Person:", width=2,
                                      style={"text-align": "left"}),
                            dbc.Col([
                                # html.H1(
                                #         children = 'N/A', id='users_persondd2',
                                # ),
                                dcc.Dropdown(children = 'N/A',
                                    id="users_persondd2"
                                ),
                                dbc.FormFeedback(
                                    "Please select a person to link to the user",
                                    valid=False),
                                dbc.FormText(
                                    "",
                                    color = "secondary",
                                    id = "users_persondd2_form_text"
                                ),
                            ],
                                width=8
                            )
                        ],
                        row=True,
                        id = 'users_persondd2_formgroup'
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Username*", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="users_username", placeholder="Enter username"
                             ),
                             dbc.FormFeedback(
                                 "Too short, already taken, or has spaces", valid=False)
                         ],
                            width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Password*", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="password", id="users_password", placeholder="Enter password"
                             ),
                             dbc.FormFeedback(
                                 "Passwords must be at least 6 characters", valid=False)
                         ], width=8
                        )],
                        row=True
                    ),
                    dbc.FormGroup(
                        [dbc.Label("Confirm Password*", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="password", id="users_confirm_password", placeholder="Enter password"
                             ),
                             dbc.FormFeedback("Passwords must match", valid=False)
                         ], width=8
                        )],
                        row=True
                    ),
                    html.Div(
                        [dbc.FormGroup([
                            dbc.Label("Person currently linked:", width=2,
                                      style={"text-align": "left"}),
                            dbc.Col([
                                    dbc.Label(id="users_person_linked", style={"font-weight": "bold", "text-decoration": "underline", "font-size": "1.25vw"}
                                              ),
                                    ], width=10)
                        ], row=True),
                        ], id='div_users_person_linked', style={"display": "none"},
                    ),
                    dbc.FormGroup(
                        [
                            dbc.Label("Last Name*", width=2, style={"text-align": "left"}),
                            dbc.Col([
                                dbc.Input(
                                    type="text", id="users_lname", placeholder="Enter last name"
                                ),
                                dbc.FormFeedback("Please enter your last name", valid=False)
                            ],
                                width=8
                            )
                        ],
                        row=True
                    ),
                    dbc.FormGroup(
                        [
                            dbc.Label("First Name*", width=2, style={"text-align": "left"}),
                            dbc.Col([
                                dbc.Input(
                                    type="text", id="users_fname", placeholder="Enter first name"
                                ),
                                dbc.FormFeedback("Please enter your first name", valid=False)
                            ],
                                width=8
                            )
                        ],
                        row=True
                    ),
                    dbc.FormGroup(
                        [
                            dbc.Label("Middle Name", width=2, style={"text-align": "left"}),
                            dbc.Col([
                                dbc.Input(
                                    type="text", id="users_mname", placeholder="Enter middle name"
                                ),
                                dbc.FormFeedback("Please enter your middle name", valid=False)
                            ],
                                width=8
                            )
                        ],
                        row=True
                    ),

                    dbc.FormGroup(
                        [
                            dbc.Label("Name Extension (Suffix)", width=2,
                                      style={"text-align": "left"}),
                            dbc.Col([
                                dbc.Input(
                                    type="text", id="users_extensionname", placeholder="Enter suffix"
                                ),
                                dbc.FormFeedback("Please enter your name extension", valid=False)
                            ],
                                width=8
                            )
                        ],
                        row=True
                    ),
                    dbc.FormGroup(
                        [
                            dbc.Label("UP E-mail*", width=2, style={"text-align": "left"}),
                            dbc.Col([
                                dbc.Input(
                                    type="text", id="users_upemail", placeholder="Enter UP e-mail"
                                ),
                                dbc.FormFeedback(
                                    "Please enter correct UP e-mail or UP e-mail has already been registered", valid=False)
                            ],
                                width=8
                            )
                        ],
                        row=True
                    ),
                    html.Div([
                        dcc.Checklist(
                            options=[
                                {'label': ' Mark for Deletion?', 'value': '1'},
                            ], id='users_chkusermarkfordeletion', value=[]
                        ),
                    ], id='divuserdelete',  style={'text-align': 'middle', 'display': 'inline'}),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save New User", id="users_btnsubmituser",
                                   color="primary", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="users_btncancelsubmituser",
                                   color="secondary", className="ml-auto", href='/settings/settings_users')
                    ]),
                ], style={'width': '100%'}),
                dbc.Col([

                    html.Div([
                        dcc.Input(id='users_usersubmitstatus', type='text', value="0")
                    ], style={'display': 'none'}),
                    html.Div([
                        dcc.Input(id='users_userid', type='text', value="0")
                    ], style={'display': 'none'}),
                    dcc.ConfirmDialog(
                        id='usermessage',
                    ), ], width=2
                )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


# #
# @app.callback(
#     [
#         Output("divuserdelete", "style"),
#         Output("password", "disabled"),
#         Output("confirm_password", "disabled"),
#     ],
#     [
#         Input("btnsubmituser", "children"),
#     ],
# )
# def changeuserdivdisplay(mode):
#     if mode =="Save Changes":
#         return [{'text-align':'middle', 'display':'inline'}, True,True]
#     else:
#         return [{'display':'none'}, False,False]
#
#
# #
@app.callback(
    [
        Output('users_username', 'value'),
        Output('users_password', 'value'),
        Output('users_confirm_password', 'value'),
        Output('users_fname', 'value'),
        Output('users_lname', 'value'),
        Output('users_mname', 'value'),
        Output('users_extensionname', 'value'),
        Output('users_upemail', 'value'),
        # Output('users_person_linked', 'children'),
        Output("users_userprocess_editmodalhead", "children"),
        Output("users_btnsubmituser", "children"),
        Output("users_userid", 'value'),
        Output("users_chkusermarkfordeletion", "value"),
        Output("divuserdelete", "style"),
        Output("users_password", "disabled"),
        Output("users_confirm_password", "disabled"),
        Output('users_persondd_formgroup', 'style'),
        Output('users_persondd2_formgroup', 'style'),
        Output('users_persondd2', 'value'),
        Output('users_persondd2_form_text', 'children')
    ],
    [
        Input('users_usersubmitstatus', 'value'),
        # Input('btnaddnewuser', 'n_clicks'),
        Input('users_btncancelsubmituser', 'n_clicks'),
        Input("url", "search"),
        Input('users_persondd', 'value'),
    ],
    [
        State('users_username', 'value'),
        State('users_password', 'value'),
        State('users_confirm_password', 'value'),
        State('users_fname', 'value'),
        State('users_lname', 'value'),
        State('users_mname', 'value'),
        State('users_upemail', 'value'),
        State('users_userprocess_editmodalhead', "children"),
        State("users_btnsubmituser", "children"),
        State("users_userid", 'value'),
        State("users_chkusermarkfordeletion", "value"),
    ]

)
def clear_users_data(usersubmitstatus, btncancelsubmitpatient, url, users_persondd,
              username, pword, cpword, fname, lname, mname, upemail,
              userprocess_editmodalhead, btnsubmituser, userid, chkusermarkfordeletion):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":
            userid = parse_qs(parsed.query)['uid'][0]
            sql = '''SELECT user_name, user_password, user_first_name, user_last_name, user_middle_name, user_name_extension,
                     user_first_name || ' ' || CASE WHEN user_middle_name IS NULL THEN '' ELSE user_middle_name END || ' ' || CASE WHEN user_name_extension IS NULL THEN '' ELSE user_name_extension END || user_last_name AS "Person Name",
                     user_up_email, person_id
                       FROM users
                      WHERE user_id = %s'''
            values = (userid,)
            columns = ["user_name", "user_password", "user_first_name",
                       "user_last_name", "user_middle_name", "user_name_extension", "Person Name", "user_up_email", "person_id"]
            df = securequerydatafromdatabase(sql, values, columns)

            username = df["user_name"][0]
            password = df["user_password"][0]
            fname = df["user_first_name"][0]
            lname = df["user_last_name"][0]
            mname = df["user_middle_name"][0]
            extensionname = df["user_name_extension"][0]
            upemail = df["user_up_email"][0]
            person_id = df["person_id"][0]

            users_persondd2_form_text = ""
            if person_id is None:
                person_id = 0
                users_persondd2_form_text = "There is no linked person."


            # sqlpersons = ''' SELECT person_first_name || ' ' || CASE WHEN person_middle_name IS NULL THEN '' ELSE person_middle_name END || ' ' || CASE WHEN person_name_extension IS NULL THEN '' ELSE person_name_extension END || person_last_name AS "full_name"
            #             FROM persons per
            #           INNER JOIN employees emp ON emp.person_id = per.person_id
            #            WHERE person_delete_ind = %s
            #              AND per.person_id = %s
            #         ORDER BY person_last_name ASC
            #     '''
            #
            # valuespersons = (False, int(person_id),)
            # columnspersons = ["full_name", ]
            # dfpersons = securequerydatafromdatabase(sqlpersons, valuespersons, columnspersons)
            #
            # try:
            #     person_full_name = dfpersons["full_name"][0]
            # except:
            #     person_full_name = 'N/A'

            # else:
            #     person_full_name = 'N/A'
                # try:
                #     lname = df["person_last_name"][0]
                # except:
                #     lname = ''
                # try:
                #     fname = df["person_first_name"][0]
                # except:
                #     fname = ''
                # try:
                #     extensionname = df["person_name_extension"][0]
                # except:
                #     extensionname = ''
                # try:
                #     mname = df["person_middle_name"][0]
                # except:
                #     mname = ''

            values = [username, password, password, fname, lname, mname, extensionname, upemail, "Edit Existing User",
                      "Save Changes", userid, [], {'text-align': 'middle', 'display': 'inline'}, True, True, {'display': 'none'}, {}, person_id, users_persondd2_form_text]
            return values
        elif parse_qs(parsed.query)['mode'][0] == "add":
            if users_persondd:
                sql = ''' SELECT person_last_name, person_first_name, person_name_extension, person_middle_name
                            FROM persons per
                           WHERE person_delete_ind = %s
                             AND per.person_id = %s
                        ORDER BY person_last_name ASC
                    '''
                values = (False, users_persondd,)
                columns = ["person_last_name", "person_first_name",
                           "person_name_extension", "person_middle_name", ]
                df = securequerydatafromdatabase(sql, values, columns)

                person_last_name = df["person_last_name"][0]
                person_first_name = df["person_first_name"][0]
                person_name_extension = df["person_name_extension"][0]
                person_middle_name = df["person_middle_name"][0]

                values = ["", "", "", person_first_name, person_last_name, person_middle_name, person_name_extension, "", userprocess_editmodalhead,
                          btnsubmituser, userid, [], {'display': 'none'}, False, False, {}, {'display': 'none'}, "", ""]
            else:
                values = ["", "", "", "", "", "", "", "", userprocess_editmodalhead,
                          btnsubmituser, userid, [], {'display': 'none'}, False, False, {}, {'display': 'none'}, "", ""]
            return values
            # raise PreventUpdate
    else:
        raise PreventUpdate


@ app.callback(
    [
        Output("users_username", "valid"),
        Output("users_username", "invalid"),
        Output("users_password", "valid"),
        Output("users_password", "invalid"),
        Output("users_confirm_password", "valid"),
        Output("users_confirm_password", "invalid"),
        Output("users_fname", "valid"),
        Output("users_fname", "invalid"),
        Output("users_lname", "valid"),
        Output("users_lname", "invalid"),
        Output("users_mname", "valid"),
        Output("users_mname", "invalid"),
        Output("users_upemail", "valid"),
        Output("users_upemail", "invalid"),
        Output("users_persondd", "valid"),
        Output("users_persondd", "invalid"),

        Output('users_usersubmitstatus', "value"),
        Output("users_persondd", "value"),
        Output('users_results_modal', "is_open"),
        Output('users_results_body', "children"),
        Output('users_results_head_close', "style"),
        Output('users_results_head_return', "style"),
    ],
    [
        Input('users_btnsubmituser', 'n_clicks'),
        Input('btn_results_head_close', 'n_clicks'),
        Input('btn_results_head_return', 'n_clicks'),
    ],
    [
        State('current_user_id', 'data'),
        State('users_username', 'value'),
        State('users_password', 'value'),
        State('users_confirm_password', 'value'),
        State('users_fname', 'value'),
        State('users_lname', 'value'),
        State('users_mname', 'value'),
        State('users_upemail', 'value'),
        State("users_persondd", "value"),
        State("users_persondd2", "value"),
        State("users_btnsubmituser", "children"),
        State("users_chkusermarkfordeletion", "value"),
        State("url", "search"),
    ]

)
def process_users_data(btnsubmituser, btn_results_head_close, btn_results_head_return,
                current_user_id, username, pword, cpword, fname, lname, mname, upemail, person_id,  users_persondd2, mode, chkusermarkfordeletion, url):
    ctx = dash.callback_context
    stylehead_close = {'display': 'none'}
    stylehead_return = {'display': 'none'}
    parsed = urlparse.urlparse(url)



    if ctx.triggered:
        validity = [
            False, False, False,
            False, False, False,
            False, False, False,
            False, False, False,
            False, False, False, False
        ]
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'users_btnsubmituser':

            if person_id:
                if len(str(person_id)) == 0:
                    is_valid_person_id = False
                else:
                    is_valid_person_id = True

            else:
                is_valid_person_id = False

            if fname:
                if len(fname) == 0:
                    is_valid_fname = False
                else:
                    is_valid_fname = True
            else:
                is_valid_fname = False

            if lname:
                if len(lname) == 0:
                    is_valid_lname = False
                else:
                    is_valid_lname = True
            else:
                is_valid_lname = False

            if username:
                if mode == "Save New User":
                    pattern = re.compile(" ")
                    sql = "SELECT user_name FROM users WHERE user_name = %s and user_delete_ind = %s"
                    values = (username, False)
                    columns = ['user_name']
                    df = securequerydatafromdatabase(sql, values, columns)
                    if (len(username) < 3) or (df.shape[0] > 0) or pattern.search(username):
                        is_valid_username = False
                    else:
                        is_valid_username = True
                else:
                    userid = int(parse_qs(parsed.query)['uid'][0])
                    pattern = re.compile(" ")
                    sql = "SELECT user_id,user_name FROM users WHERE user_name = %s and user_delete_ind = %s"
                    values = (username, False)
                    columns = ["user_id", "user_name"]
                    df = securequerydatafromdatabase(sql, values, columns)
                    if (len(username) < 3) or pattern.search(username):
                        is_valid_username = False
                    elif df.shape[0] == 1:
                        if df["user_id"][0] != userid:
                            is_valid_username = False
                        else:
                            is_valid_username = True
                    else:
                        is_valid_username = True
            else:
                is_valid_username = False

            if parse_qs(parsed.query)['mode'][0] == "edit":
                is_valid_password = True
            else:
                if pword:
                    if len(pword) < 6:
                        is_valid_password = False
                    else:
                        is_valid_password = True
                else:
                    is_valid_password = False

            if parse_qs(parsed.query)['mode'][0] == "edit":
                is_valid_confirmpassword = True
            else:
                if cpword:
                    if cpword != pword:
                        is_valid_confirmpassword = False
                    else:
                        is_valid_confirmpassword = True
                        pword = hash_string(pword)
                        cpword = hash_string(cpword)
                else:
                    is_valid_confirmpassword = False

            is_valid_mname = True

            if upemail:
                if mode == "Save New User":
                    pattern = re.compile(" ")
                    sql = "SELECT user_up_email FROM users WHERE user_up_email = %s and user_delete_ind = %s"
                    values = (upemail, False)
                    columns = ['user_up_email']
                    df = securequerydatafromdatabase(sql, values, columns)
                    if (df.shape[0] > 0) or pattern.search(upemail):
                        is_valid_upemail = False
                    elif (len(upemail) > 0) and (upemail.endswith("@up.edu.ph") == True):
                        is_valid_upemail = True
                    else:
                        is_valid_upemail = False
                else:
                    userid = int(parse_qs(parsed.query)['uid'][0])
                    pattern = re.compile(" ")
                    sql = "SELECT user_id,user_up_email FROM users WHERE user_up_email = %s and user_delete_ind = %s"
                    values = (upemail, False)
                    columns = ["user_id", "user_up_email"]
                    df = securequerydatafromdatabase(sql, values, columns)
                    if pattern.search(upemail):
                        is_valid_upemail = False
                    elif (len(upemail) > 0) and (upemail.endswith("@up.edu.ph") == True):
                        is_valid_upemail = True
                    elif df.shape[0] == 1:
                        if df["user_id"][0] != userid:
                            is_valid_upemail = False
                        else:
                            is_valid_upemail = True
                    else:
                        is_valid_upemail = False
            else:
                is_valid_upemail = False

            validity = [
                is_valid_username, not is_valid_username,
                is_valid_password, not is_valid_password,
                is_valid_confirmpassword, not is_valid_confirmpassword,
                is_valid_fname, not is_valid_fname,
                is_valid_lname, not is_valid_lname,
                is_valid_mname, not is_valid_mname,
                is_valid_upemail, not is_valid_upemail,
                is_valid_person_id, not is_valid_person_id
            ]
            allvalid1 = [is_valid_username, is_valid_password,
                         is_valid_confirmpassword, is_valid_fname, is_valid_lname, is_valid_upemail]
            allvalid2 = [is_valid_username, is_valid_person_id,
                         is_valid_password, is_valid_confirmpassword, is_valid_upemail]

            if all(allvalid1) or all(allvalid2):
                if mode == "Save New User":
                    if person_id:
                        sql = """
                            INSERT INTO users (user_name, user_password, user_delete_ind, user_first_name,
                                user_last_name, user_middle_name, user_up_email, user_inserted_on, user_inserted_by, person_id)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            RETURNING user_id
                        """
                        values = (username, pword, False, fname, lname,
                                  mname, upemail, datetime.now(), current_user_id, person_id)
                        userid = modifydatabasereturnid(sql, values)

                        sqlcommand = '''SELECT emp_id
                                          FROM employees
                                         WHERE emp_delete_ind = %s
                                           AND person_id = %s'''
                        values2 = (False, person_id)
                        columns2 = ['emp_id']
                        df = securequerydatafromdatabase(sqlcommand, values2, columns2)

                        try:
                            emp_id = df['emp_id'][0]
                            sql_emp = """
                                UPDATE employees
                                   SET emp_user_id = %s
                                 WHERE person_id = %s
                            """
                            values3 = (userid, person_id)
                            modifydatabase(sql_emp, values3)

                        except:

                            pass

                    else:

                        sql = """
                            INSERT INTO users (user_name, user_password, user_delete_ind, user_first_name,
                                user_last_name, user_middle_name, user_up_email, user_inserted_on, user_inserted_by)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            RETURNING user_id
                        """
                        values = (username, pword, False, fname, lname,
                                  mname, upemail, datetime.now(), current_user_id)
                        userid = modifydatabasereturnid(sql, values)

                    displayed = True
                    message = "Successfully added new user"
                    status = "1"
                    stylehead_close = {'display': 'inline'}
                    stylehead_return = {'display': 'none'}

                else:
                    sql = """
                        UPDATE users SET user_name = %s, user_delete_ind= %s, user_first_name= %s,
                            user_last_name= %s, user_middle_name= %s, user_up_email = %s, user_inserted_on= %s, user_inserted_by= %s, person_id = %s
                        WHERE user_id = %s
                    """
                    if '1' in chkusermarkfordeletion:
                        fordelete = True
                    else:
                        fordelete = False
                    values = (username, fordelete, fname, lname, mname, upemail,
                              datetime.now(), current_user_id, users_persondd2, userid)
                    modifydatabase(sql, values)

                    # sqlcommand = '''SELECT emp_id
                    #                   FROM employees
                    #                  WHERE emp_delete_ind = %s
                    #                    AND person_id = %s'''
                    # values2 = (False, person_id)
                    # columns2 = ['emp_id']
                    # df = securequerydatafromdatabase(sqlcommand, values2, columns2)

                    sql_emp = """
                        UPDATE employees
                           SET emp_user_id = %s
                         WHERE person_id = %s
                    """
                    values3 = (userid, person_id)
                    modifydatabase(sql_emp, values3)

                    validity = [
                        False, False, False,
                        False, False, False,
                        False, False, False,
                        False, False, False,
                        False, False, False, False
                    ]
                    stylehead_close = {'display': 'none'}
                    stylehead_return = {'display': 'inline'}
                    displayed = True
                    message = "Successfully edited user"
                    status = "1"
            else:
                status = "2"
                displayed = True
                message = "Please review input data"
                stylehead_close = {'display': 'inline'}
                stylehead_return = {'display': 'none'}
            out = [status, "", displayed, message, stylehead_close, stylehead_return]
            out = validity+out
            return out

        elif eventid == 'btn_results_head_close':
            status = "0"
            displayed = False
            message = "Please review input data"
            stylehead_close = {'display': 'inline'}
            stylehead_return = {'display': 'none'}
            out = [status, "", displayed, message, stylehead_close, stylehead_return]
            out = validity+out
            return out
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@ app.callback(
    [
        Output('users_persondd', 'options'),
        Output('users_persondd2', 'options'),
    ],
    [
        Input('url', 'search'),
    ],
    [
        State("users_btnsubmituser", "children"),
    ],
)
def fill_in_dropdowns_for_users_profile(url, mode):
    ctx = dash.callback_context
    eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    parsed = urlparse.urlparse(url)
    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == 'edit':
            personoptions = commonmodules.queryfordropdown('''
                        SELECT person_last_name || ', ' || person_first_name || ' ' || CASE WHEN person_name_extension IS NULL THEN '' ELSE person_name_extension END || ' ' || CASE WHEN person_middle_name IS NULL THEN '' ELSE person_middle_name END as label, per.person_id as value
                          FROM persons per
                        LEFT JOIN employees emp ON emp.person_id = per.person_id
                         WHERE person_delete_ind = %s
                        ORDER BY person_last_name ASC
                   ''', (False,))
        else:
            personoptions = commonmodules.queryfordropdown('''
                        SELECT person_last_name || ', ' || person_first_name || ' ' || CASE WHEN person_name_extension IS NULL THEN '' ELSE person_name_extension END || ' ' || CASE WHEN person_middle_name IS NULL THEN '' ELSE person_middle_name END as label, per.person_id as value
                          FROM persons per
                        LEFT JOIN employees emp ON emp.person_id = per.person_id
                         WHERE person_delete_ind = %s
                           AND emp_user_id IS NULL
                           AND per.person_id NOT IN (SELECT person_id
        									      FROM users
        									     WHERE user_delete_ind = %s
        										   AND person_id IS NOT NULL)
                        ORDER BY person_last_name ASC
                   ''', (False, False,))
    else:
        raise PreventUpdate

    return [personoptions, personoptions]
