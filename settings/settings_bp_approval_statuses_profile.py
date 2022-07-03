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
from apps.commonmodules import checkiflengthzero2, checkstyle2



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
                html.H4("Add New BP Approval Status", id="bpstatuses_editmodalhead"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),

            dbc.CardBody([
                dcc.Link('← Back to BP Approval Statuses', href='/settings/settings_bp_approval_statuses'),
                html.Br(),
                html.Br(),
                dbc.Form([
                    dbc.FormGroup(
                        [dbc.Label("BP Approval Status Name", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="bpstatuses_name", placeholder="Enter BP Approval Status"
                             ),
                             dbc.FormFeedback("Enter a valid BP approval status", valid=False)
                         ],
                            width=8
                        )],
                        row=True
                    ),

                    dbc.FormGroup(
                        [dbc.Label("BP Status Description", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="bpstatuses_description", placeholder="e.g. BP is for VCA Approval"
                             ),
                             dbc.FormFeedback("Enter a valid BP approval status description", valid=False)
                         ],
                             width=8
                         )],
                        row=True
                    ),

                    dbc.FormGroup(
                        [dbc.Label("BP Status Past Name", width=2, style={"text-align": "left"}),
                         dbc.Col([
                             dbc.Input(
                                 type="text", id="bpstatuses_pastname", placeholder="e.g. Approved by VCA"
                             ),
                             dbc.FormFeedback("Enter a valid BP approval status description", valid=False)
                         ],
                             width=8
                         )],
                        row=True
                    ),



                    dbc.FormGroup(
                        [dbc.Label("BP Status Type", width=2, style={"text-align": "left"}, id = 'bpstatuses_type_label'),
                         dbc.Col([
                             dcc.Dropdown(
                                 id="bpstatuses_type",
                                 options=[
                                    {'label': 'Approval Status', 'value': 0},
                                    {'label': 'Return Status', 'value': 1},
                                    {'label': 'Terminal Status', 'value': 2},
                                    {'label': 'In Process Status', 'value': 3},

                                 ],
                                 searchable=False,
                                 value = 0
                             ),
                             dbc.FormFeedback("Select a BP status type", valid=False)
                         ],
                             width=8
                         )],
                        row=True
                    ),

                    html.Hr(),
                    # dbc.Label("Status Viewable by ", width=2, style={"text-align": "left"}, id = 'bpstatuses_type_label')



                    html.Div([
                        dbc.FormGroup(
                            [dbc.Label("Add Approving Role to Status", width=2, style={"text-align": "left"}, id = 'bpstatuses_role_label'),
                             dbc.Col([
                                 dcc.Dropdown(
                                     id="bpstatuses_addrole",
                                     options=[
                                        # {'label': 'Faculty', 'value': '1'},
                                        # {'label': 'Administrative Personnel', 'value': '2'},
                                        # {'label': 'Research and Extension Professional Staff (REPS)', 'value': '3'},
                                        # {'label': 'Others', 'value': '11'}
                                     ],
                                     searchable=True
                                 ),
                                 #dbc.FormFeedback("Too short or already taken", valid = False)
                             ],
                                width=8
                            )],
                            row=True
                        ),

                    dbc.Button("Add Role", id="bpstatusesprofile_addrolebtn", color="primary", block=False),

                    html.Br(),
                    html.Br(),

                    html.Div([

                    ], id='bpstatusesprofile_rolesdiv'),



                    dbc.FormGroup(
                        [dbc.Label("Remove Approving Role to Status", width=2, style={"text-align": "left"},
                                   id='bpstatuses_role_label'),
                         dbc.Col([
                             dcc.Dropdown(
                                 id="bpstatuses_removerole",
                                 options=[
                                     # {'label': 'Faculty', 'value': '1'},
                                     # {'label': 'Administrative Personnel', 'value': '2'},
                                     # {'label': 'Research and Extension Professional Staff (REPS)', 'value': '3'},
                                     # {'label': 'Others', 'value': '11'}
                                 ],
                                 searchable=False
                             ),
                             # dbc.FormFeedback("Too short or already taken", valid = False)
                         ],
                             width=8
                         )],
                        row=True
                    ),

                    dbc.Button("Remove Role", id="bpstatusesprofile_removerolebtn", color="warning", block=False),

                    html.Br(),
                    html.Br(),

                    ], id='div_bpstatuses_roles',
                        # style={'display':'none'}
                    ),




                    html.Div([
                        dcc.Checklist(
                            options=[
                                {'label': ' Mark for Deletion?', 'value': '1'},
                            ], id='bpstatuses_chkmarkfordeletion', value=[]
                        ),
                    ], id='bpstatuses_deletediv',  style={'text-align': 'middle', 'display': 'inline'}),

                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save New BP Approval Status", id="bpstatuses_submitbtn",
                                   color="primary", block=True),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", id="bpstatuses_cancel",
                                   href='/settings/settings_bp_approval_statuses', color="secondary", className="ml-auto")
                    ]),
                ], style={'width': '100%'}),


                dbc.Modal(
                    [
                        dbc.ModalHeader("BP Approval Status Encoding Confirmation", id='bpstatuses_submitmodal1header'),
                        dbc.ModalBody("Confirm BP Approval Status Entry Submission",
                                      id='bpstatuses_submitmodal1body'),
                        dbc.ModalFooter([
                            dbc.Button("Confirm", id="bpstatuses_submitmodal1go", className="mr-1",
                                       color='primary'),
                            dbc.Button("Back", id='bpstatuses_submitmodal1back', className="ml-auto")

                            # dbc.Button("Back to Home", id='bpstatuses_submitmodal2_returnbtn', className="ml-auto", href = '/')
                        ]),
                    ],
                    id="bpstatuses_submitmodal1",
                ),

                dbc.Modal(
                    [
                        dbc.ModalHeader("BP Approval Status Encoding", id='bpstatuses_submitmodal2_header'),
                        dbc.ModalBody("Employee Database has been successfully updated.",
                                      id='bpstatuses_submitmodal2_body'),
                        dbc.ModalFooter([
                            dbc.Button(
                                "Back to BP Approval Statuses", id='bpstatuses_submitmodal2_closebtn', className="ml-auto", color = 'primary',
                                # href = '/settings/settings_person_employee_encoding',
                                href='/settings/settings_bp_approval_statuses',
                            ),
                            dbc.Button(
                                "Close", id='bpstatuses_submitmodal2_closebtn', className="ml-auto",color = 'primary',
                                # href = '/settings/settings_person_employee_encoding',
                                href='/home',
                            ),
                            # dbc.Button("Back to Home", id='bpstatuses_submitmodal2_returnbtn', className="ml-auto", href = '/')
                        ]),
                    ],
                    id="bpstatuses_submitmodal2",
                ),

                dbc.Input(id = 'bpstatusesprofile_proxyinput', value = 0, style = {'display':'none'})


            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )


    ]),


])


