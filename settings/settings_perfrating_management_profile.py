import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from apps import commonmodules
import dash_bootstrap_components as dbc
from app import app
from dash.exceptions import PreventUpdate
from datetime import datetime
import dash_table
import urllib.parse as urlparse
from urllib.parse import parse_qs
from datetime import date as date
import dash
from apps.dbconnect import securequerydatafromdatabase, modifydatabase, modifydatabasereturnid,bulkmodifydatabase
import pandas as pd
layout = html.Div([

    commonmodules.get_header(),
    commonmodules.get_menu(),
    commonmodules.get_common_variables(),
    dcc.Store(id='sr_sessionentitlement', storage_type='memory', data=[]),
    dcc.Store(id='sr_sessionentitlementprocessed', storage_type='memory', data=[]),
    dcc.Store(id='sr_sessionentitlementcid', storage_type='memory', data=[]),
    dcc.Store(id='sr_rows_to_edit', storage_type='memory', data=[]),
    dcc.Store(id='sr_edit_row_status', storage_type='memory', data=[]),
    html.H1("Performance Rating Management"),
    dcc.Link('← Back to Employee', href='/settings/settings_perfrating_query', id="perfrating_mgt_back_link"),
    html.Br(),
    #dcc.Link('← Back to Basic Papers Main', href='/servicerecord/query_faculty', id="sr_mgt_back_link_bp"),
    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Performance Rating Details"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([

                # dbc.Row([
                #     dbc.Col([
                #         html.P("Select Employee:*", style={"fontWeight":"bold"}, className="labelbold")
                #     ], width=4),
                #     dbc.Col([
                #         dcc.Dropdown(
                #             id="sr_mgt_select_emp",
                #             options=[
                #                 {"label":"Faculty", "value":"1"},
                #                 {"label":"Administrative Personnel", "value":"2"},
                #                 {"label":"REPS", "value":"3"},
                #
                #             ],
                #             value="",
                #             searchable = True,
                #             clearable = True
                #         )
                #     ], width=8)
                #
                # ]),
                html.Hr(),

                dbc.Row([
                    dbc.Col([
                        html.H5("Personal Information",style={'color':'rgb(128,0,0)', "font-weight":"bold"})
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
                        dbc.Label(id="perfrating_query_faculty_lname_srmanagemnt", style={"text-align":"left",'color':'black', 'font-weight':'bold'})
                    ], width=9),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("First Name", style={"text-align": "left"}),
                    ], width=3),
                    dbc.Col([
                        dbc.Label(id="perfrating_query_faculty_fname_srmanagemnt", style={"text-align":"left",'color':'black', 'font-weight':'bold'})
                    ], width=9),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Middle Name", style={"text-align": "left"}),
                    ], width=3),
                    dbc.Col([
                        dbc.Label(id="perfrating_query_faculty_mname_srmanagemnt", style={"text-align":"left",'color':'black', 'font-weight':'bold'})
                    ], width=9),
                ]),
                # dbc.Row([
                #     dbc.Col([
                #         dbc.Label("Birthday", style={"text-align": "left"}),
                #     ], width=3),
                #     dbc.Col([
                #         dbc.Label(id="query_faculty_bday_srmanagemnt", style={"text-align":"left",'color':'black', 'font-weight':'bold'})
                #     ], width=9),
                # ]),
                # dbc.Row([
                #     dbc.Col([
                #         dbc.Label("Place of Birth", style={"text-align": "left"}),
                #     ], width=3),
                #     dbc.Col([
                #         dbc.Label(id="query_faculty_placeofbirth_srmanagemnt", style={"text-align":"left",'color':'black', 'font-weight':'bold'})
                #     ], width=9),
                # ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Employee Number", style={"text-align": "left"}),
                    ], width=3),
                    dbc.Col([
                        dbc.Label(id="perfrating_query_faculty_enum_srmanagemnt", style={"text-align":"left",'color':'black', 'font-weight':'bold'})
                    ], width=9),
                ]),
                # html.Div([
                #     dbc.Row([
                #         dbc.Col([
                #             dbc.Label("Main Unit:", style={"text-align": "left"}),
                #         ], width=3),
                #         dbc.Col([
                #             dbc.Label(id="perfrating_query_faculty_mainunitnone_srmanagemnt", style={"text-align":"left",'color':'black', 'font-weight':'bold'})
                #         ], width=9),
                #     ]),
                # ], style={"display":"none"}),
                # html.Div([
                #     dbc.Row([
                #         dbc.Col([
                #             dbc.Label("Primary Designation:", style={"text-align": "left"}),
                #         ], width=3),
                #         dbc.Col([
                #             dbc.Label(id="perfrating_query_faculty_primdesignone_srmanagemnt", style={"text-align":"left",'color':'black', 'font-weight':'bold'})
                #         ], width=9),
                #     ]),
                # ], style={"display":"none"}),

                dbc.Row([
                    dbc.Col([
                        dbc.Label("Employee is Active:", style={"text-align": "left"}),
                    ], width=3),
                    dbc.Col([
                        dbc.Label(id="perfrating_query_status_srmanagemnt", style={"text-align":"left",'color':'black', 'font-weight':'bold'})
                    ], width=9),
                ]),

                html.Br(),
                html.Hr(),
                dbc.Row([
                    dbc.Col([
                        html.H5("Performance Rating Entry Information",style={'color':'rgb(128,0,0)', "font-weight":"bold"})
                    ]),
                    dbc.Col([
                    ]),
                ]),
                html.Br(),
                # dbc.Row([
                #     dbc.Col([
                #         dbc.Spinner([
                #         dbc.FormGroup([
                #                 dbc.Label("Primary Appointment?*", width=3, style={"text-align":"left",'color':'black', 'font-weight':'normal'}),
                #
                #                 dbc.Col([
                #                     dbc.Row([
                #                         dbc.Col([
                #                             dbc.Checklist(
                #                                 options=[
                #                                     {"label": "Primary", "value": 1},
                #
                #                                 ],
                #                                 value=[1],
                #                                 id="sr_mgt_is_primary",
                #                                 switch=True,
                #                             ),
                #
                #                         ],width=4),
                #                         dbc.Col([
                #                             html.Div([
                #                                 dbc.Checklist(
                #                                     options=[
                #                                         {"label": "Update Main Employee Details?", "value": 1},
                #
                #                                     ],
                #                                     value=[],
                #                                     id="sr_mgt_update_emp",
                #                                     switch=True,
                #                                 ),
                #                             ],id="sr_mgt_update_emp_div",)
                #                         ],width=4),
                #                         dbc.Col([
                #                             html.Div([
                #                                 dbc.Checklist(
                #                                     options=[
                #                                         {"label": "Set employee to be active", "value": 1},
                #
                #                                     ],
                #                                     value=[1],
                #                                     id="sr_mgt_is_active",
                #                                     switch=True,
                #                                 ),
                #                             ],id="sr_mgt_update_emp_div",)
                #                         ],width=4),
                #                     ]),
                #
                #
                #
                #                 ],width=9)
                #             ],row=True),
                #         ]),
                #     ]),
                # ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Spinner([
                        dbc.FormGroup(
                            [dbc.Label("Performance Rating", width=2, style={"text-align":"left"}),
                            dbc.Col([
                                dbc.Input(
                                    type="text", id="perf_rating", placeholder="Enter Performance Rating"
                                ),
                                dbc.FormFeedback("Too short or already taken", valid = False)
                            ],
                            width=8
                            )],
                            row = True
                        ),
                        ]),
                    ]),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Spinner([
                        dbc.FormGroup(
                            [dbc.Label("Adjectival Rating", width=2, style={"text-align":"left"}),
                            dbc.Col([
                                dbc.Label(id="adjectival_rating"),
                                dbc.FormText("If no adjectival rating appears, please assign an employee class to the designation through the Designations Module.")

                            ],
                            width=8
                            )],
                            row = True
                        ),
                        ]),
                    ]),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Spinner([
                        dbc.FormGroup(
                            [dbc.Label("Start Period", width=2, style={"text-align":"left"}),
                            dbc.Col([
                                dcc.DatePickerSingle(id='perf_rating_start_period', placeholder="mm/dd/yyyy"),
                                dbc.FormFeedback("Please enter start date.", valid = False)
                            ],width=8)
                            # dbc.Col([
                            #     dbc.Input(
                            #         type="text", id="perf_rating_start_period", placeholder="Enter start period"
                            #     ),
                            #     dbc.FormFeedback("Too short or already taken", valid = False)
                            # ],
                            # width=8
                            # )

                            ],
                            row = True
                        ),
                        ]),
                    ]),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup(
                            [dbc.Label("End Period", width=2, style={"text-align":"left"}),
                            dbc.Col([
                                dcc.DatePickerSingle(id='perf_rating_end_period', placeholder="mm/dd/yyyy"),

                                dbc.FormFeedback("Please enter end date.", valid = False)
                            ],width=8)
                            ],
                            row = True
                        ),
                    ]),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup(
                            [dbc.Label("Unit:", width=2, style={"text-align":"left"}),
                            dbc.Col([
                                dcc.Dropdown(id='perfrating_query_main_unit_srmanagemnt',
                                    options = [],
                                    #value="",
                                    searchable=True,
                                    clearable=True),

                                #dbc.FormFeedback("Please enter end date.", valid = False)
                            ],width=8)
                            ],
                            row = True
                        ),
                    ]),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup(
                            [dbc.Label("Designation:", width=2, style={"text-align":"left"}),
                            dbc.Col([
                                dcc.Dropdown(id='perfrating_query_designation_srmanagemnt',
                                    options = [],
                                    #value="",
                                    searchable=True,
                                    clearable=True),

                                #dbc.FormFeedback("Please enter end date.", valid = False)
                            ],width=8)
                            ],
                            row = True
                        ),
                    ]),
                ]),
                # dbc.Row([
                #     dbc.Col([
                #         dbc.Label("Main Unit:", style={"text-align": "left"}),
                #     ], width=3),
                #     dbc.Col([
                #         dbc.Label(id="perfrating_query_main_unit_srmanagemnt", style={"text-align":"left",'color':'black', 'font-weight':'bold'})
                #     ], width=9),
                # ]),
                # dbc.Row([
                #     dbc.Col([
                #         dbc.Label("Primary Designation:", style={"text-align": "left"}),
                #     ], width=3),
                #     dbc.Col([
                #         dbc.Label(id="perfrating_query_designation_srmanagemnt", style={"text-align":"left",'color':'black', 'font-weight':'bold'})
                #     ], width=9),
                # ]),
                # dbc.Row([
                #     dbc.Col([
                #         dbc.Spinner([
                #         dbc.FormGroup([
                #                 dbc.Label("Proposed Designation*", width=3, style={"text-align":"left",'color':'black', 'font-weight':'normal'},id="sr_mgt_select_desig_label"),
                #
                #                 dbc.Col([
                #                     dcc.Dropdown( #autofilled, same with previous designation
                #                         id='sr_mgt_select_desig',
                #                         placeholder="Please select position for appointment",
                #                     ),
                #                     dbc.FormFeedback("Please select position", valid = False)
                #                 ],width=9)
                #             ],row=True),
                #
                #         ]),
                #     ]),
                #
                #
                # ]),
                # dbc.Row([
                #     dbc.Col([
                #         dbc.FormGroup([
                #                 dbc.Label("Status*", width=3, style={"text-align":"left",'color':'black', 'font-weight':'normal'}, id='sr_mgt_select_status_label'),
                #                 dbc.Col([
                #                     dcc.Dropdown( #autofilled, same with previous designation
                #                         id='sr_mgt_select_status',
                #                         options=[
                #                             {"label":"Part Time", "value":"1"},
                #                             {"label":"Full Time", "value":"2"},
                #                             {"label":"Contractual", "value":"3"},
                #                             {"label":"Substitute", "value":"4"},
                #                             {"label":"Temporary", "value":"5"},
                #                             {"label":"Permanent", "value":"6"},
                #                         ],
                #
                #                         placeholder="Please select status",
                #                     ),
                #                     dbc.FormFeedback("Please enter salary grade of appointment.", valid = False)
                #                 ],width=9)
                #             ],row=True),
                #     ]),
                # ]),
                # dbc.Row([
                #     dbc.Col([
                #         dbc.FormGroup([
                #                 dbc.Label("Start Date*", width=3, style={"text-align":"left",'color':'black', 'font-weight':'normal'}, id='sr_mgt_start_date_label'),
                #                 dbc.Col([
                #                     dbc.Row([
                #                         dbc.Col([
                #                             dcc.DatePickerSingle(id='sr_mgt_start_date', placeholder="mm/dd/yyyy",date=date.today(), display_format='MMM DD, YYYY'
                #                                                  ),
                #                             dbc.FormFeedback("Please enter start date.", valid = False),
                #                         ], width=3),
                #                         dbc.Col([
                #                             dbc.Checklist(
                #                                 options=[
                #                                     {"label": "With End Date", "value": 1},
                #
                #                                 ],
                #                                 value=[1],
                #                                 id="sr_mgt_end_date_chk",
                #                                 switch=True,
                #                             ),
                #                         ], width=3),
                #                         dbc.Col([
                #
                #                         ], width=6),
                #                     ]),
                #
                #
                #
                #                 ],width=9)
                #             ],row=True),
                #     ]),
                # ]),


                dbc.Row([
                    dbc.Col([

                        dbc.FormGroup([
                                dbc.Label("Delete Performance Rating Entry?*", width=3, style={"text-align":"left",'color':'black', 'font-weight':'normal'}),

                                dbc.Col([
                                    dbc.Checklist(
                                        options=[
                                            {"label": "", "value": 1},

                                        ],
                                        value=[],
                                        id="perfrating_mgt_delete_ind",
                                        switch=True,
                                    ),

                                ],width=9)
                            ],row=True),

                    ]),

                ], id="perfrating_div_sr_mgt_delete_ind"),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Save Performance Rating Entry", color="primary", className="mr-1",
                                   id="perfrating_btn_save_sr_entry"),
                    ]),
                    dbc.Col([
                        dbc.Button("Cancel", color="primary", className="mr-1",
                                   id="perfrating_btn_cancel_sr_entitlements"),
                    ]),
                    dbc.Col([
                    ]),
                ]),
                # html.Div([
                #     dcc.Input(id='sr_eligibilities_summary', type='text', value="0")
                # ], style={'display': 'none'}),
                html.Div([
                    dcc.Input(id='perfrating_submit_summary', type='text', value="0")
                ], style={'display': 'none'}),
                html.Div([
                    dcc.Input(id='perfrating_load_sr', type='text', value="0")
                ], style={'display': 'none'}),
                dbc.Modal(
                    [
                        dbc.ModalHeader(
                            "Performance Rating Entry"),
                        dbc.ModalBody(
                            "Successfully modified performance rating"),
                        dbc.ModalFooter(
                            [
                            # html.Div([
                            #     dbc.Button("Close and Add New Entry", id="perfrating_result_return_close", className="ml-auto"),
                            # ], id="perfrating_div_close_add_entry"),

                            dbc.Button("Return to Employee Performance Ratings", id="perfrating_result_return_menu", className="ml-auto"
                            ),
                            ]
                        ),
                    ],
                    id="perfrating_result_modal",
                    centered=True,
                    backdrop='static',
                    size="lg"
                ),
                dbc.Modal(
                    [
                        dbc.ModalHeader(
                            "Performance Rating Entry Message"),
                        dbc.ModalBody(
                            [html.Div("Please check required fields and complete entry.", id="perfrating_result_modal_message_body")],),
                        dbc.ModalFooter(
                            [

                            dbc.Button("Close", id="perfrating_result_modal_message_btn", className="ml-auto"
                            ),
                            ]
                        ),
                    ],
                    id="perfrating_result_modal_message",
                    centered=True,
                    backdrop='static',
                    size="lg"
                ),
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])

