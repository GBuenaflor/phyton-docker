import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from apps import commonmodules
import dash_bootstrap_components as dbc
from app import app
from dash.exceptions import PreventUpdate
import re
from dash.dependencies import Input, Output, State
from apps import commonmodules
import dash
from apps.dbconnect import securequerydatafromdatabase
import urllib.parse as urlparse
from urllib.parse import parse_qs


layout = html.Div([
    commonmodules.get_header(),
    commonmodules.get_menu(),
    commonmodules.get_common_variables(),
    html.H1("Module Closed"),
    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("This module is closed for the time being."),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            dcc.Markdown('''Please wait for further announcements from HRDO. ''')
                        ]),



                    ])
                ])
            ])
        ])
    ])
])

#
# @app.callback(
#     [
#         Output('pending', 'children'),
#         Output('rolename', 'children')
#     ],
#     [
#         Input('url', 'pathname'),
#         Input('ddroledropdown', 'value')
#     ],
#     [
#         State('sessioncurrentrole', 'data'),
#         State('pending', 'children'),
#         State('current_user_id', 'data'),
#         State('sessionroleunits', 'data'),
#         State('sessiondefaultrole', 'data'),
#         State('sessionlistofunits', 'data'),
#         State('sessioncurrentunit', 'data'),
#     ]
# )
# def pendingapprovals(url, ddroledropdown, sessioncurrentrole, pending, currentuserid, sessionroleunits, sessiondefaultrole,
#                      sessionlistofunits, sessioncurrentunit):
#     #listofallowedunits = tuple(sessionlistofunits[str(sessioncurrentunit)])
#     # print("sessionlistofunits", sessionlistofunits)
#     # print("sessioncurrentunit", sessioncurrentunit)
#     print('printing sessioncurrentunit', sessioncurrentunit)
#     try:
#         listofallowedunits = tuple(sessionlistofunits[str(sessioncurrentunit)])
#     except:
#         listofallowedunits = ''
#     ctx = dash.callback_context
#     parsed = urlparse.urlparse(url)
#     if ctx.triggered:
#         eventid = ctx.triggered[0]['prop_id'].split('.')[0]
#         if eventid == 'ddroledropdown':
#
#             listofunits = list(
#                 filter(lambda sessionroleunits: sessionroleunits['role_id'] == ddroledropdown, sessionroleunits))
#             print("listofunits", listofunits)
#             if listofunits:
#                 unitrole = listofunits[0]
#             else:
#                 unitrole = list(filter(
#                     lambda sessionroleunits: sessionroleunits['role_id'] == sessiondefaultrole, sessionroleunits))[0]
#             print("unitrole", unitrole)
#
#             if currentuserid != -1:
#                 role_id = unitrole['role_id']
#
#                 print("role", role_id)
#
#                 #bpstatus = 0
#
#                 # if role_id == 2:
#                 #     bpstatus = 0
#                 if role_id == 29:
#                     bpstatus = 2
#                     print("listofallowedunits", listofallowedunits)
#                     if listofallowedunits == "":
#                         raise PreventUpdate
#                     else:
#                         sqlcommand = '''SELECT COUNT(bp.bp_id) AS Count
#                                                 FROM persons p INNER JOIN basic_papers bp on bp.person_id = p.person_id
#                                                 INNER JOIN bp_status_changes bsc ON bsc.bp_id = bp.bp_id
#                                                 INNER JOIN bp_statuses bs ON bsc.bp_status_id = bs.bp_status_id
#                                                 INNER JOIN designations d ON d.designation_id = bp.bp_designation_id
#                                                 INNER JOIN appointment_types bpt ON bpt.appt_type_id = bp.bp_appt_type_id
#                                                 INNER JOIN emp_classes ec ON ec.emp_class_id = bp.bp_emp_class_id
#                                                 WHERE bp_delete_ind = %s
#
#                                                   AND bs.bp_status_id = %s
#                                                   AND bp_status_change_current_ind = %s
#                                                   AND bp_designation_unit_id IN %s
#                                                   AND bp.bp_id NOT IN (SELECT bp_id
#                                                           FROM dpc_bp_approvals
#                                                         WHERE dpc_bp_approval_by = %s
#                                                           AND dpc_bp_approval_delete_ind = %s)
#                                                 AND bp.bp_emp_class_id IN (select DISTINCT dpc_member_type_id from dpc_members dm
#                                                         INNER JOIN employees e ON e.emp_id = dm.emp_id
#                                                         INNER JOIN users u ON u.user_id = e.emp_user_id
#                                                         where user_id = %s) '''
#                         values = (False, bpstatus, True, listofallowedunits,
#                                   currentuserid, False, currentuserid,)
#
#                         columns = ['Count']
#                         df = securequerydatafromdatabase(sqlcommand, values, columns)
#                         count = df['Count'][0]
#                         print("count", count)
#
#                 elif role_id == 30:
#                     bpstatus = 4
#                     if listofallowedunits == "":
#                         raise PreventUpdate
#                     else:
#                         sqlcommand = '''SELECT COUNT(bp.bp_id) AS Count
#                                                 FROM persons p INNER JOIN basic_papers bp on bp.person_id = p.person_id
#                                                 INNER JOIN bp_status_changes bsc ON bsc.bp_id = bp.bp_id
#                                                 INNER JOIN bp_statuses bs ON bsc.bp_status_id = bs.bp_status_id
#                                                 INNER JOIN designations d ON d.designation_id = bp.bp_designation_id
#                                                 INNER JOIN appointment_types bpt ON bpt.appt_type_id = bp.bp_appt_type_id
#         										INNER JOIN emp_classes ec ON ec.emp_class_id = bp.bp_emp_class_id
#                                                 WHERE bp_delete_ind = %s
#
#                                                   AND bs.bp_status_id = %s
#                                                   AND bp_status_change_current_ind = %s
#                                                   AND bp_designation_unit_id IN %s
#                                                   AND bp.bp_id NOT IN (SELECT bp_id
#         												  FROM cpc_bp_approvals
#         												WHERE cpc_bp_approval_by = %s
#                                                           AND cpc_bp_approval_delete_ind = %s)
#         										AND bp.bp_emp_class_id IN (select DISTINCT cpc_member_type_id from cpc_members dm
#         												INNER JOIN employees e ON e.emp_id = dm.emp_id
#         												INNER JOIN users u ON u.user_id = e.emp_user_id
#         												where user_id = %s) '''
#                         values = (False, 4, True, listofallowedunits,
#                                   currentuserid, False, currentuserid, )
#                         print("listofallowedunits", listofallowedunits)
#                         columns = ['Count']
#                         df = securequerydatafromdatabase(sqlcommand, values, columns)
#                         count = df['Count'][0]
#                         print("count", count)
#
#                 elif role_id in [33, 7, 1, 8, 15, 9, 10, 16, 25, 11, 12, 13, 17, 14]:
#                     if role_id == 33:
#                         bpstatus = 3
#                     elif role_id == 7:
#                         bpstatus = 5
#                     elif role_id == 1:
#                         bpstatus = 6
#                     elif role_id == 8:
#                         bpstatus = 7
#                     elif role_id == 15:
#                         bpstatus = 8
#                     elif role_id == 9:
#                         bpstatus = 9
#                     elif role_id == 10:
#                         bpstatus = 10
#                     elif role_id == 16:
#                         bpstatus = 17
#                     elif role_id == 25:
#                         bpstatus = 11
#                     elif role_id == 11:
#                         bpstatus = 12
#                     elif role_id == 12:
#                         bpstatus = 13
#                     elif role_id == 13:
#                         bpstatus = 15
#                     elif role_id == 17:
#                         bpstatus = 14
#                     elif role_id == 14:
#                         bpstatus = 16
#                     if listofallowedunits == "":
#                         raise PreventUpdate
#                     else:
#                         sqlcommand = '''
#                                     SELECT COUNT(bp.bp_id) AS Count
#                                     FROM persons p
#                                     INNER JOIN basic_papers bp on bp.person_id = p.person_id
#                                     INNER JOIN bp_status_changes bsc ON bsc.bp_id = bp.bp_id
#                                     INNER JOIN bp_statuses bs ON bsc.bp_status_id = bs.bp_status_id
#                                     INNER JOIN designations d ON d.designation_id = bp.bp_designation_id
#                                     INNER JOIN appointment_types at ON at.appt_type_id = bp.bp_appt_type_id
#                                     WHERE bp_delete_ind = %s
#                                       AND bs.bp_status_id = %s
#                                       AND bp_status_change_current_ind = %s
#                                       AND bp_designation_unit_id IN %s
#                                       AND bp.bp_id NOT IN (SELECT bp_id
#                                               FROM dpc_bp_approvals
#                                             WHERE dpc_bp_approval_by = %s)
#                                       '''
#                         values = (False, bpstatus, True,  listofallowedunits, currentuserid,)
#
#                         print("listofallowedunits", listofallowedunits)
#                         columns = ['Count']
#                         df = securequerydatafromdatabase(sqlcommand, values, columns)
#                         count = df['Count'][0]
#                         print("count", count)
#
#                 else:
#                     count = 0
#
#                 # print("listofallowedunits", listofallowedunits)
#                 # columns = ['Count']
#                 # df = securequerydatafromdatabase(sqlcommand, values, columns)
#                 # count = df['Count'][0]
#                 # print("count", count)
#
#                 #count = 1
#
#                 sqlrole = '''SELECT role_name FROM roles WHERE role_id = %s'''
#                 values = (role_id,)
#                 columns = ['role_name']
#                 df = securequerydatafromdatabase(sqlrole, values, columns)
#                 role_name = df['role_name'][0]
#                 print("role_name", role_name)
#
#                 return [count, role_name]
#             else:
#                 raise PreventUpdate
#
#         else:
#             raise PreventUpdate
#     else:
#         raise PreventUpdate