@app.callback(
    [
        Output('bpstatusesprofile_proxyinput', 'value')
    ],

    [
        Input('bpstatusesprofile_addrolebtn', 'n_clicks'),
        Input('bpstatusesprofile_removerolebtn', 'n_clicks'),
        # Input('bpstatusesprofile_rolesdiv', 'children')


    ],
    [
        State('url', 'search'),
        State('bpstatuses_addrole', 'value'),
        State('bpstatuses_removerole', 'value'),
        State('current_user_id', 'data'),

    ]


)

def updateaddremoveroles(bpstatusesprofile_addrolebtn, bpstatusesprofile_removerolebtn,
                         # bpstatusesprofile_rolesdiv,
                         url, bpstatuses_addrole, bpstatuses_removerole, current_user_id):

    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)

    if parse_qs(parsed.query):
        mode = str(parse_qs(parsed.query)['mode'][0])
        if mode == "edit":
            bp_status_id = str(parse_qs(parsed.query)['bp_status_id'][0])

        if ctx.triggered:
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]

            if eventid == 'bpstatusesprofile_addrolebtn':



                sqlupdate = '''
                            INSERT INTO bp_status_roles (bp_status_id, role_id, bp_status_role_module_type, bp_status_role_inserted_by, bp_status_role_inserted_on, bp_status_role_delete_ind)
                            VALUES (%s, %s, %s, %s, %s, %s)

                '''
                values = (bp_status_id, bpstatuses_addrole, 1, current_user_id, datetime.now(), False)

                modifydatabase(sqlupdate, values)

            elif eventid == 'bpstatusesprofile_removerolebtn':
                sqlupdate = '''
                        UPDATE bp_status_roles SET bp_status_role_delete_ind = %s
                        WHERE bp_status_id = %s
                        AND role_id = %s

                            '''
                values = (True, bp_status_id, bpstatuses_removerole)
                modifydatabase(sqlupdate, values)

            return [1]

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('bpstatusesprofile_rolesdiv', 'children'),
        Output('bpstatuses_addrole', 'options'),
        Output('bpstatuses_removerole', 'options'),


    ],
    [
        Input("url", "search"),
        Input('bpstatusesprofile_addrolebtn', 'n_clicks'),
        Input('bpstatusesprofile_removerolebtn', 'n_clicks'),

    ]


)