# @app.callback(
#     Output("collapse", "is_open"),
#     [Input("collapse-button", "n_clicks")],
#     [State("collapse", "is_open")],
# )
# def toggle_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open

@app.callback([
    Output('perfrating_div_sr_mgt_delete_ind','style'),
    #Output('perfrating_div_close_add_entry','style'),
    #Output('collapse-button-div','style'),
    #Output('sr_mgt_update_emp_div','style'),
    #Output('sr_mgt_update_emp','value'),
],
    [
    Input('url', 'pathname'),
],
    [
    State('url', 'search'),
],)
def delete_ind_div(path,url ):
    if path=="/settings/settings_perfrating_management_profile":
        parsed = urlparse.urlparse(url)
        mode = str(parse_qs(parsed.query)['mode'][0])
        if mode == "add":
            style={'display': 'none'}
            #div_close_add_entry={'display': 'inline'}
            #sr_mgt_update_emp_div={'display': 'inline'}
            #sr_mgt_update_emp_div_val =[1]
        # elif mode == "convert":
        #     style={'display': 'none'}
        #     div_close_add_entry={'display': 'none'}
        #     # sr_mgt_update_emp_div={'display': 'inline'}
        #     # sr_mgt_update_emp_div_val =[]
        else:
            style={'display': 'inline'}
            #div_close_add_entry={'display': 'none'}
            # sr_mgt_update_emp_div={'display': 'inline'}
            # sr_mgt_update_emp_div_val =[]
        return [style]
    else:
        raise PreventUpdate


