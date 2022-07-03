import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash
import re
from dash.dependencies import Input, Output, State, MATCH, ALL
from apps import commonmodules
import json
from dash.exceptions import PreventUpdate
from app import app
from apps import home
from apps.dbconnect import securequerydatafromdatabase, modifydatabase, modifydatabasereturnid
import hashlib
from datetime import datetime
import dash_table
import pandas as pd
import numpy as np
from dash_extensions import Keyboard
import urllib.parse as urlparse
from urllib.parse import parse_qs


layout = html.Div([
    commonmodules.get_header(),
    commonmodules.get_menu(),
    commonmodules.get_common_variables(),
    dcc.Store(id='activeunitids', storage_type='memory', data=[]),
    html.H1("Maintain Unit Tags of Employees"),
    dcc.Link('← Back to Main Search',
             href='/settings/settings_unit_emp'),
    html.Hr(),
    html.Div([
        dbc.Card([

            dbc.CardHeader(
                html.H4("Manage Employee Unit Tags"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([

                html.Hr(),

                dbc.Row([
                    dbc.Col([
                        html.H5("Personal Information", style={
                                'color': 'rgb(128,0,0)', "font-weight": "bold"})
                    ]),
                    dbc.Col([
                    ]),
                ]),
                html.Br(),


                dbc.Row([
                    dbc.Col([
                        dbc.Label("Last Name", style={"text-align": "left"}),
                    ], width=3),
                    dbc.Col([
                        dbc.Label(id="unit_emp__lname_srmanagemnt", style={
                                  "text-align": "left", 'color': 'black', 'font-weight': 'bold'})
                    ], width=9),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("First Name", style={"text-align": "left"}),
                    ], width=3),
                    dbc.Col([
                        dbc.Label(id="unit_emp__fname_srmanagemnt", style={
                                  "text-align": "left", 'color': 'black', 'font-weight': 'bold'})
                    ], width=9),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Middle Name", style={"text-align": "left"}),
                    ], width=3),
                    dbc.Col([
                        dbc.Label(id="unit_emp__mname_srmanagemnt", style={
                                  "text-align": "left", 'color': 'black', 'font-weight': 'bold'})
                    ], width=9),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Birthday", style={"text-align": "left"}),
                    ], width=3),
                    dbc.Col([
                        dbc.Label(id="unit_emp__bday_srmanagemnt", style={
                                  "text-align": "left", 'color': 'black', 'font-weight': 'bold'})
                    ], width=9),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Place of Birth", style={"text-align": "left"}),
                    ], width=3),
                    dbc.Col([
                        dbc.Label(id="unit_emp__placeofbirth_srmanagemnt", style={
                                  "text-align": "left", 'color': 'black', 'font-weight': 'bold'})
                    ], width=9),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Employee Number", style={"text-align": "left"}),
                    ], width=3),
                    dbc.Col([
                        dbc.Label(id="unit_emp__enum_srmanagemnt", style={
                                  "text-align": "left", 'color': 'black', 'font-weight': 'bold'})
                    ], width=9),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Main Unit:", style={"text-align": "left"}),
                    ], width=3),
                    dbc.Col([
                        dbc.Label(id="unit_emp__main_unit_srmanagemnt", style={
                                  "text-align": "left", 'color': 'black', 'font-weight': 'bold'})
                    ], width=9),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Primary Designation:", style={"text-align": "left"}),
                    ], width=3),
                    dbc.Col([
                        dbc.Label(id="unit_emp_designation_srmanagemnt", style={
                                  "text-align": "left", 'color': 'black', 'font-weight': 'bold'})
                    ], width=9),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Employee Status:", style={"text-align": "left"}),
                    ], width=3),
                    dbc.Col([
                        dbc.Label(id="unit_emp__status_srmanagemnt", style={
                                  "text-align": "left", 'color': 'black', 'font-weight': 'bold'})
                    ], width=9),
                ]),

                html.Hr(),


                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Select Unit:", width=4, style={"text-align": "left"}),
                                dbc.Col([
                                    dcc.Dropdown(
                                        options=[

                                        ],
                                        id='query_val_emp_units',
                                        searchable=True, clearable=True
                                    ),
                                ],
                                    width=8
                                )
                            ],
                            row=True
                        ),
                    ]),

                ]),
                dbc.Row([
                        dbc.Col([
                            dbc.Button("Add", id="emp_uni_list_add",
                                       color="primary", block=True),
                        ]),
                        ]),
                html.Hr(),
                html.H5("Unit List"),
                html.Div([

                ], id="emp_uni_list"),

            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])