def loadrolestable(url, bpstatusesprofile_addrolebtn, bpstatusesprofile_removerolebtn):
    addroleoptions = []
    removeroleoptions = []
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":

            bp_status_id = str(parse_qs(parsed.query)['bp_status_id'][0])

            sql1 = '''
                        SELECT bsr.role_id, r.role_name
                        FROM bp_status_roles bsr
                        LEFT JOIN roles r ON r.role_id = bsr.role_id
                        WHERE bsr.bp_status_id = %s
                        AND bsr.bp_status_role_delete_ind = %s

                '''

            addroleoptions = commonmodules.queryfordropdown('''
                        SELECT role_name as label, role_id as value
                        FROM roles
                        WHERE role_delete_ind = %s
                        AND role_id NOT IN (
                                    SELECT r.role_id
                                    FROM bp_status_roles bsr
                                    LEFT JOIN roles r ON r.role_id = bsr.role_id
                                    WHERE bsr.bp_status_id = %s
                                    AND bsr.bp_status_role_delete_ind = %s

                        )
                        ORDER BY role_name
                   ''', (False, bp_status_id, False))

            removeroleoptions = commonmodules.queryfordropdown('''

                        SELECT r.role_name as label, bsr.role_id as value
                        FROM bp_status_roles bsr
                        LEFT JOIN roles r ON r.role_id = bsr.role_id
                        WHERE bsr.bp_status_id = %s
                        AND bsr.bp_status_role_delete_ind = %s

                   ''', (bp_status_id, False))

            values1 = (bp_status_id, False)
            columns1 = ['role_id', 'role_name']
            df = securequerydatafromdatabase(sql1, values1, columns1)
            df.columns = ['Role ID', 'Role']

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
        else:
            table = []

        return [table, addroleoptions, removeroleoptions]

    else:
        raise PreventUpdate


@app.callback(
    [
        Output('bpstatuses_name', 'value'),
        Output('bpstatuses_description', 'value'),
        Output('bpstatuses_pastname', 'value'),
        Output('bpstatuses_type', 'value'),
        Output('bpstatuses_addrole', 'value'),


        Output("bpstatuses_editmodalhead", "children"),
        Output("bpstatuses_submitbtn", "children"),
        Output("bpstatuses_chkmarkfordeletion", "style"),


        Output('div_bpstatuses_roles', 'style'),


    ],
    [
        Input("url", "search"),
    ],
    [

    ]

)
def cleardata(url,

              ):

    div_bpstatuses_roles_style = {'display':'inline'}
    table = []

    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parsed.query:
        if parse_qs(parsed.query)['mode'][0] == "edit":

            bp_status_id = str(parse_qs(parsed.query)['bp_status_id'][0])
            div_bpstatuses_roles_style = {'display': 'inlne'}
            bpstatuses_editmodalhead = "Edit Existing BP Status"
            bpstatuses_submit = "Save Changes"
            bpstatuses_chkmarkfordeletion_style = {"display": "inline"}
            bp_status_id = parse_qs(parsed.query)['bp_status_id'][0]

            sql = '''

            SELECT bp_status_name, bp_status_description, bp_status_past_name, bp_status_type, r.role_id
            FROM bp_statuses bs
            LEFT JOIN bp_status_roles bsr ON bs.bp_status_id = bsr.bp_status_id
            LEFT JOIN roles r ON r.role_id = bsr.role_id
            WHERE bp_status_delete_ind = %s
            AND bs.bp_status_id = %s
            '''
            values = (False, bp_status_id,)
            columns = ['bp_status_name', 'bp_status_description', 'bp_status_past_name', 'bp_status_type', 'role_id']
            df = securequerydatafromdatabase(sql, values, columns)

            bp_status_name = df["bp_status_name"][0]
            bp_status_description = df["bp_status_description"][0]
            bp_status_past_name = df["bp_status_past_name"][0]
            bp_status_type = df["bp_status_type"][0]
            role_id = df["role_id"][0]

        elif parse_qs(parsed.query)['mode'][0] == "add":

            div_bpstatuses_roles_style = {'display': 'none'}
            bpstatuses_editmodalhead = "Add New BP Approval Status"
            bpstatuses_submit = "Save New BP Approval Status"
            bpstatuses_chkmarkfordeletion_style = {"display": "none"}


            bp_status_name = ""
            bp_status_description= ""
            bp_status_past_name= ""
            bp_status_type = ""
            role_id= ""



        return [bp_status_name, bp_status_description, bp_status_past_name,bp_status_type, role_id,
                bpstatuses_editmodalhead, bpstatuses_submit, bpstatuses_chkmarkfordeletion_style,
                div_bpstatuses_roles_style]

    else:

        raise PreventUpdate