@app.callback([
    #Output('sr_mgt_select_emp', 'options'),
    # Output('sr_mgt_select_desig', 'options'),
    # Output('sr_mgt_select_unit', 'options'),
    # Output('sr_mgt_select_sg', 'options'),
    # Output('sr_entitlement', 'options'),
    # Output('sr_entitlementtype', 'options'),
    # Output('sr_mgt_psi', 'options'),
    Output('perfrating_mgt_back_link', 'href'),
    Output('perfrating_btn_cancel_sr_entitlements', 'href'),
    Output('perfrating_result_return_menu', 'href'),
    Output('perfrating_load_sr','value'),
    # Output('sr_mgt_select_appt_type', 'options'),
    # Output('sr_mgt_back_link_bp', 'href'),
    # Output('sr_mgt_emp_class', 'options'),
    # Output('sr_mgt_select_status', 'options'),
    # Output('sr_mgt_select_sg_type', 'options'),
],
    [
    Input('url', 'pathname'),
],
    [
    State('url', 'search'),


],)
def fillindropdowns(path,url ):
    parsed = urlparse.urlparse(url)
    #print("listofunits",sessionlistofunits)
    #print("sessioncurrentunit",sessioncurrentunit)
    if path=="/settings/settings_perfrating_management_profile":
        eid = str(parse_qs(parsed.query)['eid'][0])
        mode = str(parse_qs(parsed.query)['mode'][0])
        if mode == "add":
            perfrating_load_sr = 1
        else:
            perfrating_load_sr = 2
        # designationoptions = commonmodules.queryfordropdown('''
        #     SELECT designation_name as label, designation_id as value
        #    FROM designations
        #    WHERE designation_delete_ind = %s
        #    ORDER BY designation_name
        # ''', (False,))
        #
        # listofunits = commonmodules.queryfordropdown('''
        #     SELECT CONCAT(unit_name,' (', unit_code, ') ') as label, unit_id as value
        #    FROM units
        #    WHERE unit_delete_ind = %s
        #    ORDER BY unit_name
        # ''', (False, ))
        #
        # salarygrades = commonmodules.queryfordropdown('''
        #     SELECT sg_number_step as label, sg_number_step_id as value
        #    FROM sg_number_steps
        #    WHERE sg_number_delete_ind = %s
        #    ORDER BY sg_number_step
        # ''', (False, ))
        #
        # plantilla_items = commonmodules.queryfordropdown('''
        #     SELECT plantilla_number as label, plantilla_id as value
        #    FROM plantilla_items
        #    WHERE plantilla_delete_ind = %s
        #    ORDER BY plantilla_number
        # ''', (False,))
        #
        # obpentitlement = commonmodules.queryfordropdown('''
        #     SELECT entitle_name as label,  entitle_id as value
        #    FROM entitlements
        #    WHERE entitle_delete_ind = %s
        #    AND entitle_name NOT IN ('For NULL mapping')
        #    ORDER BY entitle_name
        # ''', (False,))
        #
        # obpentitlementtype = commonmodules.queryfordropdown('''
        #     SELECT entitle_type_name as label, entitle_type_id as value
        #    FROM entitlement_types
        #    WHERE entitle_type_delete_ind = %s
        #    ORDER BY entitle_type_name
        # ''', (False,))
        #
        # appttypes = commonmodules.queryfordropdown('''
        #     SELECT appt_type_name as label, appt_type_id as value
        #    FROM appointment_types
        #    WHERE appt_type_delete_ind = %s
        #    ORDER BY appt_type_name
        # ''', (False,))
        #
        # emp_classes = commonmodules.queryfordropdown('''
        #     SELECT emp_class_name as label, emp_class_id as value
        #    FROM emp_classes
        #    WHERE emp_class_delete_ind = %s
        #    ORDER BY emp_class_name
        # ''', (False,))
        #
        # emp_statuses = commonmodules.queryfordropdown('''
        #     SELECT emp_status_desc as label, emp_status_id as value
        #    FROM emp_statuses
        #    WHERE emp_status_delete_ind = %s
        #    ORDER BY emp_status_name
        # ''', (False,))

        href_bp ="/settings/settings_perfrating_management"

        href ="/settings/settings_perfrating_query_profile?mode=view&eid="+str(eid)
        # sgobpentitlementtype = commonmodules.queryfordropdown('''
        #     SELECT entitle_type_name as label, entitle_type_id as value
        #    FROM entitlement_types
        #    WHERE entitle_type_delete_ind = %s and entitle_type_id in %s
        #    ORDER BY entitle_type_name
        # ''', (False,(6,16)))

        return [href, href, href, perfrating_load_sr]
    else:
        raise PreventUpdate

# @app.callback([
#     Output('sr_mgt_end_date_div', 'style'),
# ],
#     [
#     Input('sr_mgt_end_date_chk', 'value'),
# ],
#     [
#
# ],)
# def toggle_end_date_div(sr_mgt_end_date_chk ):
#     if 1 in sr_mgt_end_date_chk:
#         return [{'display':'inline'}]
#     else:
#         return [{'display':'none'}]



@app.callback(
    [
        Output("perfrating_query_faculty_fname_srmanagemnt", "children"),
        Output("perfrating_query_faculty_mname_srmanagemnt", "children"),
        Output("perfrating_query_faculty_lname_srmanagemnt", "children"),
        # Output("query_faculty_bday_srmanagemnt", "children"),
        # Output("query_faculty_placeofbirth_srmanagemnt", "children"),
        Output("perfrating_query_faculty_enum_srmanagemnt", "children"),
        # Output("perfrating_query_faculty_mainunitnone_srmanagemnt", "children"),
        # Output("perfrating_query_faculty_primdesignone_srmanagemnt", "children"),
        Output("perfrating_query_status_srmanagemnt", "children"),
        #Output('perfrating_query_main_unit_srmanagemnt', 'value')
    ],
    [
        Input("url", "search"),
    ],
        [
            State("url", "pathname"),
        ],
)
def updatefacultyprofile(url, pathname):
    parsed = urlparse.urlparse(url)
    if parsed.query and pathname =="/settings/settings_perfrating_management_profile":
        empid = str(parse_qs(parsed.query)['eid'][0])

        sqlcommand = '''SELECT person_first_name, person_middle_name, person_last_name, emp_is_active, emp_number

        FROM persons p INNER JOIN employees e on e.person_id = p.person_id

        WHERE e.emp_id = %s and e.emp_delete_ind = %s'''
        values = (empid, False)
        columns = ['person_first_name', 'person_middle_name',
                   'person_last_name', 'emp_is_active','emp_number']
        df = securequerydatafromdatabase(sqlcommand, values, columns)
        person_first_name = df["person_first_name"][0]
        person_middle_name = df["person_middle_name"][0]
        person_last_name = df["person_last_name"][0]
        # person_dob = df["person_dob"][0]
        # person_pob = df["person_pob"][0]
        # designation_name =  df["designation_name"][0]
        # unit_name=  df["unit_name"][0]
        # unit_id=  df["unit_id"][0]
        emp_number = df["emp_number"][0]
        # print(unit_name, 'unit_name')
        # print(designation_name, 'designation_name')
        # print(unit_id, 'unit_id')
        #print(df["emp_is_active"][0])
        if df["emp_is_active"][0]:
            emp_is_active=  "Active"
        else:
            emp_is_active=  "Inactive"
        return [person_first_name, person_middle_name, person_last_name, emp_number, emp_is_active]
    else:
        raise PreventUpdate




