import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash
import pandas as pd
from dash.dependencies import Input, Output, State
import webbrowser
from dash.exceptions import PreventUpdate
from app import app
from apps import home, login, commonmodules, privacy, siteinfo, module_closed
from apps.settings import settings, settings_users, settings_users_profile, settings_modules, settings_modules_profile, settings_roles, settings_roles_profile
from apps.settings import settings_module_roles, settings_module_roles_profile, settings_user_roles, settings_user_roles_profile, settings_doc_requirements, settings_doc_requirements_profile
from apps.settings import settings_bp_types, settings_bp_types_profile, settings_bp_docs, settings_bp_docs_profile, settings_degrees, settings_degrees_profile, settings_degreeprograms_profile, settings_designations, settings_designations_profile, settings_salary_grades, settings_salary_grades_profile, settings_entitlements, settings_entitlements_profile, settings_entitlementtype_profile
from apps.settings import settings_perfrating_query, settings_perfrating_query_profile, settings_perfrating_management_profile
from apps.settings import settings_personal_data, settings_personal_data_profile, settings_admin_positions, settings_admin_positions_profile, settings_admin_emp_assignment, settings_admin_emp_assignment_profile
from apps.settings import settings_schools, settings_schools_profile, settings_employee_management, settings_employee_management_profile, settings_leaves, settings_leaves_profile
from apps.settings import settings_bp_approval_flows, settings_bp_approval_flows_profile, settings_person_employee_encoding
from apps.settings import settings_units, settings_units_profile, settings_personal_data_viewing, settings_personal_data_viewing_profile
from apps.settings import settings_unit_emp, settings_unit_emp_profile, settings_role_reports, settings_role_reports_profile, settings_bp_approval_statuses, settings_bp_approval_statuses_profile
from datetime import datetime
from waitress import serve
import os
import sys


CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
FOOTER_STYLE = {
    "position": "fixed",
    "bottom": 0,
    "left": 0,
    "right": 0,
    "height": "2rem",
    # "padding": "1rem 1rem",
    "background-color": "#f3f3f3ff",
}

#server = app.server
server = '0.0.0.0'
# added to supress all callback exceptions, march 2, 2021
app.config.suppress_callback_exceptions = True
app.layout = html.Div([
    # Session Variables
    dcc.Store(id='sessionmenudict', storage_type='session'),
    dcc.Store(id='sessioncurrentrole', storage_type='session', clear_data=False),
    dcc.Store(id='sessiondefaultrole', storage_type='session'),
    dcc.Store(id='sessionupdaterole', storage_type='session'),
    dcc.Store(id='sessionlogout', storage_type='session'),
    dcc.Store(id='current_user_id', storage_type='session', ),
    dcc.Store(id='temp_current_user_id', storage_type='session'),
    dcc.Store(id='sessionlastchange', storage_type='session'),
    dcc.Store(id='sessioncurrentunitid', storage_type='session'),
    #dcc.Store(id='sessioncurrentunit', storage_type='session'),
    dcc.Store(id='sessionlistofunits', storage_type='session'), #becomes access level now
    dcc.Store(id='sessionlistofunits_home', storage_type='session'), #home unit level
    dcc.Store(id='googlestate', storage_type='session'),
    dcc.Store(id='current_module', storage_type='session'),

    # Location Variable
    dcc.Location(id='url', refresh=True),

    # Page Content Variable


    dbc.Modal(
        [
            dbc.ModalHeader(
                html.H4(["Session Logout"])),
            dbc.ModalBody([
                "You have been automatically logged out of the system. Please login again if you want to use this service. "
            ]),
            dbc.ModalFooter([
                dbc.Button("Close", href="/", id="modal_logout_close",
                           style={"float": "left"}, color='primary')
            ]),
        ],
        id="modal_logout",
        centered=True,
        backdrop='static',
        keyboard=False,
        size="xl",
    ),
    html.Div(id='page-content', style=CONTENT_STYLE),

    html.Div(id="timeoutdiv"),
    dcc.Interval(id='timeoutinterval', interval=30*60*1000, n_intervals=0, max_intervals=-1),
    html.Div([
        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Acceptable Use Policy", href="https://upd.edu.ph/aup/")),
                dbc.NavItem(dbc.NavLink("Privacy Policy", href="/privacy")),
                dbc.NavItem(dbc.NavLink(
                    "Contact Us", href="https://docs.google.com/forms/d/e/1FAIpQLSe8tF2Rjh1SnJTzmqmwdch8_qBePibEnDqdlDOZPjl5O4IPFw/viewform")),
                dbc.NavItem(dbc.NavLink("HRDO Website", href="https://hrdo.upd.edu.ph/")),
                dbc.NavItem(dbc.NavLink("OVCA Website", href="https://ovca.upd.edu.ph/")),
                dbc.NavItem(dbc.NavLink("UPD Website", href="https://upd.edu.ph/")),
            ], fill=True,
        ),

    ], style=FOOTER_STYLE),
])