# @app.callback(
#
#
#         Output("div_bpstatuses_role", "style"),
#
#
#
#     [
#         Input("bpstatuses_type", "value"),
#     ],
#     [
#
#     ]
#
# )
# def toggle_divrole(bpstatuses_type,
#                          # sabbatical_first_time
#                          ):
#     ctx = dash.callback_context
#     # parsed = urlparse.urlparse(url)
#     # if path == "/leaves/leavesentry_profile":
#
#     if ctx.triggered:
#         eventid = ctx.triggered[0]['prop_id'].split('.')[0]
#         if eventid == 'bpstatuses_type':
#             print(bpstatuses_type, 'bpstatuses_type')
#             if bpstatuses_type == 0:
#                 return {'display': 'inline'}
#             else:
#                 return {'display': 'none'}
#         else:
#             raise PreventUpdate
#     else:
#         raise PreventUpdate

@app.callback(
    [
        Output('bpstatuses_name', 'valid'), Output('bpstatuses_name', 'invalid'),
        Output('bpstatuses_description', 'valid'), Output('bpstatuses_description', 'invalid'),
        Output('bpstatuses_pastname', 'valid'), Output('bpstatuses_pastname', 'invalid'),
        Output('bpstatuses_type_label', 'style'),

        Output('bpstatuses_submitmodal1', 'is_open')



    ],

    [
        Input('bpstatuses_submitbtn', 'n_clicks'),
        Input('bpstatuses_submitmodal1go', 'n_clicks'),
        Input('bpstatuses_submitmodal1back', 'n_clicks')

    ],
    [
        State('bpstatuses_name', 'value'),
        State('bpstatuses_description', 'value'),
        State('bpstatuses_pastname', 'value'),
        State('bpstatuses_type', 'value'),


    ]

)

def bpstatuses_modal1open(bpstatuses_submitbtn, bpstatuses_submitmodal1go, bpstatuses_submitmodal1back,
                          bpstatuses_name, bpstatuses_description, bpstatuses_pastname, bpstatuses_type):

    bpstatuses_submitmodal1 = False
    ctx = dash.callback_context
    if ctx.triggered:

        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        bpstatuses_namevalid = checkiflengthzero2(bpstatuses_name)
        bpstatuses_descriptionvalid = checkiflengthzero2(bpstatuses_description)
        bpstatuses_pastnamevalid = checkiflengthzero2(bpstatuses_pastname)
        bpstatuses_typevalid = checkiflengthzero2(bpstatuses_type+1)

        bpstatuses_type_label = checkstyle2(bpstatuses_typevalid)
        # if bpstatuses_type == 0:
        #     bpstatuses_rolevalid = checkiflengthzero2(bpstatuses_role)
        #
        #     bpstatuses_role_label = checkstyle2(bpstatuses_rolevalid)
        # else:
        #     bpstatuses_rolevalid = True
        #     bpstatuses_role_label = {"text-align": "left", 'color': 'black'}

        allvalid = [bpstatuses_namevalid, bpstatuses_descriptionvalid, bpstatuses_pastnamevalid, bpstatuses_typevalid]


        if all(allvalid):

            bpstatuses_submitmodal1 = True

        if eventid in ['bpstatuses_submitbtn','bpstatuses_submitmodal1go', 'bpstatuses_submitmodal1back']:
            if eventid in ['bpstatuses_submitmodal1go', 'bpstatuses_submitmodal1back']:

                bpstatuses_submitmodal1 = False

            return [bpstatuses_namevalid, not bpstatuses_namevalid,
                    bpstatuses_descriptionvalid, not bpstatuses_descriptionvalid,
                    bpstatuses_pastnamevalid, not bpstatuses_pastnamevalid,
                    bpstatuses_type_label,

                    bpstatuses_submitmodal1]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('bpstatuses_submitmodal2', 'is_open')

    ],
    [
        Input('bpstatuses_submitmodal1go', 'n_clicks'),
        Input('bpstatuses_submitmodal2_closebtn', 'n_clicks')

    ],
    [
        State('bpstatuses_name', 'value'),
        State('bpstatuses_description', 'value'),
        State('bpstatuses_pastname', 'value'),
        State('bpstatuses_type', 'value'),
        State('bpstatuses_addrole', 'value'),
        State('bpstatuses_chkmarkfordeletion', 'value'),
        State('url', 'search'),
        State('current_user_id', 'data'),

    ]
)