# @app.callback(
#     [Output("modal_sr_select_entitlement", "is_open"),
#      Output('current_sr_entitlements', 'children'),
#      Output('sr_sessionentitlement', 'data'),
#      Output('sr_sessionentitlementprocessed', 'data'),
#     #
#     Output("sr_eligibilities_summary", "value"),
#     Output('sr_sessionentitlementcid','data'),
#     Output('sr_rows_to_edit','data'),
#     Output('sr_model_header','children'),
#     Output('sr_edit_row_status','data'),
#      ],
#     [Input("btn_add_sr_entitlements", "n_clicks"),
#
#      Input("modal_sr_entitlement_save", "n_clicks"),
#      Input("modal_sr_entitlement_cancel", "n_clicks"),
#     Input("btn_delete_sr_entitlements", "n_clicks"),
#     Input('sr_load_sr','value'),
#     Input('btn_edit_sr_entitlement',"n_clicks")
#      ],
#     [
#     State("sr_entitlement", "value"),
#     State("sr_entitlementtype", "value"),
#     State("sr_entitlementvalue", "value"),
#     State("sr_entitlementtext", "value"),
#     State("sr_entitlement", "options"),
#     State("sr_entitlementtype", "options"),
#     State('sr_sessionentitlement', 'data'),
#     State('sr_sessionentitlementprocessed', 'data'),
#     State('current_sr_entitlements', 'children'),
#
#     #
#     State('sr_sessionentitlementcid','data'),
#     #
#     State('url', 'search'),
#     State('current_user_id', 'data'),
#     State('sr_rows_to_edit','data'),
#     State('sr_model_header','children'),
#     State('sr_edit_row_status','data'),
#
#
#      ],
# )
# def toggle_modal_entitlements(btn_add_entitlements,modal_bp_entitlement_save,modal_bp_entitlement_cancel,btn_delete_sr_entitlements,sr_load_sr,btn_edit_sr_entitlement,
#     sr_entitlement, sr_entitlementtype, sr_entitlementvalue, sr_entitlementtext, sr_entitlement_ops, sr_entitlementtype_ops,
#     sr_sessionentitlement, sr_sessionentitlementprocessed, table, sr_sessionentitlementcid,url,current_user_id,sr_rows_to_edit,sr_model_header,sr_edit_row_status
#     ):
#
#     ctx = dash.callback_context
#     if ctx.triggered:
#         eventid = ctx.triggered[0]['prop_id'].split('.')[0]
#         #print(eventid)
#         if eventid=="btn_add_sr_entitlements":
#             sr_model_header = "Add Entitlement"
#             modal_sr_select_entitlement = True
#             sr_edit_row_status = 1
#             return [modal_sr_select_entitlement, table, sr_sessionentitlement, sr_sessionentitlementprocessed,1, sr_sessionentitlementcid,sr_rows_to_edit,sr_model_header,sr_edit_row_status] #, table,sessionentitlement, sessionentitlementprocessed,sessionentitlementcid, 0 ]
#         if eventid=="modal_sr_entitlement_save":
#
#             if sr_entitlement and sr_entitlementtype and (float(sr_entitlementvalue)>=0):
#                 if sr_edit_row_status==1:
#                     entitlement = [(i, d) for i, d in enumerate(sr_entitlement_ops) if sr_entitlement in d.values()]
#                     if entitlement:
#                         entitlement = entitlement[0][1]['label']
#                     entitlementtype = [(i, d) for i, d in enumerate(sr_entitlementtype_ops) if sr_entitlementtype in d.values()]
#                     if entitlementtype:
#                         entitlementtype = entitlementtype[0][1]['label']
#                     new_row = {'Entitlement': entitlement, 'Type of Entitlement': entitlementtype, 'Value': sr_entitlementvalue, 'Remarks': sr_entitlementtext}
#                     sr_sessionentitlementprocessed.append(new_row)
#                     new_row_raw =  {'Entitlement': sr_entitlement, 'Type of Entitlement': sr_entitlementtype, 'Value': sr_entitlementvalue, 'Remarks': sr_entitlementtext}
#                     sr_sessionentitlement.append(new_row_raw)
#                     parsed = urlparse.urlparse(url)
#                     mode = str(parse_qs(parsed.query)['mode'][0])
#                     if mode == "edit":
#                         srid = str(parse_qs(parsed.query)['srid'][0])
#                         insert_sr_entitlements([new_row_raw], current_user_id, srid)
#
#                 else:
#                     # print(sr_sessionentitlementcid)
#                     # print(sr_rows_to_edit)
#                     parsed = urlparse.urlparse(url)
#                     srid = str(parse_qs(parsed.query)['srid'][0])
#                     entitlement = [(i, d) for i, d in enumerate(sr_entitlement_ops) if sr_entitlement in d.values()]
#                     if entitlement:
#                         entitlement = entitlement[0][1]['label']
#                     entitlementtype = [(i, d) for i, d in enumerate(sr_entitlementtype_ops) if sr_entitlementtype in d.values()]
#                     if entitlementtype:
#                         entitlementtype = entitlementtype[0][1]['label']
#                     sr_rows_to_edit_value = sr_rows_to_edit[0]
#                     sr_entitle_id=sr_sessionentitlementcid[sr_rows_to_edit_value]
#                     sr_sessionentitlement[sr_rows_to_edit_value]['Entitlement'] = sr_entitlement
#                     sr_sessionentitlement[sr_rows_to_edit_value]['Type of Entitlement'] = sr_entitlementtype
#                     sr_sessionentitlement[sr_rows_to_edit_value]['Value'] = sr_entitlementvalue
#                     sr_sessionentitlement[sr_rows_to_edit_value]['Remarks'] = sr_entitlementtext
#
#                     sr_sessionentitlementprocessed[sr_rows_to_edit_value]['Entitlement'] = entitlement
#                     sr_sessionentitlementprocessed[sr_rows_to_edit_value]['Type of Entitlement'] = entitlementtype
#                     sr_sessionentitlementprocessed[sr_rows_to_edit_value]['Value'] = sr_entitlementvalue
#                     sr_sessionentitlementprocessed[sr_rows_to_edit_value]['Remarks'] = sr_entitlementtext
#
#                     sqlbpfields = """
#                         UPDATE sr_entitlements SET  entitle_id=%s, entitle_type_id=%s, sr_entitle_amount=%s, sr_entitle_remarks=%s
#                         WHERE sr_entitle_id=%s
#                     """
#                     entitlevalues = [sr_entitlement, sr_entitlementtype, sr_entitlementvalue, sr_entitlementtext, sr_entitle_id]
#                 #    print(entitlevalues)
#                     modifydatabase(sqlbpfields, entitlevalues)
#                     # print(sr_sessionentitlement[sr_rows_to_edit_value])
#                     # print(sr_sessionentitlementprocessed[sr_rows_to_edit_value])
#                 #
#                 mode = str(parse_qs(parsed.query)['mode'][0])
#                 if mode=='edit':
#                     sql = ''' SELECT sr_entitle_id
#                     FROM sr_entitlements
#                     WHERE sr_id = %s  AND sr_entitle_delete_ind=%s'''
#                     values = (srid, False)
#                     columns = ['sr_entitle_id']
#                     df = securequerydatafromdatabase(sql, values, columns)
#                     sr_sessionentitlementcid = df['sr_entitle_id'].to_list()
#                 df = pd.DataFrame.from_dict(sr_sessionentitlementprocessed, orient='columns')
#                 if len(sr_sessionentitlementprocessed) > 0:
#                     df = addcheckboxtocolumn(df)
#                 table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
#             modal_sr_select_entitlement = False
#             return [modal_sr_select_entitlement, table, sr_sessionentitlement, sr_sessionentitlementprocessed,1,sr_sessionentitlementcid,sr_rows_to_edit,sr_model_header,sr_edit_row_status]
#         elif eventid=="modal_sr_entitlement_cancel":
#             modal_sr_select_entitlement = False
#             sr_edit_row_status=0
#             return [modal_sr_select_entitlement, table, sr_sessionentitlement, sr_sessionentitlementprocessed,1,sr_sessionentitlementcid, sr_rows_to_edit,sr_model_header,sr_edit_row_status]
#
#
#         elif eventid =="btn_edit_sr_entitlement":
#             rowstodelete = returnselectedrows(table, 5)
#             sr_model_header = "Edit Selected Entitlement"
#             if len(rowstodelete)==1:
#                 print(rowstodelete)
#                 modal_sr_select_entitlement = True
#                 sr_rows_to_edit =rowstodelete
#                 sr_edit_row_status=2
#                 return [modal_sr_select_entitlement, table,sr_sessionentitlement, sr_sessionentitlementprocessed,3,sr_sessionentitlementcid,sr_rows_to_edit,sr_model_header,sr_edit_row_status ]
#             else:
#                 print("please select 1")
#
#             raise PreventUpdate
#         elif eventid=="btn_delete_sr_entitlements":
#             rowstodelete = returnselectedrows(table, 5)
#             parsed = urlparse.urlparse(url)
#             mode = str(parse_qs(parsed.query)['mode'][0])
#             #
#             print(sr_sessionentitlement)
#             entitlementlist = []
#             for index in range(len(sr_sessionentitlement)):
#                 if index in rowstodelete:
#                     entitlementlist.append(sr_sessionentitlement[index])
#             sr_sessionentitlement =   entitlementlist
#             if mode == "edit":
#                 srid = str(parse_qs(parsed.query)['srid'][0])
#                 for item in entitlementlist:
#                 #    print(item)
#                     sqlbpfields = """
#                         UPDATE sr_entitlements SET  sr_entitle_delete_ind=%s
#                         WHERE sr_id=%s AND entitle_id=%s AND entitle_type_id =%s
#                     """
#                     entitlevalues = [True, srid, item["Entitlement"], item["Type of Entitlement"]]
#                 #    print(entitlevalues)
#                     modifydatabase(sqlbpfields, entitlevalues)
#
#
#             processedlist = []
#             for index in range(len(sr_sessionentitlementprocessed)):
#                 if index not in rowstodelete:
#                     processedlist.append(sr_sessionentitlementprocessed[index])
#             sr_sessionentitlementprocessed = processedlist
#             modal_sr_select_entitlement = False
#             df = pd.DataFrame.from_dict(sr_sessionentitlementprocessed, orient='columns')
#             if len(sr_sessionentitlementprocessed) > 0:
#                 df = addcheckboxtocolumn(df)
#             table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
#
#             return [modal_sr_select_entitlement, table,sr_sessionentitlement, sr_sessionentitlementprocessed,0,sr_sessionentitlementcid,sr_rows_to_edit,sr_model_header,sr_edit_row_status ]
#         elif eventid =='sr_load_sr' and sr_load_sr==2:
#             parsed = urlparse.urlparse(url)
#             mode = str(parse_qs(parsed.query)['mode'][0])
#             modal_sr_select_entitlement = False
#             if mode in ["add","edit"]:
#                 parsed = urlparse.urlparse(url)
#                 srid = str(parse_qs(parsed.query)['srid'][0])
#
#
#
#
#             #
#                 sql = ''' SELECT e.entitle_id, entitle_name, et.entitle_type_id, entitle_type_name,
#                 sr_entitle_amount, sr_entitle_remarks, sr_entitle_id
#         		FROM sr_entitlements sre INNER JOIn entitlements e ON e.entitle_id = sre.entitle_id
#         		INNER JOIN entitlement_types et ON sre.entitle_type_id = et.entitle_type_id
#                 WHERE sr_id = %s AND sr_entitle_delete_ind=%s'''
#                 values = (srid, False)
#                 columns = ['entitle_id', 'entitle_name', 'entitle_type_id', 'entitle_type_name', 'sr_entitle_amount', 'sr_entitle_remarks', 'sr_entitle_id']
#                 df = securequerydatafromdatabase(sql, values, columns)
#
#                 dfsessionentitlements = df[['entitle_id', 'entitle_type_id', 'sr_entitle_amount', 'sr_entitle_remarks']].copy()
#                 dfsessionentitlements.columns =['Entitlement', 'Type of Entitlement', 'Value', 'Remarks']
#                 sr_sessionentitlement = dfsessionentitlements.to_dict('records')
#
#                 sessionentitlementsprocesseddf = df[['entitle_name', 'entitle_type_name', 'sr_entitle_amount', 'sr_entitle_remarks']].copy()
#                 sessionentitlementsprocesseddf.columns = ["Entitlement", "Type of Entitlement", "Value", "Remarks"]
#                 table = sessionentitlementsprocesseddf
#             #
#             #
#                 sr_sessionentitlementprocessed = sessionentitlementsprocesseddf.to_dict('records')
#                 sessionentitlementsprocesseddf = pd.DataFrame.from_dict(
#                     sr_sessionentitlementprocessed, orient='columns')
#                 if len(sessionentitlementsprocesseddf) > 0:
#                     sessionentitlementsprocesseddf = addcheckboxtocolumn(sessionentitlementsprocesseddf)
#                 table = dbc.Table.from_dataframe(
#                     sessionentitlementsprocesseddf, striped=True, bordered=True, hover=True)
#                 sr_sessionentitlementcid = df['sr_entitle_id'].to_list()
#             else:
#                 print("test")
#                 bpid = str(parse_qs(parsed.query)['bpid'][0])
#
#
#                 sql = ''' SELECT e.entitle_id, entitle_name, et.entitle_type_id, entitle_type_name,
#                 bp_entitle_amount, bp_entitle_remarks, bp_entitle_id
#         		FROM bp_entitlements bpe INNER JOIn entitlements e ON e.entitle_id = bpe.entitle_id
#         		INNER JOIN entitlement_types et ON bpe.entitle_type_id = et.entitle_type_id
#                 WHERE bp_id = %s AND bp_entitle_delete_ind=%s'''
#                 values = (bpid, False)
#                 columns = ['entitle_id', 'entitle_name', 'entitle_type_id', 'entitle_type_name', 'bp_entitle_amount', 'bp_entitle_remarks', 'bp_entitle_id']
#                 df = securequerydatafromdatabase(sql, values, columns)
#                 dfsessionentitlements = df[['entitle_id', 'entitle_type_id', 'bp_entitle_amount', 'bp_entitle_remarks']].copy()
#                 dfsessionentitlements.columns =['Entitlement', 'Type of Entitlement', 'Value', 'Remarks']
#                 sr_sessionentitlement = dfsessionentitlements.to_dict('records')
#
#                 sessionentitlementsprocesseddf = df[['entitle_name', 'entitle_type_name', 'bp_entitle_amount', 'bp_entitle_remarks']].copy()
#                 sessionentitlementsprocesseddf.columns = ["Entitlement", "Type of Entitlement", "Value", "Remarks"]
#                 table = sessionentitlementsprocesseddf
#             #
#             #
#                 sr_sessionentitlementprocessed = sessionentitlementsprocesseddf.to_dict('records')
#                 sessionentitlementsprocesseddf = pd.DataFrame.from_dict(
#                     sr_sessionentitlementprocessed, orient='columns')
#                 if len(sessionentitlementsprocesseddf) > 0:
#                     sessionentitlementsprocesseddf = addcheckboxtocolumn(sessionentitlementsprocesseddf)
#                 table = dbc.Table.from_dataframe(
#                     sessionentitlementsprocesseddf, striped=True, bordered=True, hover=True)
#                 sr_sessionentitlementcid = df['entitle_id'].to_list()
#
#
#             return [modal_sr_select_entitlement, table, sr_sessionentitlement, sr_sessionentitlementprocessed,1,sr_sessionentitlementcid,sr_rows_to_edit,sr_model_header,sr_edit_row_status]
#
#         else:
#             raise PreventUpdate
#     else:
#         raise PreventUpdate
#
# def addcheckboxtocolumn(df):
#     linkcolumn = {}
#     for index, row in df.iterrows():
#         linkcolumn[index] = dbc.Checklist(options=[{"label": "", "value": 1}], value=[])
#     data_dict = df.to_dict()
#     dictionarydata = {'Select': linkcolumn}
#     data_dict.update(dictionarydata)
#     df = pd.DataFrame.from_dict(data_dict)
#     return df
#
#
# @app.callback(
#     [
#     Output("sr_entitlement", "value"),
#     Output("sr_entitlementtype", "value"),
#     Output("sr_entitlementvalue", "value"),
#     Output("sr_entitlementtext", "value"),
#     ],
#     [
#         Input("sr_eligibilities_summary", "value")
#     ],
#     [
#     State("sr_entitlement", "value"),
#     State("sr_entitlementtype", "value"),
#     State("sr_entitlementvalue", "value"),
#     State("sr_entitlementtext", "value"),
#     State('sr_sessionentitlement', 'data'),
#     State('sr_rows_to_edit','data'),
#     State('sr_sessionentitlementcid','data'),
#     ],
# )
# def toggle_modal_entitlement_values(sr_eligibilities_summary,
#                                 obpentitlement, obpentitlementtype, obpentitlementvalue, obpentitlementtext, sr_sessionentitlement,sr_rows_to_edit,
#                                 sr_sessionentitlementcid
#                                 ):
#     if sr_eligibilities_summary == 1:
#         obpentitlement = ""
#         obpentitlementtype = ""
#         obpentitlementvalue  = ""
#         obpentitlementtext = ""
#     elif sr_eligibilities_summary == 3:
#
#         obpentitlementtype = 1
#         obpentitlementvalue  = 1
#         obpentitlementtext =1
#         # print('sr_rows_to_edit',sr_rows_to_edit)
#         # print("sr_sessionentitlement",sr_sessionentitlement)
#         # print("sr_sessionentitlementcid",sr_sessionentitlementcid)
#         obpentitlement=sr_sessionentitlement[sr_rows_to_edit[0]]['Entitlement']
#         obpentitlementtype =sr_sessionentitlement[sr_rows_to_edit[0]]['Type of Entitlement']
#         obpentitlementvalue  =sr_sessionentitlement[sr_rows_to_edit[0]]['Value']
#         obpentitlementtext =sr_sessionentitlement[sr_rows_to_edit[0]]['Remarks']
#
#     return [obpentitlement, obpentitlementtype, obpentitlementvalue, obpentitlementtext]
#
# def returnselectedrows(dftable, ncolumns):
#     selectedrows = []
#     if dftable:
#         for i in range(0, len(dftable['props']['children'][1]['props']['children'])):
#             if 1 in dftable['props']['children'][1]['props']['children'][i]['props']['children'][ncolumns-1]['props']['children']['props']['value']:
#                 selectedrows.append(i)
#     return selectedrows