@app.callback(
    [
        Output('emp_uni_list','children'),
        Output('activeunitids','data')
    ],
    [
        Input("unit_emp__fname_srmanagemnt", "children"),
        Input('emp_uni_list_add','n_clicks'),
        Input({'type': 'dynamic_unhide_unit', 'index': ALL}, 'n_clicks'),
        Input({'type': 'dynamic_setprim_unit', 'index': ALL}, 'n_clicks'),
    ],
    [
        State("url","pathname"),
        State("url", "search"),
        State('query_val_emp_units','value'),
        State('current_user_id', 'data'),
        State({'type': 'dynamic_unhide_unit', 'index': ALL}, 'children'),
        State({'type': 'dynamic_setprim_unit', 'index': ALL}, 'children'),
    ],
)
def updatefacultyprofile(unit_emp__fname_srmanagemnt, n_clicks,dynamic_unhide_unit,dynamic_setprim_unit, pathname,url, query_val_emp_units, current_user_id,
    dynamic_unhide_unit_children,dynamic_setprim_unit_children):
    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid=="unit_emp__fname_srmanagemnt"  and pathname == "/settings/settings_unit_emp_profile":
            empid = str(parse_qs(parsed.query)['eid'][0])
            sr_change_history,activeunitids = queryempunits(empid)
            return [sr_change_history,activeunitids ]
            pass
        elif eventid == 'emp_uni_list_add' and pathname == "/settings/settings_unit_emp_profile":
            if query_val_emp_units:
                empid = str(parse_qs(parsed.query)['eid'][0])
                values=[empid,query_val_emp_units, False, True,current_user_id, datetime.today(), False]
                sqlcommand = '''INSERT INTO emp_units(emp_id, unit_id, emp_unit_is_primary_home_unit, emp_unit_is_active,
                                emp_unit_inserted_by, emp_unit_inserted_on,emp_unit_delete_ind )
                                VALUES(%s,%s,%s,%s,%s,%s,%s)'''
                modifydatabase(sqlcommand, values)
                sr_change_history, activeunitids = queryempunits(empid)
                return [sr_change_history,activeunitids ]
            else:
                raise PreventUpdate
        else:
            empid = str(parse_qs(parsed.query)['eid'][0])
            index = json.loads(eventid)["index"]
            type = json.loads(eventid)["type"]
            if type=="dynamic_unhide_unit":
                values=[True, index,empid ]
                sqlupdate = ''' UPDATE emp_units SET
                         emp_unit_delete_ind=%s
                        WHERE unit_id = %s and emp_id=%s
                        '''
                modifydatabase(sqlupdate, values)
                sr_change_history,activeunitids = queryempunits(empid)
                return [sr_change_history,activeunitids ] 
            elif type=="dynamic_setprim_unit":
                values=[index,empid ]
                sqlupdate = ''' UPDATE employees SET
                         emp_primary_home_unit_id=%s
                        WHERE emp_id=%s
                         '''
                modifydatabase(sqlupdate, values)
                values=[False,empid ]
                sqlupdate = ''' UPDATE emp_units SET
                         emp_unit_is_primary_home_unit=%s
                        WHERE emp_id=%s
                         '''
                modifydatabase(sqlupdate, values)

                values=[True, index,empid, False ]
                sqlupdate = ''' UPDATE emp_units SET
                         emp_unit_is_primary_home_unit=%s
                        WHERE unit_id = %s and emp_id=%s and emp_unit_delete_ind = %s
                         '''
                modifydatabase(sqlupdate, values)
                # modifydatabase(sqlupdate, values)
                sr_change_history,activeunitids = queryempunits(empid)
                return [sr_change_history,activeunitids ]
    else:
        raise PreventUpdate
    #

