import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash
import re
from dash.dependencies import Input, Output, State, MATCH, ALL
from apps import commonmodules
from apps.commonmodules import queryfordropdown
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
from datetime import datetime as dt
from datetime import date


layout = html.Div([
    commonmodules.get_header(),
    commonmodules.get_menu(),
    commonmodules.get_common_variables(),
    html.H1("Administrative Position Employee Assignment"),
    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Administrative Position Employee Filters"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Search Last Name:", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="admin_emp_searchname", placeholder="Enter search name"
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
                            dbc.Button("Search", id="admin_emp_btn_search_employees",
                                       color="primary", block=True),
                        ]),
                        dbc.Col([
                        
                        ]),
                        ]),
                html.Hr(),
                html.H5("Administrative Position Employees"),
                html.Br(),
                html.Div([
                    dbc.Button("Link Admin Position to Employee", color="primary", className="mr-1",
                               id="btn_add_admin_emp_member"),
                ], style={"width": "32%", "verticalAlign": "top", "display": "inline-block", "margin-right": "1%"}),
                html.Div([
                ], style={"width": "32%", "verticalAlign": "top", "display": "inline-block", "margin-right": "1%"}),
                # html.Div([
                #     dbc.Button("Delete Selected DAPC", color="primary", className="mr-1",
                #                id="btn_delete_admin_emp_member"),
                # ], style={"width": "32%", "verticalAlign": "top", "display": "inline-block", "margin-right": "1%"}),
                html.Br(),
                html.Br(),
                html.Div([
                ], id="admin_emp_queryfacultydiv"),
                dbc.Modal(
                    [
                        dbc.ModalHeader("Success!", id="admin_emp_message_modalhead"),
                        dbc.ModalBody("You have successfully linked an administrative position to an employee.",
                                      id="admin_emp_message_modalbody"),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="admin_emp_message_modalclose",
                                       className="ml-auto")
                        ),
                    ],
                    id="admin_emp_message_modal",
                    centered=True,
                    backdrop='static'
                ),
                dbc.Modal(  # Modal add dapc
                    [
                        dbc.ModalHeader(
                            "Link an Employee to Administrative Position"),
                        dbc.ModalBody([
                            html.Br(),
                            html.Div([
                                dbc.FormGroup(
                                    [
                                        dbc.Label("Administrative Position", width=2,
                                                  style={"text-align": "left"}),
                                        dbc.Col([
                                            dcc.Dropdown(
                                                id="admin_emp_pos_dd",
                                                options=[
                                                ],
                                                # value="",
                                                searchable=True,
                                                clearable=True
                                            )
                                            #dbc.FormFeedback("Too short or already taken", valid = False)
                                        ],
                                            width=8
                                        )],
                                    row=True
                                ),
                                # dbc.FormGroup(
                                #     [
                                #         dbc.Label("Unit", width=2, style={"text-align": "left"}),
                                #         dbc.Col([
                                #             dcc.Dropdown(
                                #                 id="admin_emp_unit_dd",
                                #                 options=[
                                #                 ],
                                #                 # value="",
                                #                 searchable=True,
                                #                 clearable=True
                                #             )
                                #             #dbc.FormFeedback("Too short or already taken", valid = False)
                                #         ],
                                #             width=8
                                #         )],
                                #     row=True
                                # ),
                                html.Br(),
                                html.Div(
                                    [
                                        dbc.Label("Select Faculty to Link to Administrative Position:", width=8,
                                                  style={"text-align": "left"}),
                                        html.Br(),
                                        dash_table.DataTable(
                                            id='dt_add_admin_emp_member',
                                            row_selectable="single",
                                            # row_deletable=True,
                                            style_header={
                                                # '#a88f75',
                                                'minwidth': '100%',
                                                'backgroundColor': 'black', 'color': 'white',
                                                'whiteSpace': 'normal', 'fontWeight': 'bold', 'fontSize': 14, 'font-family': 'sans-serif'
                                            },
                                            style_cell={'textAlign': 'center',
                                                        #            # 'minWidth': '120px', 'width': '100px',
                                                        #            'maxWidth': '100px',
                                                        'textOverflow': 'ellipsis',
                                                        'maxWidth': 0,
                                                        'height': 'auto',
                                                        'whiteSpace': 'normal',
                                                        'fontSize': 13, 'font-family': 'sans-serif', 'textAlign': 'center'},
                                            css=[{
                                                'selector': '.dash-cell div.dash-cell-value',
                                                'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                                            }],
                                            style_cell_conditional=[
                                                {
                                                    'if': {'row_index': 'odd'},
                                                    'backgroundColor': 'rgb(248, 248, 248)'
                                                },
                                                {
                                                    'if': {'column_id': 'Unit'},
                                                    'width': '30%'
                                                },
                                                {
                                                    'if': {'column_id': 'Employee ID'},
                                                    'width': '10%'
                                                },
                                            ],

                                            style_table={'width': '90%',
                                                         'marginRight': '5%', 'marginLeft': '5%'},
                                            # editable=True,
                                            persistence=True,
                                            persistence_type="session",
                                            persisted_props=["data"],
                                        )  # end of data table
                                    ], style={'marginRight': '5%', 'display': 'inline-block', 'width': '100%'}
                                ),  # end of Div of the data table

                            ]),

                            html.Br(),
                        ]),
                        dbc.ModalFooter([
                            dbc.Button("Save and Close", id="btn_modal_admin_emp_member_close",
                                       className="ml-auto"),
                            dbc.Button("Cancel", id="btn_modal_admin_emp_member_cancel",
                                       className="ml-auto")
                        ]),
                    ],
                    id="modal_admin_emp_select_member",
                    centered=True,
                    backdrop='static',
                    size="xl",
                ),
                html.Div([
                    dcc.Input(id='admin_emp_submit_status', type='text', value="0")
                ], style={'display': 'none'}),

            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


# def returnselectedrows(dftable, ncolumns):
#     selectedrows = []
#     if dftable:
#         for i in range(0, len(dftable['props']['children'][1]['props']['children'])):
#             if 1 not in dftable['props']['children'][1]['props']['children'][i]['props']['children'][ncolumns-1]['props']['children']['props']['value']:
#                 selectedrows.append(i)
#     return selectedrows


@app.callback(
    [
        Output('admin_emp_queryfacultydiv', 'children'),
        Output('modal_admin_emp_select_member', 'is_open'),
        Output('dt_add_admin_emp_member', 'columns'),
        Output('dt_add_admin_emp_member', 'data'),
        Output('admin_emp_message_modal', 'is_open'),
        Output('admin_emp_message_modalbody', 'children'),
        Output('admin_emp_message_modalhead', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('admin_emp_btn_search_employees', 'n_clicks'),
        Input("btn_modal_admin_emp_member_close", "n_clicks"),
        Input('btn_add_admin_emp_member', 'n_clicks'),
        Input("btn_modal_admin_emp_member_cancel", "n_clicks"),
        Input('admin_emp_message_modalclose', 'n_clicks'),
        Input('admin_emp_submit_status', 'value')
        # Input('btn_delete_admin_emp_member', 'n_clicks')

    ],
    [
        State('admin_emp_searchname', 'value'),
        State('sessioncurrentunit', 'data'),
        State('current_user_id', 'data'),
        State('modal_admin_emp_select_member', 'is_open'),
        #State("admin_emp_unit_dd", "value"),
        State("admin_emp_pos_dd", "value"),
        State('dt_add_admin_emp_member', 'data'),
        State('dt_add_admin_emp_member', 'selected_rows'),
        State('sessionlistofunits', 'data'),
    ],
)
def querylistofadminemployees(path,
                              admin_emp_btn_search_employees,
                              btn_modal_admin_emp_member_close,
                              btn_add_admin_emp_member,
                              btn_modal_admin_emp_member_cancel,
                              admin_emp_message_modalclose,
                              admin_emp_submit_status,
                              searchname,
                              sessioncurrentunit,
                              current_user_id,
                              modal_is_open,
                              # admin_emp_unit_dd,
                              admin_emp_pos_dd,
                              dtdata,
                              selected_rows,
                              sessionlistofunits):
    ctx = dash.callback_context
    listofallowedunits = tuple(sessionlistofunits[str(sessioncurrentunit)])


    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        df = pd.DataFrame(columns=["Last Name", "First Name", "Middle Name"])
        if eventid == 'admin_emp_btn_search_employees':
            if any(searchname):
                searchname = "%"+searchname+"%"
                sqlcommand = '''
                            SELECT ae.admin_emp_id, emp.emp_number, design.designation_name, un.unit_name,  per.person_last_name, per.person_first_name,
                            CASE
        						WHEN ae.admin_emp_is_active = True THEN 'True'
        						WHEN ae.admin_emp_is_active = False THEN 'False'
        						ELSE ''
        					END AS admin_emp_is_active
                              FROM admin_employees ae
        					INNER JOIN admin_positions ap ON ap.admin_pos_id = ae.admin_pos_id
                            INNER JOIN designations design ON design.designation_id = ap.admin_designation_id
                            INNER JOIN employees emp ON emp.emp_id = ae.emp_id
                            INNER JOIN persons per ON per.person_id = emp.person_id
        					INNER JOIN units un ON un.unit_id = ap.admin_pos_unit_id
                             WHERE ap.admin_pos_unit_id IN %s
                              AND admin_emp_is_active = %s
                              AND admin_emp_delete_ind = %s
                              AND per.person_last_name ILIKE %s
                        '''
                values = (listofallowedunits, True, False, searchname)
            else:
                sqlcommand = '''
                            SELECT ae.admin_emp_id, emp.emp_number, design.designation_name, un.unit_name,  per.person_last_name, per.person_first_name,
                            CASE
        						WHEN ae.admin_emp_is_active = True THEN 'True'
        						WHEN ae.admin_emp_is_active = False THEN 'False'
        						ELSE ''
        					END AS admin_emp_is_active
                              FROM admin_employees ae
        					INNER JOIN admin_positions ap ON ap.admin_pos_id = ae.admin_pos_id
                            INNER JOIN designations design ON design.designation_id = ap.admin_designation_id
                            INNER JOIN employees emp ON emp.emp_id = ae.emp_id
                            INNER JOIN persons per ON per.person_id = emp.person_id
        					INNER JOIN units un ON un.unit_id = ap.admin_pos_unit_id
                             WHERE ap.admin_pos_unit_id IN %s
                              AND admin_emp_is_active = %s
                              AND admin_emp_delete_ind = %s
                        '''
                values = (listofallowedunits, True, False)
            columns = ['admin_emp_id', 'emp_number', 'admin_pos_name', 'unit_name', 'person_last_name', 'person_first_name',
                       'admin_emp_is_active']
            df = securequerydatafromdatabase(sqlcommand, values, columns)

            df.columns = ["Admin Employee ID", "Employee Number",
                          "Admin Position", "Unit", "Last Name", "First Name", "Active"]
            columns = [{"name": i, "id": i} for i in df.columns]
            data = df.to_dict("rows")
            linkcolumn = {}
            editcolumn = {}
            for index, row in df.iterrows():
                editcolumn[index] = dcc.Link(
                    'Edit', href='/settings/settings_admin_emp_assignment_profile?admin_emp_id='+str(row["Admin Employee ID"])+'&mode=edit')
            # for index, row in df.iterrows():
            #     linkcolumn[index] = dbc.Checklist(options=[{"label": "", "value": 1}], value=[])
            data_dict = df.to_dict()
            dictionarydata = {'Edit': editcolumn}
            # dictionarydata2 = {'Delete': linkcolumn}
            data_dict.update(dictionarydata)
            # data_dict.update(dictionarydata2)
            df = pd.DataFrame.from_dict(data_dict)
            table = dbc.Table.from_dataframe(df,
                                             striped=True,
                                             bordered=True,
                                             hover=True,
                                             style={'text-align': 'center'})
            return [table, False, "", "", "", "", ""]
        elif eventid in ['btn_modal_admin_emp_member_close']:
            try:
                empid = dtdata[selected_rows[0]]["Employee ID"]
                empidcheck = 1
            except:
                empid = 0
                empidcheck = None
            sql2 = '''
                    SELECT ae.admin_emp_id, ap.admin_pos_id, per.person_last_name, per.person_first_name
                      FROM admin_employees ae
                    INNER JOIN employees emp ON emp.emp_id = ae.emp_id
                    INNER JOIN persons per ON per.person_id = emp.person_id
                    INNER JOIN admin_positions ap ON ap.admin_pos_id = ae.admin_pos_id
                     WHERE emp.emp_id = %s
                      AND ap.admin_pos_id = %s
                      AND admin_emp_is_active = %s
                      AND admin_emp_delete_ind = %s
                      AND emp.emp_delete_ind = %s
            ''' #AND ap.admin_pos_unit_id IN %s  #removed this to accommodate 1 person to many positions

            values = (empid, admin_emp_pos_dd, True, False, False)
            columns = ['admin_emp_id', 'admin_pos_id', 'admin_emp_member_is_active',
                       'admin_emp_member_delete_ind']
            df2 = securequerydatafromdatabase(sql2, values, columns)

            if (df2.shape[0] == 0) and admin_emp_pos_dd and (empidcheck is not None):
                # sqlcommand = '''
                #             SELECT ae.admin_emp_id, emp.emp_number, design.designation_name, un.unit_name,  per.person_last_name, per.person_first_name,
                #             CASE
                # 				WHEN ae.admin_emp_is_active = True THEN 'True'
                # 				WHEN ae.admin_emp_is_active = False THEN 'False'
                # 				ELSE ''
                # 			END AS admin_emp_is_active
                #               FROM admin_employees ae
                # 			INNER JOIN admin_positions ap ON ap.admin_pos_id = ae.admin_pos_id
                #           INNER JOIN designations design ON design.designation_id = ap.admin_designation_id
                #             INNER JOIN employees emp ON emp.emp_id = ae.emp_id
                #             INNER JOIN persons per ON per.person_id = emp.person_id
                # 			INNER JOIN units un ON un.unit_id = ap.admin_pos_unit_id
                #              WHERE ap.admin_pos_unit_id IN %s
                #               AND admin_emp_is_active = %s
                #               AND admin_emp_delete_ind = %s
                #               AND
                #         '''
                # values = (listofallowedunits, True, False)
                # columns = ['admin_emp_id', 'emp_number', 'admin_pos_name', 'unit_name', 'person_last_name', 'person_first_name',
                #            'admin_emp_is_active']
                # df = securequerydatafromdatabase(sqlcommand, values, columns)
                # admin_pos_unit = df["admin_pos_unit"][0]

                sql = """
                    INSERT INTO admin_employees (admin_pos_id, emp_id, admin_emp_is_active, admin_emp_inserted_by, admin_emp_inserted_on, admin_emp_delete_ind)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                values = (admin_emp_pos_dd, empid, True, current_user_id, datetime.now(), False)
                modifydatabase(sql, values)
                admin_emp_submit_status = 1
            else:
                modal_head = 'Error in Saving'
                modal_message = 'Please review input details'

                sqlcommand = '''
                            SELECT ae.admin_emp_id, emp.emp_number, design.designation_name, un.unit_name,  per.person_last_name, per.person_first_name,
                            CASE
        						WHEN ae.admin_emp_is_active = True THEN 'True'
        						WHEN ae.admin_emp_is_active = False THEN 'False'
        						ELSE ''
        					END AS admin_emp_is_active
                              FROM admin_employees ae
        					INNER JOIN admin_positions ap ON ap.admin_pos_id = ae.admin_pos_id
                            INNER JOIN designations design ON design.designation_id = ap.admin_designation_id
                            INNER JOIN employees emp ON emp.emp_id = ae.emp_id
                            INNER JOIN persons per ON per.person_id = emp.person_id
        					INNER JOIN units un ON un.unit_id = ap.admin_pos_unit_id
                             WHERE ap.admin_pos_unit_id IN %s
                              AND admin_emp_is_active = %s
                              AND admin_emp_delete_ind = %s
                        '''
                values = (listofallowedunits, True, False)
                columns = ['admin_emp_id', 'emp_number', 'admin_pos_name', 'unit_name', 'person_last_name', 'person_first_name',
                           'admin_emp_is_active']
                df = securequerydatafromdatabase(sqlcommand, values, columns)

                df.columns = ["Admin Employee ID", "Employee Number", "Admin Position", "Unit", "Last Name", "First Name",
                              "Active?"]
                columns = [{"name": i, "id": i} for i in df.columns]
                data = df.to_dict("rows")
                linkcolumn = {}
                editcolumn = {}
                for index, row in df.iterrows():
                    editcolumn[index] = dcc.Link(
                        'Edit', href='/settings/settings_admin_emp_assignment_profile?admin_emp_id='+str(row["Admin Employee ID"])+'&mode=edit')
                # for index, row in df.iterrows():
                #     linkcolumn[index] = dbc.Checklist(options=[{"label": "", "value": 1}], value=[])
                data_dict = df.to_dict()
                dictionarydata = {'Edit': editcolumn}
                # dictionarydata2 = {'Delete': linkcolumn}
                data_dict.update(dictionarydata)
                # data_dict.update(dictionarydata2)
                df = pd.DataFrame.from_dict(data_dict)
                table = dbc.Table.from_dataframe(df,
                                                 striped=True,
                                                 bordered=True,
                                                 hover=True,
                                                 style={'text-align': 'center'})
                return [table, False, "", "", True, modal_message, modal_head]

            sqlcommand = '''
                        SELECT ae.admin_emp_id, emp.emp_number, design.designation_name, un.unit_name,  per.person_last_name, per.person_first_name,
                        CASE
    						WHEN ae.admin_emp_is_active = True THEN 'True'
    						WHEN ae.admin_emp_is_active = False THEN 'False'
    						ELSE ''
    					END AS admin_emp_is_active
                          FROM admin_employees ae
    					INNER JOIN admin_positions ap ON ap.admin_pos_id = ae.admin_pos_id
                        INNER JOIN designations design ON design.designation_id = ap.admin_designation_id
                        INNER JOIN employees emp ON emp.emp_id = ae.emp_id
                        INNER JOIN persons per ON per.person_id = emp.person_id
    					INNER JOIN units un ON un.unit_id = ap.admin_pos_unit_id
                         WHERE ap.admin_pos_unit_id IN %s
                          AND admin_emp_is_active = %s
                          AND admin_emp_delete_ind = %s
                    '''
            values = (listofallowedunits, True, False)
            columns = ['admin_emp_id', 'emp_number', 'admin_pos_name', 'unit_name', 'person_last_name', 'person_first_name',
                       'admin_emp_is_active']
            df = securequerydatafromdatabase(sqlcommand, values, columns)
            df.columns = ["Admin Employee ID", "Employee Number", "Admin Position", "Unit", "Last Name", "First Name",
                          "Active?"]
            columns = [{"name": i, "id": i} for i in df.columns]
            data = df.to_dict("rows")
            linkcolumn = {}
            editcolumn = {}
            for index, row in df.iterrows():
                editcolumn[index] = dcc.Link(
                    'Edit', href='/settings/settings_admin_emp_assignment_profile?admin_emp_id='+str(row["Admin Employee ID"])+'&mode=edit')
            # for index, row in df.iterrows():
            #     linkcolumn[index] = dbc.Checklist(options=[{"label": "", "value": 1}], value=[])
            data_dict = df.to_dict()
            dictionarydata = {'Edit': editcolumn}
            # dictionarydata2 = {'Delete': linkcolumn}
            data_dict.update(dictionarydata)
            # data_dict.update(dictionarydata2)
            df = pd.DataFrame.from_dict(data_dict)
            table = dbc.Table.from_dataframe(df,
                                             striped=True,
                                             bordered=True,
                                             hover=True,
                                             style={'text-align': 'center'})
            modal_message = "You have successfully linked an administrative position to an employee."
            modal_head = "Success!"
            return [table, False, "", "", True, modal_message, modal_head]
        elif eventid in ['admin_emp_message_modalclose']:
            sqlcommand = '''
                        SELECT ae.admin_emp_id, emp.emp_number, design.designation_name, un.unit_name,  per.person_last_name, per.person_first_name,
                        CASE
    						WHEN ae.admin_emp_is_active = True THEN 'True'
    						WHEN ae.admin_emp_is_active = False THEN 'False'
    						ELSE ''
    					END AS admin_emp_is_active
                          FROM admin_employees ae
    					INNER JOIN admin_positions ap ON ap.admin_pos_id = ae.admin_pos_id
                        INNER JOIN designations design ON design.designation_id = ap.admin_designation_id
                        INNER JOIN employees emp ON emp.emp_id = ae.emp_id
                        INNER JOIN persons per ON per.person_id = emp.person_id
    					INNER JOIN units un ON un.unit_id = ap.admin_pos_unit_id
                             WHERE ap.admin_pos_unit_id IN %s
                               AND admin_emp_is_active = %s
                               AND admin_emp_delete_ind = %s
                    '''
            values = (listofallowedunits, True, False)
            columns = ['admin_emp_id', 'emp_number', 'admin_pos_name', 'unit_name', 'person_last_name', 'person_first_name',
                       'admin_emp_is_active']
            df = securequerydatafromdatabase(sqlcommand, values, columns)

            df.columns = ["Admin Employee ID", "Employee Number", "Admin Position", "Unit", "Last Name", "First Name",
                          "Active?"]
            columns = [{"name": i, "id": i} for i in df.columns]
            data = df.to_dict("rows")
            linkcolumn = {}
            editcolumn = {}
            for index, row in df.iterrows():
                editcolumn[index] = dcc.Link(
                    'Edit', href='/settings/settings_admin_emp_assignment_profile?admin_emp_id='+str(row["Admin Employee ID"])+'&mode=edit')
            # for index, row in df.iterrows():
            #     linkcolumn[index] = dbc.Checklist(options=[{"label": "", "value": 1}], value=[])
            data_dict = df.to_dict()
            dictionarydata = {'Edit': editcolumn}
            # dictionarydata2 = {'Delete': linkcolumn}
            data_dict.update(dictionarydata)
            # data_dict.update(dictionarydata2)
            df = pd.DataFrame.from_dict(data_dict)
            table = dbc.Table.from_dataframe(df,
                                             striped=True,
                                             bordered=True,
                                             hover=True,
                                             style={'text-align': 'center'})
            return [table, False, "", "", False, "", ""]
        elif eventid == 'btn_add_admin_emp_member':  # assignment actual modal
            sqlcommand = """
                        SELECT emp.emp_id, un.unit_name, per.person_last_name, per.person_first_name, per.person_middle_name
                          FROM employees emp
                       INNER JOIN persons per ON per.person_id = emp.person_id
                       INNER JOIN units un ON un.unit_id = emp.emp_primary_home_unit_id
                           AND emp_is_active = %s
                           AND emp_primary_home_unit_id IN %s
                           AND emp_class_id = %s
                       ORDER BY person_last_name ASC
                        """
            values = (True, listofallowedunits, 1)  # change this to currentunitid
            columns = ['emp_id', 'unit_name',
                       'person_last_name', 'person_first_name', 'person_middle_name']
            df = securequerydatafromdatabase(sqlcommand, values, columns)

            df.columns = ["Employee ID", "Unit", "Last Name", "First Name", "Middle Name"]
            columns = [{"name": i, "id": i} for i in df.columns]  # list of dict
            data = df.to_dict("rows")
            return ["", True, columns, data, "", "", ""]
        elif eventid in ['btn_modal_admin_emp_member_cancel']:

            sqlcommand = '''
                        SELECT ae.admin_emp_id, emp.emp_number, design.designation_name, un.unit_name,  per.person_last_name, per.person_first_name,
                        CASE
    						WHEN ae.admin_emp_is_active = True THEN 'True'
    						WHEN ae.admin_emp_is_active = False THEN 'False'
    						ELSE ''
    					END AS admin_emp_is_active
                          FROM admin_employees ae
    					INNER JOIN admin_positions ap ON ap.admin_pos_id = ae.admin_pos_id
                        INNER JOIN designations design ON design.designation_id = ap.admin_designation_id
                        INNER JOIN employees emp ON emp.emp_id = ae.emp_id
                        INNER JOIN persons per ON per.person_id = emp.person_id
    					INNER JOIN units un ON un.unit_id = ap.admin_pos_unit_id
                         WHERE ap.admin_pos_unit_id IN %s
                          AND admin_emp_is_active = %s
                          AND admin_emp_delete_ind = %s
                    '''
            values = (listofallowedunits, True, False)

            columns = ['admin_emp_id', 'emp_number', 'admin_pos_name', 'unit_name', 'person_last_name', 'person_first_name',
                       'admin_emp_is_active']
            df = securequerydatafromdatabase(sqlcommand, values, columns)

            df.columns = ["Admin Employee ID", "Employee Number", "Admin Position", "Unit", "Last Name", "First Name",
                          "Active?"]
            columns = [{"name": i, "id": i} for i in df.columns]
            data = df.to_dict("rows")
            linkcolumn = {}
            editcolumn = {}
            for index, row in df.iterrows():
                editcolumn[index] = dcc.Link(
                    'Edit', href='/settings/settings_admin_emp_assignment_profile?admin_emp_id='+str(row["Admin Employee ID"])+'&mode=edit')
            # for index, row in df.iterrows():
            #     linkcolumn[index] = dbc.Checklist(options=[{"label": "", "value": 1}], value=[])
            data_dict = df.to_dict()
            dictionarydata = {'Edit': editcolumn}
            # dictionarydata2 = {'Delete': linkcolumn}
            data_dict.update(dictionarydata)
            # data_dict.update(dictionarydata2)
            df = pd.DataFrame.from_dict(data_dict)
            table = dbc.Table.from_dataframe(df,
                                             striped=True,
                                             bordered=True,
                                             hover=True,
                                             style={'text-align': 'center'})
            return [table, False, "", "", "", "", ""]
        else:
            raise PreventUpdate
    else:

        sqlcommand = '''
                    SELECT ae.admin_emp_id, emp.emp_number, design.designation_name, un.unit_name,  per.person_last_name, per.person_first_name,
					CASE
						WHEN ae.admin_emp_is_active = True THEN 'True'
						WHEN ae.admin_emp_is_active = False THEN 'False'
						ELSE ''
					END AS admin_emp_is_active
                      FROM admin_employees ae
					INNER JOIN admin_positions ap ON ap.admin_pos_id = ae.admin_pos_id
                    INNER JOIN designations design ON design.designation_id = ap.admin_designation_id
                    INNER JOIN employees emp ON emp.emp_id = ae.emp_id
                    INNER JOIN persons per ON per.person_id = emp.person_id
					INNER JOIN units un ON un.unit_id = ap.admin_pos_unit_id
                     WHERE ap.admin_pos_unit_id IN %s
                      AND admin_emp_is_active = %s
                      AND admin_emp_delete_ind = %s
                '''
        values = (listofallowedunits, True, False)
        columns = ['admin_emp_id', 'emp_number', 'admin_pos_name', 'unit_name',
                   'person_last_name', 'person_first_name', 'admin_emp_delete_ind']
        df = securequerydatafromdatabase(sqlcommand, values, columns)

        df.columns = ["Admin Employee ID", "Employee Number", "Admin Position", "Unit", "Last Name", "First Name",
                      "Active?"]
        columns = [{"name": i, "id": i} for i in df.columns]
        data = df.to_dict("rows")

        linkcolumn = {}
        editcolumn = {}
        for index, row in df.iterrows():
            editcolumn[index] = dcc.Link(
                'Edit', href='/settings/settings_admin_emp_assignment_profile?admin_emp_id='+str(row["Admin Employee ID"])+'&mode=edit')
        # for index, row in df.iterrows():
        #     linkcolumn[index] = dbc.Checklist(options=[{"label": "", "value": 1}], value=[])
        data_dict = df.to_dict()
        dictionarydata = {'Edit': editcolumn}
        # dictionarydata2 = {'Delete': linkcolumn}
        data_dict.update(dictionarydata)
        # data_dict.update(dictionarydata2)
        df = pd.DataFrame.from_dict(data_dict)
        table = dbc.Table.from_dataframe(df,
                                         striped=True,
                                         bordered=True,
                                         hover=True,
                                         style={'text-align': 'center'})
        return [table, False, "", "", "", "", ""]


@app.callback(
    [
        Output('admin_emp_pos_dd', 'options')
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('url', 'search'),
        State('sessioncurrentunit', 'data'),
        State('sessionlistofunits', 'data'),
    ],)
def admin_emp_fillindropdowns(path, url, sessioncurrentunit, sessionlistofunits):
    parsed = urlparse.urlparse(url)
    listofallowedunits = tuple(sessionlistofunits[str(sessioncurrentunit)])
    if path == "/settings/settings_admin_emp_assignment":
        #mode = str(parse_qs(parsed.query)['mode'][0])
        # if mode == "edit":
        #     admin_pos_load_data = 1
        # else:
        #     admin_pos_load_data = 2
        positions = commonmodules.queryfordropdown('''
            SELECT designation_name || ' - ' || un.unit_name AS admin_pos_name, admin_pos_id
              FROM admin_positions ap
            INNER JOIN units un ON un.unit_id = ap.admin_pos_unit_id
			INNER JOIN designations design ON design.designation_id = ap.admin_designation_id
             WHERE admin_pos_delete_ind = %s
               AND admin_pos_unit_id IN %s
            ORDER BY admin_pos_name
        ''', (False, listofallowedunits,))

        return [positions]
    else:
        raise PreventUpdate