@app.callback(
    [
    Output("perfrating_submit_summary", "value"),
    Output("perfrating_result_modal", "is_open"),
    # Output("sr_mgt_select_unit_label", "style"),
    # Output("sr_mgt_select_desig_label", "style"),
    # Output("sr_mgt_select_status_label", "style"),
    # Output("sr_mgt_psi_label", "style"),
    # Output("sr_mgt_select_sg_label", "style"),
    # Output("sr_mgt_salary_per_annum_label", "style"),
    # Output("sr_mgt_select_appt_type_label", "style"),
    Output("perfrating_result_modal_message", "is_open"),
    #Output("sr_mgt_emp_class_label", "style"),
    ],
    [
        Input("perfrating_btn_save_sr_entry", "n_clicks"),
        #Input("perfrating_result_return_close", "n_clicks"),
        Input("perfrating_result_modal_message_btn", "n_clicks"),
    ],
    [
    State("perf_rating", "value"),

    State("perf_rating_start_period", "date"),
    State("perf_rating_end_period", "date"),
    State("perfrating_query_main_unit_srmanagemnt", "value"),
    State("perfrating_query_designation_srmanagemnt", "value"),

    # State("sr_mgt_psi", "value"),
    # State("sr_mgt_select_sg", "value"),
    # State("sr_mgt_salary_per_annum", "value"),
    # State("sr_mgt_remarks", "value"),
    # State("sr_sessionentitlement", "data"),
    # State("sr_mgt_select_unit_label", "style"),
    # State("sr_mgt_select_desig_label", "style"),
    # State("sr_mgt_select_status_label", "style"),
    # State("sr_mgt_psi_label", "style"),
    # State("sr_mgt_select_sg_label", "style"),
    # State("sr_mgt_salary_per_annum_label", "style"),
    State('url','search'),
    State('current_user_id', 'data'),
    # State("sr_mgt_is_primary", "value"),
    State("perfrating_mgt_delete_ind", "value"),
    # State("sr_mgt_select_appt_type", "value"),
    # State("sr_mgt_select_appt_type_label", "style"),
    State('sessioncurrentrole', 'data'),
    State("perfrating_result_modal_message", "is_open"),
    #State("sr_mgt_update_emp", "value"),
    #State("sr_mgt_emp_class", "value"),
    #State("sr_mgt_is_active", "value"),
    #State("sr_mgt_emp_class", "style"),
    #State("sr_mgt_select_sg_type", "value"),
    ],
)
def save_sr(perfrating_btn_save_sr_entry,
    #perfrating_result_return_close,
    perfrating_result_modal_message_btn,
    perf_rating,
    perf_rating_start_period,
    perf_rating_end_period,
    perfrating_query_main_unit_srmanagemnt,
    perfrating_query_designation_srmanagemnt,

    # sr_mgt_select_unit, sr_mgt_select_desig, sr_mgt_select_status, sr_mgt_start_date,
    # sr_mgt_end_date_chk, sr_mgt_end_date, sr_mgt_psi, sr_mgt_select_sg,sr_mgt_salary_per_annum,sr_mgt_remarks,
    # sr_sessionentitlement,sr_mgt_select_unitlabel,sr_mgt_select_desiglabel,sr_mgt_select_statuslabel,
    # sr_mgt_psilabel,sr_mgt_select_sglabel,sr_mgt_salary_per_annumlabel,

    url,current_user_id,
    # sr_mgt_is_primary,

    sr_mgt_delete_ind,
    # sr_mgt_select_appt_type,sr_mgt_select_appt_type_label,

    sessioncurrentrole,
    perfrating_result_modal_message,

    # sr_mgt_update_emp,
    # sr_mgt_emp_class,sr_mgt_is_active, sr_mgt_emp_class_label,sr_mgt_select_sg_type #,sr_mgt_remarks_label
    ):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid=="perfrating_btn_save_sr_entry":
            perf_ratingvalid,perf_ratinginvalid = checkiflengthzero(perf_rating)
            perfrating_query_main_unit_srmanagemntvalid,perfrating_query_main_unit_srmanagemntinvalid = checkiflengthzero(perfrating_query_main_unit_srmanagemnt)
            perfrating_query_designation_srmanagemntvalid,perfrating_query_designation_srmanagemntinvalid = checkiflengthzero(perfrating_query_designation_srmanagemnt)
            # sr_mgt_select_desigvalid,sr_mgt_select_desiginvalid = checkiflengthzero(sr_mgt_select_desig)
            # sr_mgt_select_statusvalid,sr_mgt_select_statusinvalid = checkiflengthzero(sr_mgt_select_status)
            # sr_mgt_psivalid,sr_mgt_psiinvalid = checkiflengthzero(sr_mgt_psi)
            # sr_mgt_select_sgvalid,sr_mgt_select_sginvalid = checkiflengthzero(sr_mgt_select_sg)
            # sr_mgt_salary_per_annumvalid,sr_mgt_salary_per_annuminvalid = checkiflengthzero(sr_mgt_salary_per_annum)
            # sr_mgt_select_appt_typevalid,sr_mgt_select_appt_typeinvalid= checkiflengthzero(sr_mgt_select_appt_type)
            # sr_mgt_emp_classvalid,sr_mgt_emp_classinvalid= checkiflengthzero(sr_mgt_emp_class)
            # sr_mgt_select_unitlabel = checkstyle(sr_mgt_select_unitinvalid)
            # sr_mgt_select_desiglabel = checkstyle(sr_mgt_select_desiginvalid)
            # sr_mgt_select_statuslabel = checkstyle(sr_mgt_select_statusinvalid)
            # sr_mgt_psilabel = checkstyle(sr_mgt_psiinvalid)
            # sr_mgt_select_sglabel = checkstyle(sr_mgt_select_sginvalid)
            # sr_mgt_salary_per_annumlabel = checkstyle(sr_mgt_salary_per_annuminvalid)
            # sr_mgt_select_appt_type_label = checkstyle(sr_mgt_select_appt_type)
            # sr_mgt_emp_class_label = checkstyle(sr_mgt_emp_classinvalid)

            #required fields per type of appt type:
            # if sr_mgt_select_appt_type in [45, 36,32,31,33,34,35]:
            #     valid = [sr_mgt_select_unitvalid]
            # elif sr_mgt_select_appt_type in [1,2,3,4,5,6,7,8,9,10,11,12,13,14]:
            #     valid = [sr_mgt_select_unitvalid,sr_mgt_select_desigvalid,sr_mgt_select_statusvalid,sr_mgt_select_appt_typevalid,sr_mgt_emp_classvalid]
            # else:
            #     valid = [sr_mgt_select_unitvalid,sr_mgt_select_desigvalid,sr_mgt_select_statusvalid,sr_mgt_select_appt_typevalid,sr_mgt_emp_classvalid]
            # if 1 in sr_mgt_is_primary:
            #     sr_mgt_is_primary = True
            # else:
            #     sr_mgt_is_primary = False
            #
            # if 1 in sr_mgt_update_emp:
            #     sr_mgt_update_emp = True
            # else:
            #     sr_mgt_update_emp = False
            valid = [perf_ratingvalid, perfrating_query_main_unit_srmanagemntvalid, perfrating_query_designation_srmanagemntvalid]
            if all(valid):
                parsed = urlparse.urlparse(url)
                mode = str(parse_qs(parsed.query)['mode'][0])
                eid = str(parse_qs(parsed.query)['eid'][0])
                #update_all_primary(eid)
                # if 1 not in sr_mgt_end_date_chk:
                #     sr_mgt_end_date = None
                if mode in ["add"]:
                    perfrating_val = [eid, perf_rating_start_period, perf_rating_end_period, perf_rating,
                        current_user_id, datetime.now(), False, perfrating_query_main_unit_srmanagemnt, perfrating_query_designation_srmanagemnt]
                    sqlbpstatuses = """
                        INSERT INTO performance_ratings (emp_id, perf_rating_start_period, perf_rating_end_period, perf_rating_ipcr,
                            perf_rating_inserted_by, perf_rating_inserted_on, perf_rating_delete_ind, perf_unit_id, perf_emp_designation_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING perf_rating_id

                    """
                    perf_rating_id = modifydatabasereturnid(sqlbpstatuses, perfrating_val)
                    # if len(sr_sessionentitlement)>0:
                    #     insert_sr_entitlements(sr_sessionentitlement, current_user_id, sr_id)
                # elif mode =="convert":
                #     bpid = str(parse_qs(parsed.query)['bpid'][0])
                #     service_records_val = [eid, sr_mgt_is_primary, sr_mgt_select_desig, sr_mgt_select_unit, sr_mgt_select_status,
                #         sr_mgt_start_date,sr_mgt_end_date, sr_mgt_psi, sr_mgt_select_sg,sr_mgt_salary_per_annum,sr_mgt_remarks,
                #         current_user_id, datetime.now(), False,sr_mgt_emp_class,sr_mgt_select_appt_type,bpid, sr_mgt_select_sg_type]
                #     sqlbpstatuses = """
                #         INSERT INTO service_records(emp_id,sr_is_primary, sr_design_id, sr_unit_id, sr_status_id,
                #             sr_start_date,sr_end_date, sr_psi_id,sr_salary_grade_id,sr_salary_rate,sr_remarks,sr_inserted_by,sr_inserted_on,
                #             sr_delete_ind, sr_class_id, sr_appt_type_id, bp_id, sr_entitle_type_id)
                #         VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s) RETURNING sr_id
                #
                #     """
                #     sr_id = modifydatabasereturnid(sqlbpstatuses, service_records_val)
                #     if len(sr_sessionentitlement)>0:
                #         insert_sr_entitlements(sr_sessionentitlement, current_user_id, sr_id)
                #
                #
                #     sqlfalse = """ UPDATE bp_status_changes
                #                       SET bp_status_change_current_ind = %s
                #                         WHERE bp_id = %s"""
                #     values = (False, bpid)
                #     modifydatabase(sqlfalse, values)
                #
                #
                #     bp_statuses = [bpid, 20, current_user_id, sessioncurrentrole, datetime.now(), False, True]
                #     sqlbpstatuses = """
                #         INSERT INTO bp_status_changes(bp_id, bp_status_id, bp_status_change_by, bp_status_change_role_id,
                #             bp_status_change_on, bp_status_change_delete_ind, bp_status_change_current_ind)
                #         VALUES (%s, %s, %s, %s, %s, %s, %s)
                #
                #     """
                #     modifydatabase(sqlbpstatuses, bp_statuses)
                else:
                    perf_rating_id = str(parse_qs(parsed.query)['perf_rating_id'][0])
                    if 1 in sr_mgt_delete_ind:
                        delete_ind = True
                    else:
                        delete_ind = False
                    perfrating_val = [eid, perf_rating_start_period, perf_rating_end_period, perf_rating,
                        current_user_id, datetime.now(), delete_ind, perfrating_query_main_unit_srmanagemnt, perfrating_query_designation_srmanagemnt, perf_rating_id]

                    sqlbpstatuses = """
                        UPDATE performance_ratings SET emp_id=%s, perf_rating_start_period = %s, perf_rating_end_period = %s,
                        perf_rating_ipcr= %s, perf_rating_inserted_by= %s, perf_rating_inserted_on = %s, perf_rating_delete_ind= %s,
                        perf_unit_id = %s, perf_emp_designation_id = %s
                        WHERE perf_rating_id = %s
                    """

                    modifydatabase(sqlbpstatuses, perfrating_val)
                # if sr_mgt_is_primary and sr_mgt_update_emp:
                #     if 1 in sr_mgt_is_active:
                #         sr_mgt_is_active=True
                #     else:
                #         sr_mgt_is_active =False
                #     emp_values = (sr_mgt_select_status,sr_mgt_select_desig,sr_mgt_select_unit,sr_mgt_select_sg,sr_mgt_salary_per_annum,sr_mgt_emp_class,sr_mgt_is_active, sr_mgt_select_sg_type, eid )
                #     update_employees_table(emp_values)
                perfrating_result_modal_message = False
                return [1,True,perfrating_result_modal_message]
            else:
                perfrating_result_modal_message = True
                return [0,False,perfrating_result_modal_message]
        # elif eventid=="perfrating_result_return_close":
        #     return [2,False,perfrating_result_modal_message]
        elif eventid=="perfrating_result_modal_message_btn":
            perfrating_result_modal_message = False
            return [2,False,perfrating_result_modal_message]


        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