@app.callback([Output('timeoutinterval', 'disabled')],
              [Input('url', 'pathname')])
def update_(pathname):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'url':
            if pathname == "/" or pathname == '/logout':
                return [True]
            else:
                return [False]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback([Output('modal_logout', 'is_open')],
              [
    Input('timeoutinterval', 'n_intervals'),
    Input('modal_logout_close', 'n_clicks')
],
    [
        State('sessionlastchange', 'data')
])
def update_interval(n, modal_logout_close, sessionlastchange):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'timeoutinterval':
            sessiontimeout = False
            if sessionlastchange:
                sessionlastchange = datetime.strptime(sessionlastchange, '%Y-%m-%dT%H:%M:%S.%f')
                minutesdiff = (datetime.now() - sessionlastchange).total_seconds()/60
                if 30 > minutesdiff:
                    raise PreventUpdate
                else:
                    return [True]
            else:
                raise PreventUpdate
        elif eventid == 'modal_logout_close':
            return [False]
    else:
        raise PreventUpdate
# #
# @app.callback([
#                Output('modal_logout', 'is_open'),
#                ],
#               [
#               Input('url', 'pathname'),
#               Input('sessionupdaterole', 'modified_timestamp'),
#               Input('modal_logout_close','n_clicks')
#               ],
#               [
#               State('sessionmenudict', 'data'),
#               State('sessioncurrentrole', 'data'),
#               State('sessiondefaultrole', 'data'),
#               State('current_user_id', 'data'),
#               State('sessionlastchange', 'data'),
#               State('sessionlogout', 'data'),
#               State('url', 'search'),
#               State('current_module', 'data'),
#               State('url', 'href'),
#               State('sessionupdaterole', 'data'),
#               ])
# def display_logout(pathname, sessionupdaterole,modal_logout_close, sessionmenudict,
#                  sessioncurrentrole, sessiondefaultrole, current_user_id, sessionlastchange, sessionlogout, search, current_module, urlhref,
#                  sessionupdateroledata):
#     moduleauthorized = True
#     sessiontimeout = False
#     clear_sessioncurrentrole = False
#     if sessionlastchange:
#         sessionlastchange = datetime.strptime(sessionlastchange, '%Y-%m-%dT%H:%M:%S.%f')
#         minutesdiff = (datetime.now() - sessionlastchange).total_seconds()/60
#         if minutesdiff > 15 and not sessionlogout:
#             open= True
#         else:
#             open=False
#     else:
#         open=False
#     ctx = dash.callback_context
#
#     if ctx.triggered:
#         eventid = ctx.triggered[0]['prop_id'].split('.')[0]
#
#         if eventid in ['url', 'sessionupdaterole']:
#             return [open]
#         else:
#             return [false]
#     else:
#         raise PreventUpdate
#
# Main Router Function


@app.callback([Output('page-content', 'children'),
               Output('sessionlastchange', 'data'),
               Output('sessionlogout', 'data'),
               Output('current_module', 'data'),
               Output('sessioncurrentrole', 'clear_data'),

               # Output('url','search')
               ],
              [
              Input('url', 'pathname'),
              #  Input('sessionupdaterole', 'modified_timestamp'),
              # Input('ddroledropdown', 'value'),
              # Input('sessioncurrentrole', 'data'),
              ],
              [
              State('sessionmenudict', 'data'),
              State('sessioncurrentrole', 'data'),
              State('sessiondefaultrole', 'data'),
              State('current_user_id', 'data'),
              State('sessionlastchange', 'data'),
              State('sessionlogout', 'data'),
              State('url', 'search'),
              State('current_module', 'data'),
              State('url', 'href'),
              State('sessionupdaterole', 'data'),
              ])