def queryempunits(empid):
    sqlcommand = '''SELECT eu.unit_id, p.unit_name, c.unit_code, c.unit_name,
        CASE
           WHEN emp_unit_is_primary_home_unit=false
                THEN 'Additional'
           WHEN emp_unit_is_primary_home_unit=true
                THEN 'Primary'
        END,
        CASE
           WHEN emp_unit_is_active=false
                THEN 'InActive'
           WHEN emp_unit_is_active=true
                THEN 'Active'
        END

        FROM emp_units eu INNER JOIN units c ON c.unit_id =eu.unit_id
        INNER JOIN units p ON p.unit_id = c.unit_parent_id
        WHERE emp_id=%s and emp_unit_delete_ind = %s '''
    values = (empid,False)
    columns = ['unit_id', 'punit_name', 'unit_code','unit_name',
        'emp_unit_is_primary_home_unit', 'emp_unit_is_active']
    df = securequerydatafromdatabase(sqlcommand, values, columns)
    df.columns=["UnitIds", "Parent Unit", "Unit Code","Unit Name","Is Primary Unit","Row is Active?"]
    activeunitids = df['UnitIds'].to_list()

    data_dict = df.to_dict()
    linkcolumn = {}
    for index, row in df.iterrows():
        if row["Is Primary Unit"] == 'Primary':
            linkcolumn[index] = dbc.Button("Untag",id={'index':str(row["UnitIds"]), 'type': 'dynamic_unhide_unit'}, color="primary", className="mr-1", block=True, disabled=True )
        else:
            linkcolumn[index] = dbc.Button("Untag",id={'index':str(row["UnitIds"]), 'type': 'dynamic_unhide_unit'}, color="primary", className="mr-1", block=True )
    dictionarydata = {'Options': linkcolumn}
    data_dict.update(dictionarydata)
    linkcolumn = {}
    for index, row in df.iterrows():
        if row["Is Primary Unit"] == 'Primary':
            linkcolumn[index] = dbc.Button("Set As Primary",id={'index':str(row["UnitIds"]), 'type': 'dynamic_setprim_unit'}, color="success", className="mr-1", block=True, disabled=True )
        else:
            linkcolumn[index] = dbc.Button("Set As Primary",id={'index':str(row["UnitIds"]), 'type': 'dynamic_setprim_unit'}, color="success", className="mr-1", block=True )
    dictionarydata = {'Set As Primary': linkcolumn}
    data_dict.update(dictionarydata)



    df = pd.DataFrame.from_dict(data_dict)
    df = df[["Parent Unit", "Unit Code","Unit Name","Is Primary Unit","Row is Active?","Options","Set As Primary"]]
    sr_change_history = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

    return sr_change_history, activeunitids


@app.callback(
    [
        Output("unit_emp__fname_srmanagemnt", "children"),
        Output("unit_emp__mname_srmanagemnt", "children"),
        Output("unit_emp__lname_srmanagemnt", "children"),
        Output("unit_emp__bday_srmanagemnt", "children"),
        Output("unit_emp__placeofbirth_srmanagemnt", "children"),
        Output("unit_emp__enum_srmanagemnt", "children"),
        Output("unit_emp_designation_srmanagemnt", "children"),
        Output("unit_emp__main_unit_srmanagemnt", "children"),
        Output("unit_emp__status_srmanagemnt", "children"),
    ],
    [
        Input("url", "search"),
    ],
    [
        State("url", "pathname"),
    ],
)
def updatefacultyprofile(url, pathname):

    # ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    # if ctx.triggered:
    #     eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    #     print(eventid)
    if pathname == "/settings/settings_unit_emp_profile":
        empid = str(parse_qs(parsed.query)['eid'][0])
        sqlcommand = '''SELECT person_first_name, person_middle_name, person_last_name, to_char(person_dob,'Mon DD, YYYY'), person_pob, designation_name,
            unit_name, emp_is_active, emp_number
        FROM persons p INNER JOIN employees e on e.person_id = p.person_id
        LEFT JOIN designations d on d.designation_id = e.emp_primary_designation_id
        LEFT JOIN units u on u.unit_id = e.emp_primary_home_unit_id
        WHERE e.emp_id = %s and e.emp_delete_ind = %s'''
        values = (empid, False)
        columns = ['person_first_name', 'person_middle_name',
                   'person_last_name', 'person_dob', 'person_pob', 'designation_name', 'unit_name', 'emp_is_active', 'emp_number']
        df = securequerydatafromdatabase(sqlcommand, values, columns)
        person_first_name = df["person_first_name"][0]
        person_middle_name = df["person_middle_name"][0]
        person_last_name = df["person_last_name"][0]
        person_dob = df["person_dob"][0]
        person_pob = df["person_pob"][0]
        designation_name = df["designation_name"][0]
        unit_name = df["unit_name"][0]
        emp_number = df["emp_number"][0]
        # print(df["emp_is_active"][0])
        if df["emp_is_active"][0]:
            emp_is_active = "Active"
        else:
            emp_is_active = "Inactive"


        return [person_first_name, person_middle_name, person_last_name, person_dob, person_pob, emp_number, designation_name, unit_name, emp_is_active ]


    else:
        raise PreventUpdate
    # else:
    #     raise PreventUpdate