# def update_all_primary(emp_num):
#
#     sqlbpstatuses = """
#         UPDATE service_records SET  sr_is_primary=%s WHERE emp_id =%s
#     """
#     service_records_val = [False,emp_num]
#     #print("service_records_val",service_records_val)
#     modifydatabase(sqlbpstatuses, service_records_val)
#
# def update_employees_table(emp_values):
#     sqlbpstatuses = """
#         UPDATE employees SET emp_status_id=%s, emp_primary_designation_id=%s,
#             emp_primary_home_unit_id=%s,emp_salary_grade_id=%s, emp_salary_amount=%s,emp_class_id=%s,emp_is_active=%s, emp_entitle_type_id=%s
#         WHERE emp_id =%s
#
#     """
#     modifydatabase(sqlbpstatuses, emp_values)
#
# def insert_sr_entitlements(entitlements_dict, current_user_id, sr_id):
#     sqleentitlements = """
#         INSERT INTO sr_entitlements(entitle_id, entitle_type_id,sr_entitle_amount,sr_entitle_remarks,sr_id,sr_entitle_inserted_by, sr_entitle_inserted_on, sr_entitle_delete_ind)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#
#     """
#     entitlementsdf = pd.DataFrame(entitlements_dict)
#     entitlementsdf = entitlementsdf.values.tolist()
#     finalentitlements = []
#     for item in entitlementsdf:
#         item.append(sr_id)
#         item.append(current_user_id)
#         item.append(datetime.now())
#         item.append(False)
#         finalentitlements.append(item)
#     #print(finalentitlements)
#     bulkmodifydatabase(sqleentitlements, finalentitlements)




