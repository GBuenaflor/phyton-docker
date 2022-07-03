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


def hash_string(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()


layout = html.Div([
    commonmodules.get_header(),
    commonmodules.get_menu(),
    commonmodules.get_common_variables(),
    html.H1("Appointment Offices Data Entry"),
    html.Hr(),
    html.Div([
        dbc.Card([
            dbc.CardHeader(
                html.H4("Appointment Offices"),
                style={"background-color": "rgb(123,20,24)", 'color': 'white'}
            ),
            dbc.CardBody([
                # dbc.Row([
                #     dbc.Col([
                #         dcc.Markdown('''NOTE: This module displays administrative offices that appear on appointment papers.''',
                #                      style={'font-style': 'italic'})
                #     ])
                # ]),
                dbc.Row([
                    dbc.Col([
                        html.H5(
                            "This module displays administrative offices that appear on appointment papers. Only add an office if the office appears officially in an appointment paper.", style={'font-style': 'italic'})
                    ])
                ]),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        dbc.Button("Add New Appointment Office", id="btnaddnewappointmentoffice", color="primary",
                                   href='/settings/settings_appointment_offices_profile?&mode=add'),  # block=True
                    ]),
                    dbc.Col([
                        dbc.FormGroup(
                            [
                                dbc.Label("Search Appointment Office", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Input(
                                        type="text", id="sappointmentoffice", placeholder="Enter search string"
                                    ),

                                ],
                                    width=8
                                )
                            ],
                            row=True
                        ),
                    ]),

                ]),
                html.Hr(),
                html.H4("Existing Appointment Offices"),

                html.Div([

                ], id="editappointmentofficedatatable"),

                dbc.Col([

                        html.Div([
                            dcc.Input(id='appointmentofficesubmitstatus', type='text', value="0")
                        ], style={'display': 'none'}),
                        html.Div([
                            dcc.Input(id='appointmentofficeid', type='text', value="0")
                        ], style={'display': 'none'}),

                        ], width=2
                        )
            ], style={'line-height': "1em", "display": "block"}),
        ], style={'line-height': "1em", "display": "block"}
        )
    ]),
])


@app.callback([Output('editappointmentofficedatatable', 'children')
               ],
              [
    Input('sappointmentoffice', 'value'),
    Input('appointmentofficesubmitstatus', 'value'),
],
    [
],)
def querymodulesfordtcall(sappointmentoffice, appointmentofficesubmitstatus):
    if sappointmentoffice:
        sappointmentoffice = "%"+sappointmentoffice+"%"
        sqlcommand = """SELECT office_id, office_name, office_trunkline, office_telefax, office_email, office_website,
                        	   office_direct_line, design.designation_name || ' - ' || unn.unit_name AS "Admin Position"
                          FROM appointment_offices ao
                        INNER JOIN admin_positions ap ON ap.admin_pos_id = ao.admin_pos_id
                        INNER JOIN designations design ON design.designation_id = ap.admin_designation_id
                        LEFT JOIN units un ON un.unit_id = ao.office_unit_id
                        INNER JOIN units unn ON unn.unit_id = ap.admin_pos_unit_id
                          WHERE ao.office_delete_ind = %s
                            AND unn.unit_delete_ind = %s
                        	AND ap.admin_pos_delete_ind = %s
                            AND ao.office_name ILIKE %s
                        ORDER BY office_name ASC
                     """
        values = (False, False, False, sappointmentoffice,)
    else:
        sqlcommand = """SELECT office_id, office_name, office_trunkline, office_telefax, office_email, office_website,
                        	   office_direct_line, design.designation_name || ' - ' || unn.unit_name AS "Admin Position"
                          FROM appointment_offices ao
                        INNER JOIN admin_positions ap ON ap.admin_pos_id = ao.admin_pos_id
                        INNER JOIN designations design ON design.designation_id = ap.admin_designation_id
                        LEFT JOIN units un ON un.unit_id = ao.office_unit_id
                        INNER JOIN units unn ON unn.unit_id = ap.admin_pos_unit_id
                          WHERE ao.office_delete_ind = %s
                            AND unn.unit_delete_ind = %s
                        	AND ap.admin_pos_delete_ind = %s
                        ORDER BY office_name ASC
                     """
        values = (False, False, False,)
    columns = ["office_id", "office_name", "office_trunkline", "office_telefax", "office_email", "office_website",
               "office_direct_line", "Admin Position"]
    df = securequerydatafromdatabase(sqlcommand, values, columns)
    df.columns = ["Office ID", "Office Name", "Trunkline", "Telefax",
                  "E-mail", "Website", "Direct Line", "Admin Position Attached"]
    columns = [{"name": i, "id": i} for i in df.columns]
    data = df.to_dict("rows")
    linkcolumn = {}
    for index, row in df.iterrows():
        linkcolumn[index] = dcc.Link(
            'Edit', href='/settings/settings_appointment_offices_profile?appointment_office_id='+str(row["Office ID"])+'&mode=edit')
    data_dict = df.to_dict()
    dictionarydata = {'Select': linkcolumn}
    data_dict.update(dictionarydata)
    df = pd.DataFrame.from_dict(data_dict)
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
    return [table]