@app.callback(
    [
        #    Output('query_employee_class', 'options'),
        Output('query_val_emp_units', 'options'),
    ],
    [
        Input('activeunitids', 'modified_timestamp'),
    ],
    [
        State('activeunitids', 'data'),
        State("url", "pathname"),
            State('sessioncurrentunit', 'data'),
            State('sessionlistofunits', 'data'),
    ],
)
def query_emp_units(modified_timestamp,activeunitids,pathname,sessioncurrentunit,sessionlistofunits ):
    # print('activeunitids',tuple(activeunitids))
    # listofallowedunits = tuple(sessionlistofunits[str(sessioncurrentunit)])
    # print('listofallowedunits',tuple(listofallowedunits))
    #print(tuple(activeunitids))
    if pathname == "/settings/settings_unit_emp_profile" and activeunitids:
        listofunits = commonmodules.queryfordropdown('''
            SELECT CONCAT(unit_name,' (', unit_code, ') ') as label, unit_id as value
           FROM units
           WHERE unit_delete_ind = %s and unit_id NOT IN %s
           ORDER BY unit_name
        ''', (False, tuple(activeunitids)))

        # query_employee_class
        return [listofunits]
    else:
        listofunits = commonmodules.queryfordropdown('''
            SELECT CONCAT(unit_name,' (', unit_code, ') ') as label, unit_id as value
           FROM units
           WHERE unit_delete_ind = %s
           ORDER BY unit_name
        ''', (False, ))

        # query_employee_class
        return [listofunits]