def display_page(pathname,  # sessionupdaterole,
                 sessionmenudict,
                 sessioncurrentrole, sessiondefaultrole, current_user_id, sessionlastchange, sessionlogout, search, current_module, urlhref,
                 sessionupdateroledata):
    moduleauthorized = True
    sessiontimeout = False
    clear_sessioncurrentrole = False

    # if sessionlogout==True:
    #     raise PreventUpdate
#    print('sessionupdateroledata',sessionupdateroledata)
#    print('current_user_id',current_user_id)
# print('sessionlogout',sessionlogout)
#    print(sessionupdaterole)
    #print('printing  after sessionupdaterole')

    # local_vars = list(locals().items())
    # total_memory=0
    # for var, obj in local_vars:
    #     #print(var, sys.getsizeof(obj))
    #     total_memory=sys.getsizeof(obj)+total_memory
    #
    # print("totalmemory", total_memory)
    if sessionlastchange:
        sessionlastchange = datetime.strptime(sessionlastchange, '%Y-%m-%dT%H:%M:%S.%f')
        minutesdiff = (datetime.now() - sessionlastchange).total_seconds()/60
        if minutesdiff > 30 and not sessionlogout:
            sessiontimeout = True
    sessionlastchange = datetime.now()
    returnlayout = []
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        # print("index event", eventid)
        if eventid == 'url':

            if sessionmenudict:
                menudict = pd.DataFrame.from_dict(sessionmenudict)
                if sessiondefaultrole and not sessioncurrentrole:
                    selectedrole = sessiondefaultrole
                else:
                    selectedrole = sessioncurrentrole
                menudict = menudict[menudict["role_id"] == selectedrole]
                newpathname = pathname.replace('_profile', '')
                if (menudict['module_link'] == newpathname).sum() == 1:
                    moduleauthorized = True
                else:
                    moduleauthorized = False
                if not menudict[menudict['module_link'] == pathname].empty:
                    if menudict[menudict['module_link'] == pathname]["module_is_open"].iloc[0]:
                        moduleopen = True
                    else:
                        moduleopen = False
                else:
                    moduleopen = True
            if pathname == '/' or current_user_id == -1 or not current_user_id or sessiontimeout:
                if pathname == '/privacy':
                    returnlayout = privacy.layout
                elif pathname == '/siteinfo':
                    returnlayout = siteinfo.layout
                # elif pathname == '/api/emp_is_active':
                #     returnlayout = emp_is_active.layout
                    #current_module = "Request New Document"
                else:
                    returnlayout = login.layout
                    sessionlogout = True
            elif pathname == '/privacy':
                returnlayout = privacy.layout
            elif pathname == '/siteinfo':
                returnlayout = siteinfo.layout
            elif pathname == '/login':
                returnlayout = login.layout
                sessionlogout = True

            elif pathname == '/reports/reports_viewing':
                current_module = "Reports Dashboard"
                if search == '?report_id=1':
                    returnlayout = report1.layout
                elif search == '?report_id=2':
                    returnlayout = report2.layout
                elif search == '?report_id=3':
                    returnlayout = report3.layout
                elif search == '?report_id=4':
                    returnlayout = report4.layout
                elif search == '?report_id=5':
                    returnlayout = report5.layout
                elif search == '?report_id=6':
                    returnlayout = report6.layout
                elif search == '?report_id=7':
                    returnlayout = report7.layout
                elif search == '?report_id=8':
                    returnlayout = report8.layout
                elif search == '?report_id=9':
                    returnlayout = report9.layout
                elif search == '?report_id=10':
                    returnlayout = report10.layout
                elif search == '?report_id=11':
                    returnlayout = report11.layout
                elif search == '?report_id=12':
                    returnlayout = report12.layout
                elif search == '?report_id=13':
                    returnlayout = report13.layout
                elif search == '?report_id=14':
                    returnlayout = report14.layout
                elif search == '?report_id=15':
                    returnlayout = report15.layout
                elif search == '?report_id=16':
                    returnlayout = report16_currentbpsinprocess.layout
                elif search == '?report_id=17':
                    returnlayout = report17_currentleaveapplications.layout
                elif search == '?report_id=18':
                    returnlayout = report18_additionalassignments.layout
            elif moduleopen == False:
                returnlayout = module_closed.layout
                current_module = "Home"
            elif pathname == '/home' or not moduleauthorized:
                returnlayout = home.layout
                current_module = "Home"
            elif pathname == '/settings':
                returnlayout = settings.layout
            elif pathname == '/settings/settings_users':
                returnlayout = settings_users.layout
                current_module = "Users"
            elif pathname == '/settings/settings_modules':
                returnlayout = settings_modules.layout
                current_module = "Modules"
            elif pathname == '/settings/settings_users_profile':
                returnlayout = settings_users_profile.layout
                current_module = "Users"
            elif pathname == '/settings/settings_modules_profile':
                returnlayout = settings_modules_profile.layout
                current_module = "Modules"
            elif pathname == '/settings/settings_bp_approval_flows':
                returnlayout = settings_bp_approval_flows.layout
                current_module = "BP Approval Flows"
            elif pathname == '/settings/settings_bp_approval_flows_profile':
                returnlayout = settings_bp_approval_flows_profile.layout
                current_module = "BP Approval Flows"
            elif pathname == '/settings/settings_leave_approval_flows':
                returnlayout = settings_leave_approval_flows.layout
                current_module = "Leave Approval Flows"
            elif pathname == '/settings/settings_leave_approval_flows_profile':
                returnlayout = settings_leave_approval_flows_profile.layout
                current_module = "Leave Approval Flows"
            elif pathname == '/settings/settings_bp_flow_assignment':
                returnlayout = settings_bp_flow_assignment.layout
                current_module = "BP Flow Assignment"
            elif pathname == '/settings/settings_bp_flow_assignment_profile':
                returnlayout = settings_bp_flow_assignment_profile.layout
                current_module = "BP Flow Assignment"
            elif pathname == '/settings/settings_leave_flow_assignment':
                returnlayout = settings_leave_flow_assignment.layout
                current_module = "Leave Flow Assignment"
            elif pathname == '/settings/settings_leave_flow_assignment_profile':
                returnlayout = settings_leave_flow_assignment_profile.layout
                current_module = "Leave Flow Assignment"
            elif pathname == '/logout':
                returnlayout = login.layout
                sessionlogout = True
            elif pathname == '/settings/settings_roles':
                current_module = "Roles"
                returnlayout = settings_roles.layout
            elif pathname == '/settings/settings_roles_profile':
                current_module = "Roles"
                returnlayout = settings_roles_profile.layout
            elif pathname == '/settings/settings_module_roles':
                current_module = "Module Roles"
                returnlayout = settings_module_roles.layout
            elif pathname == '/settings/settings_module_roles_profile':
                returnlayout = settings_module_roles_profile.layout
                current_module = "Module Roles"
            elif pathname == '/settings/settings_user_roles':
                returnlayout = settings_user_roles.layout
                current_module = "User Roles"
            elif pathname == '/settings/settings_user_roles_profile':
                returnlayout = settings_user_roles_profile.layout
                current_module = "User Roles"
            elif pathname == '/settings/settings_doc_requirements':
                returnlayout = settings_doc_requirements.layout
                current_module = "Document Requirements"
            elif pathname == '/settings/settings_doc_requirements_profile':
                returnlayout = settings_doc_requirements_profile.layout
                current_module = "Document Requirements"
            elif pathname == '/settings/settings_bp_types':
                returnlayout = settings_bp_types.layout
                current_module = "BP Types"
            elif pathname == '/settings/settings_bp_types_profile':
                returnlayout = settings_bp_types_profile.layout
                current_module = "BP Types"
            elif pathname == '/settings/settings_bp_docs':
                returnlayout = settings_bp_docs.layout
                current_module = "BP Required Documents"
            elif pathname == '/settings/settings_bp_docs_profile':
                returnlayout = settings_bp_docs_profile.layout
                current_module = "BP Required Documents"
            elif pathname == '/settings/settings_leave_docs':
                returnlayout = settings_leave_docs.layout
                current_module = "Leave App Required Documents"
            elif pathname == '/settings/settings_leave_docs_profile':
                returnlayout = settings_leave_docs_profile.layout
                current_module = "Leave App Required Documents"
            elif pathname == '/settings/settings_leave_available_days':
                returnlayout = settings_leave_available_days.layout
                current_module = "Leave Maximum # of Days"
            elif pathname == '/settings/settings_leave_available_days_profile':
                returnlayout = settings_leave_available_days_profile.layout
                current_module = "Leave Maximum # of Days"
            elif pathname == '/settings/settings_degrees':
                returnlayout = settings_degrees.layout
                current_module = "Degrees"
            elif pathname == '/settings/settings_degrees_profile':
                returnlayout = settings_degrees_profile.layout
                current_module = "Degrees"
            elif pathname == '/settings/settings_degreeprograms_profile':
                returnlayout = settings_degreeprograms_profile.layout
                current_module = "Degrees"
            elif pathname == '/settings/settings_entitlements':
                returnlayout = settings_entitlements.layout
                current_module = "Entitlements"
            elif pathname == '/settings/settings_entitlements_profile':
                returnlayout = settings_entitlements_profile.layout
                current_module = "Entitlements"
            elif pathname == '/settings/settings_units':
                returnlayout = settings_units.layout
                current_module = "Units"
            elif pathname == '/settings/settings_units_profile':
                returnlayout = settings_units_profile.layout
                current_module = "Units"
            # elif pathname == '/settings/settings_entitlementtype':
            #     returnlayout = settings_entitlementtype.layout
            elif pathname == '/settings/settings_entitlementtype_profile':
                returnlayout = settings_entitlementtype_profile.layout
                current_module = "Entitlement Types"
            elif pathname == '/settings/settings_designations':
                returnlayout = settings_designations.layout
                current_module = "Designations"
            elif pathname == '/settings/settings_designations_profile':
                returnlayout = settings_designations_profile.layout
                current_module = "Designations"
            elif pathname == '/settings/settings_perfrating_query':
                returnlayout = settings_perfrating_query.layout
                current_module = "Performance Rating"
            elif pathname == '/settings/settings_perfrating_query_profile':
                returnlayout = settings_perfrating_query_profile.layout
                current_module = "Performance Rating"
            elif pathname == '/settings/settings_perfrating_management_profile':
                returnlayout = settings_perfrating_management_profile.layout
                current_module = "Performance Rating"
            elif pathname == '/settings/settings_salary_grades':
                returnlayout = settings_salary_grades.layout
                current_module = "Salary Grades"
            elif pathname == '/settings/settings_salary_grades_profile':
                returnlayout = settings_salary_grades_profile.layout
                current_module = "Salary Grades"
            elif pathname == '/settings/settings_personal_data':
                returnlayout = settings_personal_data.layout
                current_module = "Personal Data Editing/New Entry"
            elif pathname == '/settings/settings_personal_data_profile':
                returnlayout = settings_personal_data_profile.layout
                current_module = "Personal Data"
            elif pathname == '/settings/settings_personal_data_viewing':
                returnlayout = settings_personal_data_viewing.layout
                current_module = "Personal Data Viewing"
            elif pathname == '/settings/settings_personal_data_viewing_profile':
                returnlayout = settings_personal_data_viewing_profile.layout
                current_module = "Personal Data Viewing"
            elif pathname == '/settings/settings_person_employee_encoding':
                returnlayout = settings_person_employee_encoding.layout
                current_module = "Person/Employee Back-Encoding"
            elif pathname == '/settings/settings_employee_management':
                returnlayout = settings_employee_management.layout
                current_module = "Employee Management"
            elif pathname == '/settings/settings_employee_management_profile':
                returnlayout = settings_employee_management_profile.layout
                current_module = "Employee Management"
            elif pathname == '/settings/settings_admin_positions':
                returnlayout = settings_admin_positions.layout
                current_module = "Administrative Positions"
            elif pathname == '/settings/settings_admin_positions_profile':
                returnlayout = settings_admin_positions_profile.layout
                current_module = "Administrative Positions"
            elif pathname == '/settings/settings_appointment_offices':
                returnlayout = settings_appointment_offices.layout
                current_module = "Appointment Offices"
            elif pathname == '/settings/settings_appointment_offices_profile':
                returnlayout = settings_appointment_offices_profile.layout
                current_module = "Appointment Offices"
            elif pathname == '/settings/settings_admin_emp_assignment':
                returnlayout = settings_admin_emp_assignment.layout
                current_module = "Admin Employee Assignment"
            elif pathname == '/settings/settings_admin_emp_assignment_profile':
                returnlayout = settings_admin_emp_assignment_profile.layout
                current_module = "Admin Employee Assignment"
            elif pathname == '/settings/settings_schools':
                returnlayout = settings_schools.layout
                current_module = "Schools"
            elif pathname == '/settings/settings_schools_profile':
                returnlayout = settings_schools_profile.layout
                current_module = "Schools"
            elif pathname == '/settings/settings_bp_approval_statuses':
                returnlayout = settings_bp_approval_statuses.layout
                current_module = "BP Approval Statuses"
            elif pathname == '/settings/settings_bp_approval_statuses_profile':
                returnlayout = settings_bp_approval_statuses_profile.layout
                current_module = "BP Approval Statuses"
            elif pathname == '/settings/settings_leavetypes':
                returnlayout = settings_leavetypes.layout
                current_module = "Leave Types"
            elif pathname == '/settings/settings_leavetypes_profile':
                returnlayout = settings_leavetypes_profile.layout
                current_module = "Leave Types"
            elif pathname == '/servicerecord/query_faculty':
                returnlayout = query_faculty.layout
                current_module = "Service Record Management"
            elif pathname == '/servicerecord/sr_management':
                returnlayout = sr_management.layout
                current_module = "Service Records from BPs"
            elif pathname == '/servicerecord/sr_management_profile':
                returnlayout = sr_management_profile.layout
                current_module = "Service Record Management"
            elif pathname == '/settings/settings_plantilla_fill_statuses':
                returnlayout = settings_plantilla_fill_statuses.layout
                current_module = "Plantilla Fill Statuses"
            elif pathname == '/settings/settings_plantilla_fill_statuses_profile':
                returnlayout = settings_plantilla_fill_statuses_profile.layout
                current_module = "Plantilla Fill Statuses"
            # elif pathname == '/bp/bp_original_profile':
            #     returnlayout = bp_original_profile.layout
            elif pathname == '/settings/settings_role_reports':
                returnlayout = settings_role_reports.layout
                current_module = "Role Reports"
            elif pathname == '/settings/settings_role_reports_profile':
                returnlayout = settings_role_reports_profile.layout
                current_module = "Role Reports"
            elif pathname == '/payroll/payroll_query':
                returnlayout = payroll_query.layout
                current_module = "Payroll Report"
            elif pathname == '/plantilla/plantillamanagement_plantilla_items':
                returnlayout = plantillamanagement_plantilla_items.layout
                current_module = "Plantilla Items"
            elif pathname == '/plantilla/plantillamanagement_plantilla_items_profile':
                returnlayout = plantillamanagement_plantilla_items_profile.layout
                current_module = "Plantilla Items"
            elif pathname == '/plantilla/query_emp_plantilla':
                returnlayout = query_emp_plantilla.layout
                current_module = "Plantilla-Employees"
            elif pathname == '/plantilla/query_emp_plantilla_profile':
                returnlayout = query_emp_plantilla_profile.layout
                current_module = "Plantilla-Employees"
            elif pathname == '/plantilla/query_emp_plantilla_viewing':
                returnlayout = query_emp_plantilla_viewing.layout
                current_module = "Plantilla Viewing - Employee View"
            elif pathname == '/plantilla/query_emp_plantilla_viewing_profile':
                returnlayout = query_emp_plantilla_viewing_profile.layout
                current_module = "Plantilla Viewing - Employee View"
            elif pathname == '/plantilla/query_emp_plantilla_viewing_itemview':
                returnlayout = query_emp_plantilla_viewing_itemview.layout
                current_module = "Plantilla Viewing - Item View"
            elif pathname == '/plantilla/query_emp_plantilla_viewing_itemview_profile':
                returnlayout = query_emp_plantilla_viewing_itemview_profile.layout
                current_module = "Plantilla Viewing - Item View"
            elif pathname == '/plantilla/query_emp_plantilla_history':
                returnlayout = query_emp_plantilla_history.layout
                current_module = "Plantilla History"
            # elif pathname == '/plantilla/query_emp_plantilla_history_profile':
            #     returnlayout = query_emp_plantilla_history_profile.layout
            #     current_module = "Plantilla History"
            elif pathname == '/settings/settings_leaves':
                returnlayout = settings_leaves.layout
                current_module = "Settings"
            elif pathname == '/settings/settings_leaves_profile':
                returnlayout = settings_leaves_profile.layout
                current_module = "Settings"
            elif pathname == '/bp/bp_maintenance':
                returnlayout = bp_maintenance.layout
                current_module = "Basic Paper Maintenance"
            elif pathname == '/bp/bp_maintenance_profile':
                returnlayout = bp_maintenance_profile.layout
                current_module = "Basic Paper Maintenance"
            elif pathname == '/bp/bp_maintenance_profile':
                returnlayout = bp_maintenance_profile.layout
                current_module = "Basic Paper Maintenance"
            elif pathname == '/document_requests/requests_process':
                returnlayout = requests_process.layout
                current_module = "Process Document Requests"
            elif pathname == '/document_requests/requests_process_profile':
                returnlayout = requests_process_profile.layout
                current_module = "Process Document Requests"

            elif pathname == '/servicerecord/query_faculty_nosa':
                returnlayout = query_faculty_nosa.layout
                current_module = "NOSA"

            elif pathname == '/servicerecord/query_faculty_view':
                returnlayout = query_faculty.layout
                current_module = "Service Record Viewing"

            elif pathname == '/servicerecord/query_faculty_view':
                returnlayout = query_faculty.layout
                current_module = "Service Record Viewing"

            elif pathname == '/servicerecord/query_faculty_view_profile':
                returnlayout = query_faculty_profile.layout
                current_module = "Service Record Viewing"

            elif pathname == '/settings/settings_unit_emp':
                returnlayout = settings_unit_emp.layout
                current_module = "Employees Unit Tags"
            elif pathname == '/settings/settings_unit_emp_profile':
                returnlayout = settings_unit_emp_profile.layout
                current_module = "Employees Unit Tags"
            elif pathname == '/appointments/delegated_appointments':
                returnlayout = delegated_appointments.layout
                current_module = "College Delegated Appointments"
            elif pathname == '/appointments/delegated_appointments_profile':
                returnlayout = delegated_appointments_profile.layout
                current_module = "College Delegated Appointments"
            elif pathname == '/appointments/hrdo_appointments':
                returnlayout = hrdo_appointments.layout
                current_module = "Print BP/Appointment Papers"
            elif pathname == '/appointments/hrdo_appointments_profile':
                returnlayout = hrdo_appointments_profile.layout
                current_module = "Print BP/Appointment Papers"
            elif pathname == '/settings/settings_work_suspensions':
                returnlayout = settings_work_suspensions.layout
                current_module = "Work Suspensions"
            elif pathname == '/leaves/leave_approval':
                returnlayout = leave_approval.layout
                current_module = "Leave Approval"
            elif pathname == '/leaves/leave_approval_profile':
                returnlayout = leave_approval_profile.layout
                current_module = "Leave Approval"
            elif pathname == '/leaves/leave_viewing':
                returnlayout = leave_viewing.layout
                current_module = "Leaves Viewing"
            elif pathname == '/leaves/leave_viewing_profile':
                returnlayout = leave_viewing_profile.layout
                current_module = "Leaves Viewing"
            elif pathname == '/settings/settings_leave_approval_statuses':
                returnlayout = settings_leave_approval_statuses.layout
                current_module = "Leave Approval Statuses"
            elif pathname == '/settings/settings_leave_approval_statuses_profile':
                returnlayout = settings_leave_approval_statuses_profile.layout
                current_module = "Leave Approval Statuses"

            elif pathname == '/servicerecord/query_for_separation':
                returnlayout = query_for_separation.layout
                current_module = "Employees for Separation"

            elif pathname == '/separation/separations':
                returnlayout = separations.layout
                current_module = "Apply for Separation"
            elif pathname == '/separation/separations_profile':
                returnlayout = separations_profile.layout
                current_module = "Apply for Separation"
            elif pathname == '/separation/_printing':
                returnlayout = separations_printing.layout
                current_module = "Apply for Separation"
            elif pathname == '/leaves/leaves_cos_query':
                returnlayout = leaves_cos_query.layout
                current_module = "COS Entry"
            elif pathname == '/clearances/clearance_view':
                returnlayout = clearance_view.layout
                current_module = "View Clearances"
            elif pathname == '/clearances/clearance_view_profile':
                returnlayout = clearance_view_profile.layout
                current_module = "View Clearances"
            elif pathname == '/clearances/clearance_process':
                returnlayout = clearance_process.layout
                current_module = "Process Clearances"
            elif pathname == '/clearances/clearance_process_profile':
                returnlayout = clearance_process_profile.layout
                current_module = "Process Clearances"
            elif pathname == '/leaves/leaves_cos_query_profile':
                returnlayout = leaves_cos_query_profile.layout
                current_module = "COS Entry"
            elif pathname == '/leaves/leave_mandatory':
                returnlayout = leave_mandatory.layout
                current_module = "Mandatory Leave Deduction from VL Credits"
            elif pathname == '/separation/process_separations':
                returnlayout = process_separations.layout
                current_module = "Process Separation"
            elif pathname == '/separation/process_separations_profile':
                returnlayout = process_separations_profile.layout
                current_module = "Process Separation"
            elif pathname == '/clearances/clearance_status_roles':
                returnlayout = clearance_status_roles.layout
                current_module = "Set Clearance Role Statuses"
            elif pathname == '/clearances/clearance_status_roles_profile':
                returnlayout = clearance_status_roles_profile.layout
                current_module = "Set Clearance Role Statuses"
            elif pathname == '/settings/settings_clearance_stats':
                returnlayout = settings_clearance_stats.layout
                current_module = "Clearance Status Settings"
            elif pathname == '/settings/settings_clearance_stats_profile':
                returnlayout = settings_clearance_stats_profile.layout
                current_module = "Clearance Status Settings"
            elif pathname == '/job_portal/job_listings':
                returnlayout = job_listings.layout
                current_module = "Job Listings"
            elif pathname == '/job_portal/job_listings_profile':
                returnlayout = job_listings_profile.layout
                current_module = "Job Listings"
            elif pathname == '/job_portal/competencies':
                returnlayout = competencies.layout
                current_module = "Competencies"
            elif pathname == '/job_portal/competencies_profile':
                returnlayout = competencies_profile.layout
                current_module = "Competencies"
            elif pathname == '/job_portal/job_listing_applicants':
                returnlayout = job_listing_applicants.layout
                current_module = "Job Listing Applicants"
            elif pathname == '/job_portal/job_listing_applicants_profile':
                returnlayout = job_listing_applicants_profile.layout
                current_module = "Job Listing Applicants"
            elif pathname == '/job_portal/job_applicant_screening':
                returnlayout = job_applicant_screening.layout
                current_module = "Job Applicant Screening"

            elif pathname == '/settings/settings_documents':
                returnlayout = settings_documents.layout
                current_module = "Document Type Settings"
            elif pathname == '/settings/settings_documents_profile':
                returnlayout = settings_documents_profile.layout
                current_module = "Document Type Settings"
            elif pathname == '/document_requests/batch_requests':
                returnlayout = batch_requests.layout
                current_module = "Batch Request New Document"
            elif pathname == '/document_requests/batch_requests_profile':
                returnlayout = batch_requests_profile.layout
                current_module = "Batch Request New Document"
            else:
                returnlayout = login.layout
        elif eventid == 'sessionupdaterole':

            returnlayout = home.layout

            current_module = "Home"
            # print(sessionupdaterole)
        # elif eventid == 'sessioncurrentrole':1

        #     returnlayout = home.layout
        #     current_module = "Home"
        else:
            raise PreventUpdate

    if pathname == '/' or current_user_id == -1 or not current_user_id or sessiontimeout or pathname == '/logout':
        sessionlogout = True
        clear_sessioncurrentrole = True
    else:
        sessionlogout = False
        clear_sessioncurrentrole = False
    return [returnlayout, sessionlastchange, sessionlogout, current_module, clear_sessioncurrentrole]


if __name__ == '__main__':

    # Remove when deploying to prod:::###########25240
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)

    #####################################
    app.run_server(debug=False)
   # serve(app.server, port=8050)