# @app.callback([
#     Output('sr_mgt_salary_per_annum', 'value'),
# ],
#     [
#     Input('sr_mgt_select_sg', 'value'),
#     Input('sr_mgt_start_date', 'date'),
#     Input('sr_mgt_select_sg_type','value'),
#     Input('url', 'search'),
# ],[
#     State('sr_mgt_salary_per_annum', 'value'),
#     State('url', 'pathname'),
# ])
# def toggle_divforeigncit(obppropsg,bpren_propapptstartdate,bpren_entitle_type,url,bpren_propsalaryrate,pathname):
#
#     parsed = urlparse.urlparse(url)
#     mode = str(parse_qs(parsed.query)['mode'][0])
#     # print(pathname)
#     # print(mode)
#     if mode=="add" and pathname=="/servicerecord/sr_management_profile":
#         ctx = dash.callback_context
#         if ctx.triggered:
#             eventid = ctx.triggered[0]['prop_id'].split('.')[0]
#             if eventid in ['sr_mgt_select_sg','sr_mgt_start_date','sr_mgt_select_sg_type'] and (obppropsg and bpren_propapptstartdate and bpren_entitle_type):
#
#                 sql = "SELECT sg_version_salary_rate FROM salary_grade_versions sgv INNER JOIN salary_grades sg ON sgv.sg_id = sg.sg_id  WHERE sg_version_start_date <= %s AND sg_version_end_date >= %s and sg.sg_id = %s"
#                 values = (bpren_propapptstartdate,bpren_propapptstartdate, obppropsg)
#                 columns = ['sg_version_salary_rate']
#                 dfsql = securequerydatafromdatabase(sql, values, columns)
#                 if bpren_entitle_type==6:
#                     return [dfsql['sg_version_salary_rate'][0]*12]
#                 else:
#                     return [dfsql['sg_version_salary_rate'][0]]
#             else:
#                 raise PreventUpdate
#         else:
#             raise PreventUpdate
#     elif mode=="edit" and  pathname=="/servicerecord/sr_management_profile":
#         eid = str(parse_qs(parsed.query)['srid'][0])
#         sql = "SELECT sr_salary_rate FROM service_records WHERE sr_id=%s "
#         values = (eid,)
#         columns = ['sr_salary_rate']
#         dfsql = securequerydatafromdatabase(sql, values, columns)
#     #    print(dfsql)
#         return [dfsql['sr_salary_rate'][0]]
#     elif mode=="convert" and  pathname=="/servicerecord/sr_management_profile":
#         bpid = str(parse_qs(parsed.query)['bpid'][0])
#         sql = "SELECT bp_salary_hon_amount FROM basic_papers WHERE bp_id=%s "
#         values = (bpid,)
#         columns = ['bp_salary_hon_amount']
#         dfsql = securequerydatafromdatabase(sql, values, columns)
#     #    print(dfsql)
#         return [dfsql['bp_salary_hon_amount'][0]]
#     else:
#         raise PreventUpdate







@app.callback(
    [
    Output("perf_rating", "value"),
    # Output("sr_mgt_select_desig", "value"),
    # Output("sr_mgt_select_status", "value"),
    Output("perf_rating_start_period", "date"),
    Output("perf_rating_end_period", "date"),
    Output("perfrating_query_main_unit_srmanagemnt", "value"),
    Output("perfrating_query_designation_srmanagemnt", "value"),

    # Output("sr_mgt_end_date_chk", "value"),
    # Output("sr_mgt_end_date", "date"),
    # Output("sr_mgt_psi", "value"),
    # Output("sr_mgt_select_sg", "value"),

    # Output("sr_mgt_remarks", "value"),
    # Output("sr_mgt_select_appt_type", "value"),
    # Output("sr_mgt_select_desig_old", "children"),
    # Output("sr_mgt_select_appointment_old", "children"),
    # #Output('sr_mgt_salary_per_annum', 'value'),
    # Output('sr_mgt_emp_class', 'value'),
    # Output('sr_mgt_select_sg_type', 'value'),
    ],
    [
        Input("perfrating_submit_summary", "value"),
        Input("perfrating_load_sr", "value"),
        Input("url", "search"),
    ],
    [
    State("perf_rating", "value"),
    # State("sr_mgt_select_desig", "value"),
    # State("sr_mgt_select_status", "value"),
    State("perf_rating_start_period", "date"),
    State("perf_rating_end_period", "date"),
    State("perfrating_query_main_unit_srmanagemnt", "value"),
    State("perfrating_query_designation_srmanagemnt", "value"),
    # State("sr_mgt_end_date_chk", "value"),
    # State("sr_mgt_end_date", "date"),
    # State("sr_mgt_psi", "value"),
    # State("sr_mgt_select_sg", "value"),
    # State("sr_mgt_salary_per_annum", "value"),
    # State("sr_mgt_remarks", "value"),
    # State("sr_sessionentitlement", "data"),
    #State('url','search'),
    State("url", "pathname"),
    # State("sr_mgt_select_appt_type", "value"),
    #     State("sr_mgt_select_desig_old", "children"),
    #     State("sr_mgt_select_appointment_old", "children"),
    #     State('sr_mgt_emp_class', 'value'),
    #     State('sr_mgt_select_sg_type', 'value'),
    ],
)
def clear_sr_form(
    perfrating_submit_summary,
    perfrating_load_sr,
    url,
    perf_rating,
    perf_rating_start_period,
    perf_rating_end_period,
    perfrating_query_main_unit_srmanagemnt,
    perfrating_query_designation_srmanagemnt,

    # sr_submit_summary,sr_load_sr,
    # sr_mgt_select_unit, sr_mgt_select_desig, sr_mgt_select_status, sr_mgt_start_date,
    # sr_mgt_end_date_chk, sr_mgt_end_date, sr_mgt_psi, sr_mgt_select_sg,sr_mgt_salary_per_annum,sr_mgt_remarks,
    # sr_sessionentitlement,

    pathname
    #sr_appt_type_id,sr_mgt_select_desig_old,sr_appt_type_name_old,sr_mgt_emp_class,sr_mgt_select_sg_type
    ):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        parsed = urlparse.urlparse(url)
        mode = str(parse_qs(parsed.query)['mode'][0])
        empid = str(parse_qs(parsed.query)['eid'][0])

    #    print("clear_sr_form", eventid)
        if eventid == 'perfrating_submit_summary':
            if perfrating_submit_summary==1:
                perf_rating=None
                perf_rating_start_period = None
                perf_rating_end_period=None
                perfrating_query_main_unit_srmanagemnt = None
                perfrating_query_designation_srmanagemnt = None


        elif eventid == 'perfrating_load_sr':
            #print("sr+load",mode)
            if mode=="edit":
                perf_rating_id = str(parse_qs(parsed.query)['perf_rating_id'][0])

                #print("srid",srid)

                sqlcommand = '''SELECT perf_rating_ipcr, perf_rating_start_period, perf_rating_end_period,
                    perf_unit_id, perf_emp_designation_id
                    FROM performance_ratings pr
                    INNER JOIN employees e ON pr.emp_id = e.emp_id

                    WHERE perf_rating_id=%s'''

                values = (perf_rating_id, )
                columns = ['perf_rating_ipcr', 'perf_rating_start_period', 'perf_rating_end_period', 'perf_unit_id', 'perf_emp_designation_id']
                df = securequerydatafromdatabase(sqlcommand, values, columns)
                perf_rating= df["perf_rating_ipcr"][0]
            #    print(df["sr_design_id"][0])
                perf_rating_start_period =  df["perf_rating_start_period"][0]
                perf_rating_end_period= df["perf_rating_end_period"][0]
                perfrating_query_main_unit_srmanagemnt= df["perf_unit_id"][0]
                perfrating_query_designation_srmanagemnt= df["perf_emp_designation_id"][0]

            elif mode == "add":
                perf_rating=None
                perf_rating_start_period = None
                perf_rating_end_period=None
                sqlcommand = '''SELECT u.unit_id, d.designation_id

                FROM persons p INNER JOIN employees e on e.person_id = p.person_id
                LEFT JOIN designations d on d.designation_id = e.emp_primary_designation_id
                LEFT JOIN units u on u.unit_id = e.emp_primary_home_unit_id


                WHERE e.emp_id = %s and e.emp_delete_ind = %s'''
                values = (empid, False)
                columns = ['unit_id', 'designation_id']

                df = securequerydatafromdatabase(sqlcommand, values, columns)
                perfrating_query_main_unit_srmanagemnt=  df["unit_id"][0]
                perfrating_query_designation_srmanagemnt =  df["designation_id"][0]


        else:
            raise PreventUpdate
        return [perf_rating, perf_rating_start_period, perf_rating_end_period, perfrating_query_main_unit_srmanagemnt, perfrating_query_designation_srmanagemnt] #sr_mgt_salary_per_annum
    else:
        raise PreventUpdate

