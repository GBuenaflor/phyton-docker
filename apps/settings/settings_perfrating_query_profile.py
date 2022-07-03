import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash
import re
import flask
from dash.dependencies import Input, Output, State
from dash_extensions import Download
from dash_extensions.snippets import send_file
from apps import commonmodules
from dash.exceptions import PreventUpdate
from app import app
from apps import home
from apps.dbconnect import securequerydatafromdatabase, modifydatabase, modifydatabasereturnid,bulkmodifydatabase
import hashlib
from datetime import datetime, timedelta, date
import dash_table
import pandas as pd
import numpy as np
import urllib.parse as urlparse
from urllib.parse import parse_qs
import logging
from fpdf import FPDF
import os


app.config.suppress_callback_exceptions = True
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

layout = html.Div([
    commonmodules.get_header(),
    commonmodules.get_menu(),
    commonmodules.get_common_variables(),
    # dcc.Store(id='listofitems', storage_type='session'),
    # dcc.Store(id='listofsrs', storage_type='session'),
    html.H1("View Performance Rating"),
    dcc.Link('← View Another Employee', href='/settings/settings_perfrating_query'),

    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Employee Details"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),

            dbc.CardBody([
                # dbc.Row([
                #     dbc.Col([
                #         dbc.Label("First Name", style={"text-align": "left"}),
                #     ]),
                #     dbc.Col([
                #         dbc.Input(type="text", id="query_faculty_fname")
                #     ]),
                #     dbc.Col([
                #         dbc.Label("Middle Name", style={"text-align": "left"}),
                #     ]),
                #     dbc.Col([
                #         dbc.Input(type="text", id="query_faculty_mname")
                #     ]),
                #     dbc.Col([
                #         dbc.Label("Last Name", style={"text-align": "left"}),
                #     ]),
                #     dbc.Col([
                #         dbc.Input(type="text", id="query_faculty_lname")
                #     ]),
                # ]),
                # dbc.Row([
                #     dbc.Col([
                #         dbc.Label("Birthday", style={"text-align": "left"}),
                #     ]),
                #     dbc.Col([
                #         dbc.Input(type="text", id="query_faculty_bday")
                #     ]),
                #     dbc.Col([
                #         dbc.Label("Place of Birth", style={"text-align": "left"}),
                #     ]),
                #     dbc.Col([
                #         dbc.Input(type="text", id="query_faculty_placeofbirth")
                #     ]),
                #     dbc.Col([
                #         dbc.Label("Employee Number", style={"text-align": "left"}),
                #     ]),
                #     dbc.Col([
                #         dbc.Input(type="text", id="query_faculty_enum"),
                #         #dbc.Input(type="text", id="query_faculty_enum2")
                #     ]),
                # #    dbc.Button("Run ", id="testbtn", style={"float":"left"}, color='primary'),
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
                        dbc.Label(id="perfrating_query_faculty_profile_lname_managemnt", style={"text-align":"left",'color':'black', 'font-weight':'bold'})
                    ], width=9),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("First Name", style={"text-align": "left"}),
                    ], width=3),
                    dbc.Col([
                        dbc.Label(id="perfrating_query_faculty_profile_fname_managemnt", style={"text-align":"left",'color':'black', 'font-weight':'bold'})
                    ], width=9),
                ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Middle Name", style={"text-align": "left"}),
                    ], width=3),
                    dbc.Col([
                        dbc.Label(id="perfrating_query_faculty_profile_mname_managemnt", style={"text-align":"left",'color':'black', 'font-weight':'bold'})
                    ], width=9),
                ]),
                # dbc.Row([
                #     dbc.Col([
                #         dbc.Label("Birthday", style={"text-align": "left"}),
                #     ], width=3),
                #     dbc.Col([
                #         dbc.Label(id="query_faculty_profile_bday_srmanagemnt", style={"text-align":"left",'color':'black', 'font-weight':'bold'})
                #     ], width=9),
                # ]),
                # dbc.Row([
                #     dbc.Col([
                #         dbc.Label("Place of Birth", style={"text-align": "left"}),
                #     ], width=3),
                #     dbc.Col([
                #         dbc.Label(id="query_faculty_profile_placeofbirth_srmanagemnt", style={"text-align":"left",'color':'black', 'font-weight':'bold'})
                #     ], width=9),
                # ]),

                dbc.Row([
                    dbc.Col([
                        dbc.Label("Employee Number", style={"text-align": "left"}),
                    ], width=3),
                    dbc.Col([
                        dbc.Label(id="perfrating_query_faculty_profile_enum_managemnt", style={"text-align":"left",'color':'black', 'font-weight':'bold'})
                    ], width=9),
                ]),
                # dbc.Row([
                #     dbc.Col([
                #         dbc.Label("Main Unit:", style={"text-align": "left"}),
                #     ], width=3),
                #     dbc.Col([
                #         dbc.Label(id="query_faculty_profile_unit_srmanagemnt", style={"text-align":"left",'color':'black', 'font-weight':'bold'})
                #     ], width=9),
                # ]),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Main Unit:", style={"text-align": "left"}),
                    ], width=3),
                    dbc.Col([
                        dbc.Label(
                            id='perfrating_query_faculty_profile_unit_dd', style={"text-align":"left",'color':'black', 'font-weight':'bold'}
                        ),
                    ], width=9),
                ],align="center"),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Primary Designation:", style={"text-align": "left"}),
                    ], width=3),
                    dbc.Col([
                        dbc.Label(
                            id='perfrating_query_faculty_profile_designation_dd', style={"text-align":"left",'color':'black', 'font-weight':'bold'}
                        ),
                    ], width=9),
                ],align="center"),
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Employee Class:", style={"text-align": "left"}),
                    ], width=3),
                    dbc.Col([
                        dbc.Label(
                            id='perfrating_query_faculty_profile_class_dd', style={"text-align":"left",'color':'black', 'font-weight':'bold'}
                        ),
                    ], width=9),
                ],align="center"),

                html.Br(),


                html.Br(),
                dbc.Col([

                    html.Hr(),
                    html.H3("Existing Performance Ratings"),
                    dbc.FormText("If no adjectival rating appears, please assign an employee class to the designation through the Designations Module."),
                    html.Br(),
                    dbc.Row([

                        dbc.Col([
                            dbc.Button("Add Performance Rating", color="primary", className="mr-1",
                                    id="perfrating_add_pr"),
                        ]),
                        html.Br(),

                    ]),
                    html.Hr(),

                    html.Div([

                    ], id="perfrating_queryprlist"),


                ],


                ),
                dbc.Modal(
                    [
                        dbc.ModalHeader(
                            html.H4(["Update Performance Rating Record"], id='perfrating_edit_sr_modal_head')),
                        dbc.ModalBody([
                            "Update Successful"
                        ]),
                        dbc.ModalFooter([
                            dbc.Button(
                                        "Close", id="perfrating_update_main_sr_modal_close", style={"float":"left"}, color='primary')
                        ]),
                    ],
                    id="perfrating_update_main_sr_modal",
                    centered=True,
                    backdrop='static',
                    size="xl",
                ),

        ], style={'line-height': "1em", "display": "block"}
        )
        ]),
    ]),
])