def bpstatuses_submitmodal2(bpstatuses_submitmodal1go, bpstatuses_submitmodal2_closebtn,
                            bpstatuses_name, bpstatuses_description, bpstatuses_pastname, bpstatuses_type, bpstatuses_role,
                            bpstatuses_chkmarkfordeletion,
                            url,
                            current_user_id):

    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parse_qs(parsed.query):
        if ctx.triggered:
            mode = str(parse_qs(parsed.query)['mode'][0])
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]
            if eventid == 'bpstatuses_submitmodal1go':

                if mode == "add":

                    sql1 = """
                        INSERT INTO bp_statuses(bp_status_name, bp_status_description, bp_status_past_name,
                                                bp_status_inserted_by, bp_status_inserted_on, bp_status_delete_ind, bp_status_type)
                        VALUES (%s, %s, %s,
                                %s, %s, %s, %s)
                    """


                    values1 = [bpstatuses_name, bpstatuses_description, bpstatuses_pastname,
                               current_user_id, datetime.now(), False, bpstatuses_type]

                    modifydatabase(sql1, values1)

                    sql = '''
                    SELECT bp_status_id
                    FROM bp_statuses
                    WHERE bp_status_delete_ind = %s
                    AND bp_status_name = %s
                    AND bp_status_description = %s
                    AND bp_status_past_name = %s
                    AND bp_status_type = %s

                    '''
                    values = (False, bpstatuses_name,bpstatuses_description, bpstatuses_pastname, bpstatuses_type)
                    columns = ['bp_status_id']
                    df = securequerydatafromdatabase(sql, values, columns)

                    bp_status_id = int(df['bp_status_id'][0])


                    # if bpstatuses_type == 0:
                    #
                    #     sql2 = """
                    #         INSERT INTO bp_status_roles(bp_status_id, role_id,
                    #                                 bp_status_role_inserted_by, bp_status_role_inserted_on, bp_status_role_delete_ind)
                    #         VALUES (%s, %s,
                    #                 %s, %s, %s)
                    #     """
                    #
                    #
                    #     values2 = [bp_status_id, bpstatuses_role,
                    #                current_user_id, datetime.now(), False]
                    #
                    #     modifydatabase(sql2, values2)
                    # else:
                    #     pass

                elif mode == "edit":

                    bp_status_id = str(parse_qs(parsed.query)['bp_status_id'][0])

                    bpstatuses_deletevalue = False
                    if 1 in bpstatuses_chkmarkfordeletion or '1' in bpstatuses_chkmarkfordeletion:
                        bpstatuses_deletevalue = True


                    sql1 = """
                        UPDATE bp_statuses SET bp_status_name=%s, bp_status_description=%s, bp_status_past_name=%s,
                            bp_status_inserted_by = %s, bp_status_inserted_on = %s, bp_status_delete_ind = %s, bp_status_type = %s
                        WHERE bp_status_id=%s
                    """

                    values1 = [bpstatuses_name, bpstatuses_description, bpstatuses_pastname,
                                current_user_id, datetime.now(), bpstatuses_deletevalue, bpstatuses_type,
                               bp_status_id]

                    modifydatabase(sql1, values1)

                    # if bpstatuses_type == 0:

                        # sql2 = """
                        #     UPDATE bp_status_roles SET role_id=%s,
                        #         bp_status_role_inserted_by = %s, bp_status_role_inserted_on = %s, bp_status_role_delete_ind = %s
                        #     WHERE bp_status_id=%s
                        # """
                        #
                        # values2 = [bpstatuses_role,
                        #             current_user_id, datetime.now(), bpstatuses_deletevalue,
                        #            bp_status_id
                        #            ]
                        #
                        # modifydatabase(sql2, values2)

                    # else:
                    #     pass

                return [True]

            elif eventid == "bpstatuses_submitmodal2_closebtn":

                return [False]

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