#
# @app.callback([
#     Output('sr_mgt_salary_per_annum', 'value'),
# ],
#     [
#     Input('sr_mgt_select_sg', 'value'),
#     Input('sr_mgt_start_date', 'date'),
# ],)
# def toggle_divforeigncit(obppropsg,bpren_propapptstartdate):
#     ctx = dash.callback_context
#     if ctx.triggered:
#         eventid = ctx.triggered[0]['prop_id'].split('.')[0]
#         if eventid in ['sr_mgt_select_sg','sr_mgt_start_date'] and (obppropsg and bpren_propapptstartdate):

#             return [returnval]
#         else:
#             raise PreventUpdate
#     else:
#         raise PreventUpdate

def checkstyle(isvalidcomponent):
    if isvalidcomponent:
        style = {"text-align": "left", 'color': 'red', 'font-size':'bold'}
    else:
        style = {"text-align": "left", 'color': 'black', 'font-size':'normal'}
    return style

def checkiflengthzero(stringvar):
    isvalid = False
    isinvalid = False

    if stringvar:
        isvalid = True
        isinvalid = False
    else:
        isvalid = False
        isinvalid = True
    return isvalid, isinvalid

@app.callback(
    [
        #    Output('query_employee_class', 'options'),
        Output('perfrating_query_main_unit_srmanagemnt', 'options'),
        #Output('perfrating_query_main_unit_srmanagemnt', 'value')
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        #@State("url", "pathname")
        # State('perfrating_query_faculty_mainunitnone_srmanagemnt', 'value'),
        # State('perfrating_query_main_unit_srmanagemnt', 'options'),
        # State('perfrating_query_main_unit_srmanagemnt', 'value')
    ],
)
def fillindropdowns(pathname#, perfrating_query_faculty_mainunitnone_srmanagemnt,
    # perfrating_query_main_unit_srmanagemnt,
    # perfrating_query_main_unit_srmanagemntval
    ):
    # parsed = urlparse.urlparse(url)
    if pathname == "/settings/settings_perfrating_management_profile":

        # empid = str(parse_qs(parsed.query)['eid'][0])
        # unit = '''
        #     SELECT unit_id
        #     FROM persons p INNER JOIN employees e on e.person_id = p.person_id
        #     LEFT JOIN units u on u.unit_id = e.emp_primary_home_unit_id
        #     WHERE e.emp_id = %s and e.emp_delete_ind = %s
        # '''
        # values = (empid, False )
        # columns = ['unit_id']
        # df = securequerydatafromdatabase(unit, values, columns)
        # unit_name = df['unit_id'][0]
        # return [commonmodules.queryunits(), unit_name]
        return [commonmodules.queryunits()]
    else:
        raise PreventUpdate


@app.callback([
    Output('perfrating_query_designation_srmanagemnt', 'options'),

],
    [
    Input('url', 'pathname'),
],
    [
    State('url', 'search'),
    # State('sessioncurrentunit', 'data'),
    # State('sessionlistofunits', 'data'),
    # State('admin_pos_id', 'data')

],)
def designation_fillindropdowns(path, url):
    parsed = urlparse.urlparse(url)
    if path == "/settings/settings_perfrating_management_profile":
        # mode = str(parse_qs(parsed.query)['mode'][0])
        # if mode == "edit":
        #     admin_pos_load_data = 1
        # else:
        #     admin_pos_load_data = 2
        # listofallowedunits = tuple(sessionlistofunits[str(sessioncurrentunit)])

        designation = commonmodules.queryfordropdown('''
            SELECT designation_name as label, designation_id as value
              FROM designations d
             WHERE d.designation_delete_ind = %s
           ORDER BY designation_name
        ''', (False, ))



        return [designation]
    else:
        raise PreventUpdate


@app.callback([
    Output('adjectival_rating', 'children'),
],
    [
    Input('perf_rating', 'value'),
    Input('perfrating_query_designation_srmanagemnt', 'value'),

    Input('url', 'search'),
],[
    State('adjectival_rating', 'value'),
    State('url', 'pathname'),
])
def toggle_divforeigncit(perf_rating, perfrating_query_designation_srmanagemnt, url,adjectival_rating,pathname):
    if pathname=="/settings/settings_perfrating_management_profile":
        parsed = urlparse.urlparse(url)
        mode = str(parse_qs(parsed.query)['mode'][0])
        if mode=="add" and pathname=="/settings/settings_perfrating_management_profile":
            ctx = dash.callback_context
            if ctx.triggered:
                eventid = ctx.triggered[0]['prop_id'].split('.')[0]
                if eventid in ['perf_rating', 'perfrating_query_designation_srmanagemnt'] and (perf_rating and perfrating_query_designation_srmanagemnt):

                    sql = '''SELECT perf_rating_adjectival_name from performance_rating_adjectivals pra
                    LEFT JOIN designations d ON d.designation_emp_class_id = pra.perf_rating_adjectival_emp_class_id
                    where %s BETWEEN perf_rating_adjectival_start AND perf_rating_adjectival_end
                    and designation_id = %s
                    and perf_rating_adjectival_delete_ind = %s'''
                    values = (perf_rating, perfrating_query_designation_srmanagemnt, False)

                    columns = ['perf_rating_adjectival_name']
                    dfsql = securequerydatafromdatabase(sql, values, columns)

                    try:
                        adjectival = dfsql['perf_rating_adjectival_name'][0]

                    except:
                        adjectival = "N/A"

                    return [adjectival]

                    # sql = "SELECT sg_version_salary_rate FROM salary_grade_versions sgv INNER JOIN salary_grades sg ON sgv.sg_id = sg.sg_id  WHERE sg_version_start_date <= %s AND sg_version_end_date >= %s and sg.sg_id = %s"
                    # values = (bpren_propapptstartdate,bpren_propapptstartdate, obppropsg)
                    # columns = ['sg_version_salary_rate']
                    # dfsql = securequerydatafromdatabase(sql, values, columns)
                    # if bpren_entitle_type==6:
                    #     return [dfsql['sg_version_salary_rate'][0]*12]
                    # else:
                    #     return [dfsql['sg_version_salary_rate'][0]]
                else:
                    raise PreventUpdate
            else:
                raise PreventUpdate
        elif mode=="edit" and  pathname=="/settings/settings_perfrating_management_profile":
            perf_rating_id = str(parse_qs(parsed.query)['perf_rating_id'][0])
            if perf_rating=="":
                raise PreventUpdate
            else:
                sql = '''SELECT perf_rating_adjectival_name from performance_rating_adjectivals pra
    					LEFT JOIN designations d ON d.designation_emp_class_id = pra.perf_rating_adjectival_emp_class_id
                        LEFT JOIN performance_ratings pr ON pr.perf_emp_designation_id = d.designation_id

                        where %s BETWEEN perf_rating_adjectival_start AND perf_rating_adjectival_end
                        and perf_rating_id = %s
                        and perf_rating_adjectival_delete_ind = %s'''
                values = (perf_rating, perf_rating_id, False)

                columns = ['perf_rating_adjectival_name']
                dfsql = securequerydatafromdatabase(sql, values, columns)

            try:
                adjectival = dfsql['perf_rating_adjectival_name'][0]

            except:
                adjectival = "N/A"

            return [adjectival]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