# #

@app.callback(
    [
        Output("perfrating_query_faculty_profile_lname_managemnt", "children"),
        Output("perfrating_query_faculty_profile_fname_managemnt", "children"),
        Output("perfrating_query_faculty_profile_mname_managemnt", "children"),
        # Output("query_faculty_profile_bday_srmanagemnt", "children"),
        # Output("query_faculty_profile_placeofbirth_srmanagemnt", "children"),
        Output("perfrating_query_faculty_profile_enum_managemnt", "children"),
    #    Output("query_faculty_profile_unit_srmanagemnt", "children"),
    #    Output("query_faculty_profile_designation_srmanagemnt", "children"),
    #    Output("query_faculty_profile_status_srmanagemnt", "children"),
        Output("perfrating_add_pr", 'href'),
        #Output('sr_edit_status', 'options'),
        #Output('sr_edit_rank', 'options'),
        #Output('sr_edit_sg', 'options'),
        #Output('sr_edit_unit', 'options'),

        #Output('perfrating_query_faculty_profile_unit_dd', 'options'),
        #Output('perfrating_query_faculty_profile_designation_dd', 'options'),
        # Output('query_faculty_profile_sg_dd', 'options'),
        # Output('query_faculty_profile_employee_status_dd', 'options'),
        # Output('query_faculty_profile_employee_isactive_dd', 'options'),

        Output('perfrating_query_faculty_profile_unit_dd', 'children'),
        Output('perfrating_query_faculty_profile_designation_dd', 'children'),
        # Output('query_faculty_profile_sg_dd', 'value'),
        # Output('query_faculty_profile_employee_status_dd', 'value'),
        # Output('query_faculty_profile_employee_isactive_dd', 'value'),
        # Output('query_faculty_profile_salary_dd', 'value'),

        #Output('perfrating_query_faculty_profile_class_dd', 'options'),
        Output('perfrating_query_faculty_profile_class_dd', 'children'),
        # Output('query_faculty_profile_sgrate_dd', 'options'),
        # Output('query_faculty_profile_sgrate_dd', 'value'),
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
    if parsed.query and pathname =="/settings/settings_perfrating_query_profile":
        empid = str(parse_qs(parsed.query)['eid'][0])
        sqlcommand = '''SELECT person_first_name, person_middle_name,
            person_last_name, designation_name, unit_name,
            emp_number, emp_primary_home_unit_id, emp_primary_designation_id,
            emp_class_name
        FROM persons p INNER JOIN employees e on e.person_id = p.person_id
        LEFT JOIN designations d on d.designation_id = e.emp_primary_designation_id
        LEFT JOIN units u on u.unit_id = e.emp_primary_home_unit_id
        LEFT JOIN emp_classes ec ON ec.emp_class_id = e.emp_class_id
        WHERE e.emp_id = %s and e.emp_delete_ind = %s'''
        values = (empid, False)
        columns = ['person_first_name', 'person_middle_name',
                   'person_last_name', 'designation_name','unit_name','emp_number',
                   'emp_primary_home_unit_id', 'emp_primary_designation_id',
                   'emp_class_name']
        df = securequerydatafromdatabase(sqlcommand, values, columns)
        #print(df)
        person_first_name = df["person_first_name"][0]
        person_middle_name = df["person_middle_name"][0]
        person_last_name = df["person_last_name"][0]
        # person_dob = df["person_dob"][0]
        # person_pob = df["person_pob"][0]
        designation_name =  df["designation_name"][0]
        unit_name=  df["unit_name"][0]
        emp_number = df["emp_number"][0]
        emp_class_name = df["emp_class_name"][0]
        #emp_entitle_type_id =
        #print(df["emp_is_active"][0])
        # if df["emp_is_active"][0]:
        #     emp_is_active=  "Active"
        #     emp_is_active_val = True
        # else:
        #     emp_is_active=  "Inactive"
        #     emp_is_active_val = False
        href="/settings/settings_perfrating_management_profile?mode=add&eid="+str(empid)

#SELECT CONCAT(unit_name,' (', unit_code, ') ') as label, unit_id as value
        # listofunits = commonmodules.queryfordropdown('''
        #     SELECT unit_code as label, unit_id as value
        #    FROM units
        #    WHERE unit_delete_ind = %s
        #    ORDER BY unit_name
        # ''', (False, ))
        # # salarygrades = commonmodules.queryfordropdown('''
        # #     SELECT sg_number_step as label, sg_number_step_id as value
        # #    FROM sg_number_steps
        # #    WHERE sg_number_delete_ind = %s
        # #    ORDER BY sg_number_step
        # # ''', (False, ))
        #
        # designationoptions = commonmodules.queryfordropdown('''
        #     SELECT designation_name as label, designation_id as value
        #    FROM designations
        #    WHERE designation_delete_ind = %s
        #    ORDER BY designation_name
        # ''', (False, ))
        #
        # emp_classes = commonmodules.queryfordropdown('''
        #     SELECT emp_class_name as label, emp_class_id as value
        #    FROM emp_classes
        #    WHERE emp_class_delete_ind = %s
        #    ORDER BY emp_class_name
        # ''', (False, ))

        # statuses = commonmodules.queryfordropdown('''
        #     SELECT emp_status_name as label, emp_status_id as value
        #    FROM emp_statuses
        #    WHERE emp_status_delete_ind = %s
        #    ORDER BY emp_status_name
        # ''', (False, ))

        # isactivestatuses = [{'label':'Active','value':True},{'label':'Inactive','value':False}]


        # sqlcommand = '''SELECT sr_id, designation_name, sr_start_date, sr_end_date, atp.appt_type_name,
        #     sg_number_step, sr_salary_rate,
        #     unit_name, sr_remarks, CASE
        #        WHEN sr_delete_ind=false
        #             THEN 'Visible'
        #        WHEN sr_delete_ind=true
        #             THEN 'Deleted'
        #     END sr_delete_ind
        #
        #     FROM service_records sr INNER JOIN employees e on e.emp_id = sr.emp_id
        #     LEFT JOIN units u ON u.unit_id = sr_unit_id
        #     LEFT JOIN designations d on d.designation_id = sr.sr_design_id
        #     LEFT JOIN salary_grades sg ON sg.sg_id = sr.sr_salary_grade_id
        #     LEFT JOIN appointment_types atp ON atp.appt_type_id = sr.sr_appt_type_id
        #     WHERE e.emp_id = %s and e.emp_delete_ind = %s
        #     '''
        # columns = ['sr_id', 'sr_design', 'sr_start_date',
        #                'sr_end_date', 'sr_appt_type',"sg_number_step", "sr_salary_rate", 'unit_name',"sr_remarks","sr_delete_ind"]
        #
        # if 1 in query_hidden_options:
        #     sqlcommand = sqlcommand + ''' AND sr_appt_type_id IN %s'''
        # sqlcommand = sqlcommand + ''' ORDER BY sr_start_date, sr_salary_rate'''
        # values = [empid, False]
        # values.append((8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28))


    #    df = securequerydatafromdatabase(sqlcommand, values, columns)
    #    df.columns = ["SR_ID", "Designation", "Start Date", "End Date", "Appointment Type","SG Step","Salary",  "Unit", "Remarks"]

        # sgobpentitlementtype = commonmodules.queryfordropdown('''
        #     SELECT entitle_type_name as label, entitle_type_id as value
        #    FROM entitlement_types
        #    WHERE entitle_type_delete_ind = %s and entitle_type_id in %s
        #    ORDER BY entitle_type_name
        # ''', (False,(6,16)))

        return [person_last_name, person_first_name,person_middle_name, emp_number,
             href,
            #listofunits, designationoptions,
            unit_name, designation_name,
            #emp_classes,
            emp_class_name]
    else:
        raise PreventUpdate


# @app.callback([
#     Output('perfrating_query_faculty_profile_unit_dd', 'disabled'),
#     Output('perfrating_query_faculty_profile_designation_dd', 'disabled'),
#     # Output('query_faculty_profile_sg_dd', 'disabled'),
#     # Output('query_faculty_profile_salary_dd', 'disabled'),
#     # Output('query_faculty_profile_employee_status_dd', 'disabled'),
#     # Output('query_faculty_profile_employee_isactive_dd', 'disabled'),
#     Output('perfrating_query_faculty_profile_class_dd', 'disabled'),
#
#     #Output('divsr_save_main_service_record', 'style'),
#     #Output('query_faculty_profile_sgrate_dd', 'disabled'),
#                ],
#               [
#     Input("cb_edit_main", "value"),
# ],
#     [
#     #State('queryservicerecordlist', 'children'),
# ],)
# def disable_editing(cb_edit_main):
#     if 1 in cb_edit_main:
#
#         return [False,False,False,False,False,False,False,{'display':'inline'}, False]
#     else:
#         return [True,True, True, True, True, True,  True,{'display':'none'}, True]

    #raise PreventUpdate
#
# for value1 in app.layout['listofitems-2'].data:
#     @app.callback(
#         [Output("test3", 'is_open'),]
#         [
#         Input(value1, 'n_clicks')
#         ])
#     def test(n_clicks):
#         return [True]

@app.callback([
    Output('perfrating_queryprlist', 'children'),
    #Output('querysqlservicerecordlist', 'children'),
    #Output('listofitems', 'data'),
    #Output('querysqlservicerecordlistadditional','children')
               ],
              [
    Input("url", "pathname"),
    #Input('query_hidden_options', 'value'),
    #Input('query_deleted_srs', 'value'),
    #Input('query_order_order','value')
],
    [
    State("url","search")
],)
def querylistofsrs(pathname, url ):
    parsed = urlparse.urlparse(url)
#    print("url", url, "pathname", pathname)
    if parsed.query and pathname=="/settings/settings_perfrating_query_profile":
        empid = str(parse_qs(parsed.query)['eid'][0])
        # sqlcommand = '''SELECT sr_id, designation_name, sr_start_date, sr_end_date, sr_appt_type, unit_name


        # values = [empid, False]
        sqlcommand = '''SELECT perf_rating_id, perf_rating_start_period, perf_rating_end_period, unit_name, designation_name, pr.perf_emp_designation_id, perf_rating_ipcr FROM performance_ratings pr
        INNER JOIN units u ON u.unit_id = pr.perf_unit_id
        INNER JOIN designations d ON d.designation_id = pr.perf_emp_designation_id
        WHERE emp_id = %s and perf_rating_delete_ind = %s
        ORDER by perf_rating_start_period'''
        values = (empid, False, )
        columns = ["perf_rating_id", "perf_rating_start_period", "perf_rating_end_period", "unit_name", "designation_name", "perf_emp_designation_id", "perf_rating"]
        df = securequerydatafromdatabase(sqlcommand, values, columns)
        df.columns = ["Rating ID", "Start Period", "End Period", "Unit Name", "Designation", "Designation ID", "Performance Rating"]
        columns = [{"name": i, "id": i} for i in df.columns]
        data = df.to_dict("rows")
        linkcolumn = {}
        viewcolumn = {}
        listofids = []



        for index, row in df.iterrows():
            if row["Performance Rating"] != None:
                sqladjectival = '''SELECT perf_rating_adjectival_name from performance_rating_adjectivals pra
                LEFT JOIN designations d ON d.designation_emp_class_id = pra.perf_rating_adjectival_emp_class_id
                where %s BETWEEN perf_rating_adjectival_start AND perf_rating_adjectival_end
                and designation_id = %s
                and perf_rating_adjectival_delete_ind = %s'''
                values = (str(row["Performance Rating"]), str(row["Designation ID"]), False)
                #print(str(row["Performance Rating"]), 'perf_rating')
                #print(str(row["Designation ID"]), 'perfrating_query_designation_srmanagemnt')
                columns = ['perf_rating_adjectival_name']

                dfsqladjectival = securequerydatafromdatabase(sqladjectival, values, columns)
                try:
                    adjectival = dfsqladjectival['perf_rating_adjectival_name'][0]

                except:
                    adjectival = "N/A"
                #print(adjectival, 'adjectival')

                viewcolumn[index] = dbc.Label(children=adjectival)
                #viewcolumn[index] = dbc.Label("Wee")
                #viewcolumn[index] =dbc.Checklist(options=[{"label": "", "value": 1}], value=[])
                #viewcolumn[index] = dbc.Label("Wee")
            else:
                pass

        for index, row in df.iterrows():
            listofids.append("linkid"+str(row["Rating ID"]))
            linkcolumn[index] = html.A(['Edit'], id=str(row["Rating ID"]), href="/settings/settings_perfrating_management_profile?eid="+empid+"&mode=edit&perf_rating_id="+str(row["Rating ID"]))#, href='/servicerecord/query_service_record_profile?eid='+str(row["SR_ID"])+'&mode=edit')

        data_dict = df.to_dict()
        dictionarydata = {'Select': linkcolumn}
        dictionarydata2 = {'Adjectival Rating': viewcolumn}
        data_dict.update(dictionarydata)
        data_dict.update(dictionarydata2)
        df = pd.DataFrame.from_dict(data_dict)
        df = df[["Start Period", "End Period", "Unit Name", "Designation", "Performance Rating", "Adjectival Rating", "Select"]]
        table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

        return [table]

    else:
        raise PreventUpdate