#
# @app.callback([Output('queryfacultydiv_emp_unit', 'children')
#                ],
#               [
#
#     Input('btn_search_employees_emp_unit', 'n_clicks'),
#     Input("keyboard_query", "keydown")
# ],
#     [
#     State('searchname_emp_unit', 'value'),
#     State('query_employee_status_emp_unit', 'value'),
#     #State('query_employee_class', 'value'),
#     State('sessioncurrentunit', 'data'),
#     State('sessionlistofunits', 'data'),
#     State('current_user_id', 'data'),
#     State('searchnumber_emp_unit', 'value'),
#     State('query_emp_units', 'value'),
#     State('searchfname_emp_unit', 'value'),
#     State('url','pathname'),
#     State('query_emp_units_class','value')
# ],)
# def querylistofemployees(btn_search_employees_emp_unit, keydown, searchname_emp_unit, query_employee_status_emp_unit,  sessioncurrentunit, sessionlistofunits,  # query_employee_class
#                          current_user_id, searchnumber_emp_unit, query_emp_units, searchfname_emp_unit, pathname, query_emp_units_class):
#
#     listofallowedunits = tuple(sessionlistofunits[str(sessioncurrentunit)])
#     ctx = dash.callback_context
#
#     mode="view"
#     url='/settings/settings_unit_emp'
#     if ctx.triggered:
#         eventid = ctx.triggered[0]['prop_id'].split('.')[0]
#
#         if eventid == 'btn_search_employees_emp_unit':
#
#             if any([searchname_emp_unit, searchnumber_emp_unit, query_emp_units, searchfname_emp_unit]):  # query_employee_class
#             #concat(person_last_name, ', ',  person_first_name, ' ', person_middle_name)
#                 sqlcommand = '''SELECT emp_id, emp_number,
#
#                 coalesce(person_first_name, '') || ' ' || coalesce(person_middle_name, '') || ' ' || coalesce(person_last_name, '') || ' ' || coalesce(person_name_extension, '') AS name,
#
#
#                 unit_name, emp_class_name,
#                     emp_status_name, designation_name
#                 FROM persons p
#                 LEFT JOIN employees e ON e.person_id = p.person_id
#                 LEFT JOIN emp_classes ec ON ec.emp_class_id = e.emp_class_id
#                 LEFT JOIN emp_statuses es ON es.emp_status_id = e.emp_status_id
#                 LEFT JOIN units u ON e.emp_primary_home_unit_id = u.unit_id
#                 LEFT JOIN designations d ON e.emp_primary_designation_id= d.designation_id
#                 WHERE emp_delete_ind = %s
#                 '''
#                 values = [False]  # AND emp_primary_home_unit_id IN %s
#
#                 if 1 in query_employee_status_emp_unit:
#                     sqlcommand = sqlcommand + " AND e.emp_is_active = %s "
#                     values.append(True)
#
#                 if query_emp_units_class:
#                     sqlcommand = sqlcommand + " AND e.emp_class_id = %s "
#                     values.append(query_emp_units_class)
#
#                 if searchname_emp_unit:
#                     sqlcommand = sqlcommand + " AND person_last_name ILIKE %s "  # + \
#                     values.append(searchname_emp_unit+'%')
#
#                 if searchfname_emp_unit:
#                     sqlcommand = sqlcommand + " AND person_first_name ILIKE %s "  # + \
#                     values.append('%'+searchfname_emp_unit+'%')
#
#                 if searchnumber_emp_unit:
#                     sqlcommand = sqlcommand + " AND emp_number ILIKE %s "  # + \
#                     values.append('%'+searchnumber_emp_unit+'%')
#
#                 if query_emp_units:
#                     sqlcommand = sqlcommand + " AND unit_id = %s "  # + \
#                     values.append(query_emp_units)
#
#                 sqlcommand = sqlcommand + " ORDER BY person_last_name"
#             else:
#                 raise PreventUpdate
#                 sqlcommand = '''SELECT emp_id, emp_number, concat(person_last_name, ', ',  person_first_name, ' ', person_middle_name) AS name, unit_name, emp_class_name,
#                     emp_status_name, designation_name
#                 FROM persons p
#                 LEFT JOIN employees e ON e.person_id = p.person_id
#                 LEFT JOIN emp_classes ec ON ec.emp_class_id = e.emp_class_id
#                 LEFT JOIN emp_statuses es ON es.emp_status_id = e.emp_status_id
#                 LEFT JOIN units u ON e.emp_primary_home_unit_id = u.unit_id
#                 LEFT JOIN designations d ON e.emp_primary_designation_id= d.designation_id
#                 WHERE emp_delete_ind = %s
#                 AND emp_is_active = %s
#                 ORDER BY person_last_name'''
#                 values = (False, True)  # AND emp_primary_home_unit_id IN %s
#
#             columns = ['emp_id', 'emp_number', 'name', 'unit_name',
#                        'emp_class', 'emp_status_name', 'designation_name']
#             df = securequerydatafromdatabase(sqlcommand, values, columns)
#             df.columns = ["emp_id", "Emp Number", "Name", "Unit Name",
#                           "Employee Class", "Status Name", "Designation Name"]
#             columns = [{"name": i, "id": i} for i in df.columns]
#             data = df.to_dict("rows")
#             linkcolumn = {}
#             for index, row in df.iterrows():
#                 linkcolumn[index] = dcc.Link(
#                     'View', href=url+'?eid='+str(row["emp_id"])+'&mode='+mode)
#             df = df[["Emp Number", "Name", "Unit Name",
#                      "Employee Class", "Status Name", "Designation Name"]]
#             data_dict = df.to_dict()
#             dictionarydata = {'Select': linkcolumn}
#             data_dict.update(dictionarydata)
#             df = pd.DataFrame.from_dict(data_dict)
#             table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
#             return [table]
#         elif not keydown:
#             raise PreventUpdate
#         elif keydown['key'] == 'Enter':
#
#             if any([searchname_emp_unit, searchnumber_emp_unit, query_emp_units, searchfname_emp_unit]):  # query_employee_class
#
#                 sqlcommand = '''SELECT emp_id, emp_number,
#
#                 coalesce(person_first_name, '') || ' ' || coalesce(person_middle_name, '') || ' ' || coalesce(person_last_name, '') || ' ' || coalesce(person_name_extension, '') AS name,
#
#
#                 unit_name, emp_class_name,
#                     emp_status_name, designation_name
#                 FROM persons p
#                 LEFT JOIN employees e ON e.person_id = p.person_id
#                 LEFT JOIN emp_classes ec ON ec.emp_class_id = e.emp_class_id
#                 LEFT JOIN emp_statuses es ON es.emp_status_id = e.emp_status_id
#                 LEFT JOIN units u ON e.emp_primary_home_unit_id = u.unit_id
#                 LEFT JOIN designations d ON e.emp_primary_designation_id= d.designation_id
#                 WHERE emp_delete_ind = %s
#                 '''
#                 values = [False]  # AND emp_primary_home_unit_id IN %s
#
#                 if 1 in query_employee_status_emp_unit:
#                     sqlcommand = sqlcommand + " AND e.emp_is_active = %s "
#                     values.append(True)
#                 if searchfname_emp_unit:
#                     sqlcommand = sqlcommand + " AND person_first_name ILIKE %s "  # + \
#                     values.append('%'+searchfname_emp_unit+'%')
#                 if query_emp_units_class:
#                     sqlcommand = sqlcommand + " AND e.emp_class_id = %s "
#                     values.append(query_emp_units_class)
#
#                 if searchname_emp_unit:
#                     sqlcommand = sqlcommand + " AND person_last_name ILIKE %s "  # + \
#                     values.append(searchname_emp_unit+'%')
#
#                 if searchnumber_emp_unit:
#                     sqlcommand = sqlcommand + " AND emp_number ILIKE %s "  # + \
#                     values.append('%'+searchnumber_emp_unit+'%')
#
#                 if query_emp_units:
#                     sqlcommand = sqlcommand + " AND unit_id = %s "  # + \
#                     values.append(query_emp_units)
#
#                 sqlcommand = sqlcommand + " ORDER BY person_last_name"
#             else:
#                 raise PreventUpdate
#                 sqlcommand = '''SELECT emp_id, emp_number, concat(person_last_name, ', ',  person_first_name, ' ', person_middle_name) AS name, unit_name, emp_class_name,
#                     emp_status_name, designation_name
#                 FROM persons p
#                 LEFT JOIN employees e ON e.person_id = p.person_id
#                 LEFT JOIN emp_classes ec ON ec.emp_class_id = e.emp_class_id
#                 LEFT JOIN emp_statuses es ON es.emp_status_id = e.emp_status_id
#                 LEFT JOIN units u ON e.emp_primary_home_unit_id = u.unit_id
#                 LEFT JOIN designations d ON e.emp_primary_designation_id= d.designation_id
#                 WHERE emp_delete_ind = %s
#                 AND emp_is_active = %s
#                 ORDER BY person_last_name'''
#                 values = (False, True)  # AND emp_primary_home_unit_id IN %s
#
#             columns = ['emp_id', 'emp_number', 'name', 'unit_name',
#                        'emp_class', 'emp_status_name', 'designation_name']
#             df = securequerydatafromdatabase(sqlcommand, values, columns)
#             df.columns = ["emp_id", "Emp Number", "Name", "Unit Name",
#                           "Employee Class", "Status Name", "Designation Name"]
#             columns = [{"name": i, "id": i} for i in df.columns]
#             data = df.to_dict("rows")
#             linkcolumn = {}
#             for index, row in df.iterrows():
#                 linkcolumn[index] = dcc.Link(
#                     'View', href=url+'?eid='+str(row["emp_id"])+'&mode='+mode)
#             df = df[["Emp Number", "Name", "Unit Name",
#                      "Employee Class", "Status Name", "Designation Name"]]
#             data_dict = df.to_dict()
#             dictionarydata = {'Select': linkcolumn}
#             data_dict.update(dictionarydata)
#             df = pd.DataFrame.from_dict(data_dict)
#             table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
#             return [table]
#         else:
#             raise PreventUpdate
#     else:
#         raise PreventUpdate
# # @app.callback([
# #                ],
# #               [
# #     Input('searchname_emp_unit', 'value'),
# #     # Input('usersubmitstatus', 'value'),
# # ],
# #     [
# # ],)
# # def querylistofemployees(searchname_emp_unit):
# #     return []
