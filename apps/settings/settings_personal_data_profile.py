import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash
import re
import json
from dash.dependencies import Input, Output, State, ALL
from apps import commonmodules
from dash.exceptions import PreventUpdate
from app import app
from apps import home
from apps.dbconnect import securequerydatafromdatabase, modifydatabase, modifydatabasereturnid, bulkmodifydatabase
import hashlib
from datetime import datetime
import dash_table
import pandas as pd
import numpy as np
from datetime import date as date
import urllib.parse as urlparse
from urllib.parse import parse_qs
from apps.commonmodules import safeupper, checkiflengthzero2, checkiflengthx2, checkstyle2, ispersonexisting


#### MAIN #####


layout = html.Div([
    commonmodules.get_header(),
    commonmodules.get_menu(),
    commonmodules.get_common_variables(),
    dcc.Store(id='sessiondegrees', storage_type='memory', data=[]),
    dcc.Store(id='sessiondegreesprocessed', storage_type='memory', data=[]),
    dcc.Store(id='sessioneligibilities', storage_type='memory', data=[]),
    dcc.Store(id='sessioneligibilitiesprocessed', storage_type='memory', data=[]),
    dcc.Store(id='sessionpersonid', storage_type='memory', data=[]),
    dcc.Store(id='sessionpersoneducid', storage_type='memory', data=[]),
    dcc.Store(id='sessionpersoneligibilitiescid', storage_type='memory', data=[]),

    html.H1("Create New Personal Data Entry", style={
        "display": "none"}, id="pds_createheader"),
    html.H1("Edit Personal Data", style={"display": "none"}, id="pds_editheader"),
    dcc.Link('← Back to List of Personal Data Entries',
             href='/settings/settings_personal_data'),

    html.Div([


        dbc.FormGroup(
            dbc.FormText(["*Required"]
                         )
        ),
        html.Hr(),

        dbc.Form([

            dbc.Card([

                dbc.CardHeader(
                    html.H4("Personal Data"),
                    style={"background-color": "rgb(123,20,24)", 'color': 'white'}
                ),

                html.Br(),

                dcc.Loading([
                    dbc.CardBody([

                        html.Div([
                            dbc.Row([
                                dbc.Col([
                                    # dbc.Switch(label = "Add Employee Number", id = 'pds_addempnum', value = False)
                                    dbc.Checklist(
                                        options=[
                                            {"label": "Add Employee Number", "value": 1},
                                        ],
                                        value=[],
                                        id="pds_addempnum",
                                        inline=True,
                                        switch=True,
                                    ),

                                ]),

                            ]),
                            html.Br(),
                            dbc.Collapse([
                                dbc.Row([
                                    dbc.Col([
                                        dbc.FormGroup([
                                            dbc.Label("Employee Number", width=4,
                                                      style={"text-align": "left"}),
                                            dbc.Col([
                                                dbc.Input(
                                                    type="text", id="pds_empnum", placeholder="Enter employee number"
                                                ),
                                                dbc.FormFeedback(
                                                    "Please enter 9-digit employee number", valid=False)
                                            ], width=8)
                                        ], row=True),
                                    ]),
                                    dbc.Col([

                                    ]),
                                    dbc.Col([

                                    ]),
                                ]),
                            ], 'pds_empnum_input_collapse', is_open = False),
                            html.Br(),
                        ], id = 'pds_addempnum_div', style = {'display':'none'}),



                        dbc.Row([
                            dbc.Col([
                                html.H4("Personal Information")
                            ]),
                            dbc.Col([

                            ]),

                        ]),

                        html.Br(),

                        dbc.Row([
                            dbc.Col([
                                dbc.FormGroup([
                                    # dbc.Col([
                                    dbc.Label("Select Temporary Unit (* for New)", width=4, id='pds_tempunitlabel',
                                              style={"text-align": "left"}),
                                    # ],id = 'pds_tempunitdiv1', style = {'display':'none'}),

                                    # dbc.Col([
                                    #     dbc.Label("Select Temporary Unit", width=4, style={"text-align": "left"}),
                                    # ],id = 'pds_tempunitdiv2', style = {'display':'none'}),

                                    dbc.Col([
                                        dcc.Dropdown(
                                            id='pds_temp_unit',

                                            placeholder="Please select temporary unit",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),

                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Select Title*", width=4, id='pds_titlelabel',
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dcc.Dropdown(
                                            id='pds_title',

                                            placeholder="Please select title",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Active/Inactive?*", width=4, id='pds_isactivelabel',
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dcc.Dropdown(
                                            id='pds_isactive',
                                            options=[
                                                {'label': 'Active', 'value': True},
                                                {'label': 'Inactive', 'value': False},
                                                # {'label': 'Research and Extension Professional Staff (REPS)', 'value': '3'},
                                                # {'label': 'Others', 'value': '11'}
                                            ],
                                            placeholder="Please indicate if active or inactive",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                        ]),



                        dbc.Row([
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Last Name*", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Input(
                                            type="text", id="pds_lastname", placeholder="Enter last name"
                                        ),
                                        dbc.FormFeedback(
                                            "Please enter last name", valid=False)
                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("First Name*", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Input(
                                            type="text", id="pds_firstname", placeholder="Enter first name"
                                        ),
                                        dbc.FormFeedback(
                                            "Please enter first name", valid=False)
                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Middle Name", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Input(
                                            type="text", id="pds_middlename", placeholder="Enter middle name"
                                        ),
                                        dbc.FormFeedback(
                                            "Please enter middle name", valid=False)
                                    ], width=8)
                                ], row=True),
                            ]),
                        ]),

                        dbc.Row([
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Name Suffix", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Input(
                                            type="text", id="pds_suffixname", placeholder="e.g. SR, JR, III"
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label(
                                        "Date of Birth*", id='pds_doblabel', width=4, style={"text-align": "left", 'color': 'black'}),
                                    dbc.Col([
                                        dcc.DatePickerSingle(id='pds_dob', placeholder="mm/dd/yyyy",
                                                             max_date_allowed=date.today()),
                                        dbc.FormFeedback(
                                            "Please enter valid date", valid=False)
                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                #     dbc.FormGroup([
                                #         dbc.Label("Place of Birth", width=4,
                                #                   style={"text-align": "left"}),
                                #         dbc.Col([
                                #             dbc.Input(
                                #                 type="text", id="pds_pob", placeholder="Enter place of birth"
                                #             ),
                                #             dbc.FormFeedback(
                                #                 "Please enter place of birth", valid=False)
                                #         ], width=8)
                                #     ], row=True),
                            ]),


                        ]),

                        dbc.Row([
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Place of Birth Local?*", width=4,
                                              style={"text-align": "left"}, id='pds_pobislocallabel'),
                                    dbc.Col([
                                        dcc.Dropdown(
                                            id='pds_pobislocal',
                                            options=[
                                                {"label": "Local", "value": 1},
                                                {"label": "Other Country", "value": 2},
                                            ],
                                        )
                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([

                            ], id='pds_pobproxy1'),
                            dbc.Col([

                            ], id='pds_pobproxy2'),



                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label(
                                        "Province of Birth*", width=4, style={"text-align": "left", 'color': 'black'}, id='pds_pobprovincelabel'),
                                    dbc.Col([
                                        dcc.Dropdown(
                                            id='pds_pobprovince',
                                            options=[

                                            ],
                                        ),
                                        dbc.FormFeedback(
                                            "Please enter valid province", valid=False)
                                    ], width=8)
                                ], row=True),
                            ], id='pds_pobproxy3', style={'display': 'none'}),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("City of Birth*", width=4,
                                              style={"text-align": "left"}, id='pds_pobcitylabel'),
                                    dbc.Col([
                                        dcc.Dropdown(
                                            id='pds_pobcity',
                                            options=[

                                            ],
                                        ),
                                        dbc.FormFeedback(
                                            "Please enter valid city", valid=False)
                                    ], width=8)
                                ], row=True),
                            ], id='pds_pobproxy4', style={'display': 'none'}),



                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label(
                                        "Country of Birth*", width=4, style={"text-align": "left", 'color': 'black'}, id='pds_pobcountrylabel'),
                                    dbc.Col([
                                        dcc.Dropdown(
                                            id='pds_pobcountry',
                                            options=[

                                            ],
                                        ),

                                        dbc.FormFeedback(
                                            "Please enter valid country", valid=False)
                                    ], width=8)
                                ], row=True),
                            ], id='pds_pobproxy5', style={'display': 'none'}),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("City of Birth*", width=4,
                                              style={"text-align": "left"}, id='pds_poblabel'),
                                    dbc.Col([
                                        dbc.Input(
                                            type="text", id="pds_pob", placeholder="Enter place of birth"
                                        ),

                                        dbc.FormFeedback(
                                            "Please enter place of birth", valid=False)
                                    ], width=8)
                                ], row=True),
                            ], id='pds_pobproxy6', style={'display': 'none'}),


                        ]),



                        dbc.Row([
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label(
                                        "Sex at Birth*", id='pds_sexatbirthlabel', width=4, style={"text-align": "left", 'color': 'black'}),
                                    dbc.Col([
                                        dcc.Dropdown(
                                            id='pds_sexatbirth',
                                            options=[
                                                {"label": "Male", "value": 1},
                                                {"label": "Female", "value": 2},
                                            ],

                                            placeholder="Please select sex assigned at birth",
                                        ),
                                        dbc.FormFeedback(
                                            "Please select sex assigned at birth", valid=False)
                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label(
                                        "Civil Status*", id='pds_civilstatuslabel', width=4, style={"text-align": "left", 'color': 'black'}),

                                    dbc.Col([
                                            dcc.Dropdown(
                                                id='pds_civilstatus',
                                                options=[
                                                ],

                                                placeholder="Please select civil status",
                                            ),
                                            dbc.FormFeedback(
                                                "Please select civil status", valid=False)
                                            ], width=8)
                                ], row=True),

                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Blood Type*", id='pds_bloodtypelabel', width=4,
                                              style={"text-align": "left"}),

                                    dbc.Col([
                                            dcc.Dropdown(
                                                id='pds_bloodtype',
                                                options=[
                                                ],

                                                placeholder="Select blood type",
                                            ),
                                            dbc.FormFeedback(
                                                "Please select blood type", valid=False)
                                            ], width=8)

                                ], row=True),
                            ]),
                        ]),
                        dbc.Row([

                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Mobile Number", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Input(
                                            type="text", id="pds_mobilecontactnumber", placeholder="Enter mobile phone"
                                        ),
                                        dbc.FormFeedback(
                                            "Please enter valid mobile phone", valid=False)
                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Landline Number", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Input(
                                            type="text", id="pds_lanecontactnumber", placeholder="Enter valid landline"
                                        ),
                                        dbc.FormFeedback(
                                            "Please enter landline number", valid=False)
                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Email Address*", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Input(
                                            type="text", id="pds_email", placeholder="Enter email"
                                        ),
                                        dbc.FormFeedback(
                                            "Please enter valid email", valid=False)
                                    ], width=8)
                                ], row=True),
                            ]),
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label(
                                        "Citizenship*", id='pds_citizenshiplabel', width=4, style={"text-align": "left", 'color': 'black'}),
                                    dbc.Col([
                                        dcc.Dropdown(
                                            id='pds_citizenship',
                                            options=[
                                                {"label": "Filipino", "value": 1},
                                                {"label": "Foreign", "value": 2},
                                                {"label": "Dual Filipino Citizenship", "value": 3},
                                            ],
                                            value=1,
                                            placeholder="Please select citizenship",
                                        ),
                                        dbc.FormFeedback(
                                            "Please enter valid date", valid=False)
                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Type of Citizenship", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dcc.Dropdown(
                                            id='pds_typeofcit',
                                            options=[
                                                {"label": "By Birth", "value": 1},
                                                {"label": "By Naturalization", "value": 2},
                                            ],

                                            placeholder="Please select citizenship type",
                                        ),
                                        dbc.FormFeedback(
                                            "Please enter place of birth", valid=False)
                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                html.Div([
                                    dbc.FormGroup([
                                        dbc.Label("Country of Foreign Citizenship",
                                                  width=4, style={"text-align": "left"}),
                                        dbc.Col([
                                            dbc.Spinner([
                                                dcc.Dropdown(
                                                    id='pds_countryofcit',
                                                    options=[

                                                    ],

                                                    placeholder="Please select country of citizenship",
                                                ),
                                                dbc.FormFeedback(
                                                    "Please select country of citizenship", valid=False)
                                            ]),
                                        ], width=8)
                                    ], row=True),
                                ], id="pds_divforeigncit", style={'display': 'none'})

                            ]),
                        ]),

                        html.Hr(),
                        dbc.Spinner([
                                    dbc.Row([
                                        dbc.Col([
                                            html.H4("Current Address*")
                                        ]),
                                        dbc.Col([

                                        ]),

                                    ]),
                                    html.Br(),
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.FormGroup([

                                                dbc.Label("Country*", id='pds_addcountrycurrlabel', width=4,
                                                          style={"text-align": "left"}),
                                                dbc.Col([

                                                    dcc.Dropdown(
                                                        id='pds_addcountrycurr',
                                                        options=[

                                                        ],
                                                        value=168,
                                                        clearable=False,
                                                        placeholder="Please select current country address",
                                                    ),
                                                    dbc.FormFeedback(
                                                        "Please select country", valid=False)

                                                ], width=8)

                                            ], row=True),
                                        ]),

                                        dbc.Col([

                                        ], id='pds_pobproxy1curr'),


                                        dbc.Col([
                                            dbc.FormGroup([
                                                dbc.Label(
                                                    "Region*", id='pds_regioncurrlabel', width=4, style={"text-align": "left", 'color': 'black'}),
                                                dbc.Col([

                                                    dcc.Dropdown(
                                                        id='pds_regioncurr',
                                                        options=[

                                                        ],

                                                        placeholder="Please select current country address",
                                                    ),
                                                    dbc.FormFeedback(
                                                        "Please enter current region", valid=False)

                                                ], width=8)
                                            ], row=True),
                                        ], id='div_region'),


                                    ]),

                                    dbc.Row([
                                        dbc.Col([
                                            dbc.FormGroup([
                                                dbc.Label(
                                                    "Province*", width=4, id='pds_aprovincecurrlabel', style={"text-align": "left", 'color': 'black'}),

                                                dbc.Col([
                                                    dbc.Spinner([
                                                        dcc.Dropdown(
                                                            id='pds_aprovincecurr',
                                                            options=[
                                                            ],
                                                            placeholder="Please select current province address",
                                                        ),
                                                        dbc.FormFeedback(
                                                            "Please enter province.", valid=False)
                                                    ]),
                                                ], width=8)
                                            ], row=True),
                                        ], id='div_prov'),
                                        dbc.Col([
                                            dbc.FormGroup([
                                                dbc.Label(
                                                    "City/Municipality*", width=4, id='pds_citymuncurrentlabel', style={"text-align": "left", 'color': 'black'}),
                                                dbc.Col([
                                                    dbc.Spinner([
                                                        dcc.Dropdown(
                                                            id='pds_citymuncurrent',
                                                            options=[
                                                            ],
                                                            placeholder="Select city/municipality name",
                                                        ),
                                                        dbc.FormFeedback(
                                                            "Please enter city.", valid=False)
                                                    ]),
                                                ], width=8)
                                            ], row=True),
                                        ], id='div_city'),
                                    ]),


                                    dbc.Row([
                                        dbc.Col([
                                            dbc.FormGroup([
                                                dbc.Label("House Number, Street Address*",
                                                          width=4, style={"text-align": "left"}),
                                                dbc.Col([
                                                    dbc.Input(
                                                        type="text", id="pds_streetaddresscurr", placeholder="Enter house and street address"
                                                    ),
                                                    dbc.FormFeedback(
                                                        "Please enter house and street address", valid=False)
                                                ], width=8)
                                            ], row=True),
                                        ]),
                                        dbc.Col([
                                            dbc.FormGroup([
                                                dbc.Label("Subdivision/Village", width=4,
                                                          style={"text-align": "left"}),
                                                dbc.Col([
                                                    dbc.Input(
                                                        type="text", id="pds_subdvillagecurr", placeholder="Enter subdivision/village name"
                                                    ),
                                                    dbc.FormFeedback(
                                                        "Please enter subdivision/village name", valid=False)
                                                ], width=8)
                                            ], row=True),
                                        ]),

                                    ]),
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.FormGroup([
                                                dbc.Label("Barangay*", width=4,
                                                          style={"text-align": "left"}),
                                                dbc.Col([
                                                    dbc.Input(
                                                        type="text", id="pds_brgyaddresscurr", placeholder="Enter brgy name"
                                                    ),
                                                    dbc.FormFeedback(
                                                        "Please enter barangay.", valid=False)
                                                ], width=8)
                                            ], row=True),
                                        ]),
                                        dbc.Col([
                                            dbc.FormGroup([
                                                dbc.Label("Zip Code*", width=4,
                                                          style={"text-align": "left"}),
                                                dbc.Col([
                                                    dbc.Input(
                                                        type="text", id="pds_zipcodecurr", placeholder="Enter zip code"
                                                    ),
                                                    dbc.FormFeedback(
                                                        "Please enter zip code.", valid=False)
                                                ], width=8)
                                            ], row=True),
                                        ]),
                                    ]),
                                    html.Hr(),

                                    dbc.Row([
                                        dbc.Col([
                                            html.H4("Permanent Address*"),
                                        ]),
                                        dbc.Col([
                                            dbc.FormGroup([
                                                dbc.Checkbox(
                                                    id="pds_permsameascurrent", className="form-check-input", checked=False
                                                ),
                                                dbc.Label(
                                                    "Same as current address",
                                                    html_for="standalone-checkbox",
                                                    className="form-check-label",
                                                )
                                            ], check=True),
                                        ]),
                                    ]),
                                    html.Br(),
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.FormGroup([
                                                dbc.Label("Country*", id='pds_addcountrypermlabel', width=4,
                                                          style={"text-align": "left"}),
                                                dbc.Col([
                                                    dcc.Dropdown(
                                                        id='pds_addcountryperm',
                                                        options=[

                                                        ],
                                                        value=168,
                                                        clearable=False,
                                                        placeholder="Please select permanent country address",
                                                    ),
                                                    dbc.FormFeedback(
                                                        "Please select country", valid=False)
                                                ], width=8)
                                            ], row=True),
                                        ]),
                                        dbc.Col([

                                        ], id='pds_pobproxy1perm'),

                                        dbc.Col([
                                            dbc.FormGroup([
                                                dbc.Label(
                                                    "Region*", width=4, style={"text-align": "left", 'color': 'black'}, id='pds_regionpermlabel'),
                                                dbc.Col([
                                                    dcc.Dropdown(
                                                        id='pds_regionperm',
                                                        options=[

                                                        ],

                                                        placeholder="Please select permanent region",
                                                    ),
                                                    dbc.FormFeedback(
                                                        "Please enter permanent region", valid=False)
                                                ], width=8)
                                            ], row=True),
                                        ], id="div_regionperm"),


                                    ]),

                                    dbc.Row([
                                        dbc.Col([
                                            dbc.FormGroup([
                                                dbc.Label(
                                                    "Province*", width=4, style={"text-align": "left", 'color': 'black'}, id='pds_aprovincepermlabel'),
                                                dbc.Col([
                                                    dcc.Dropdown(
                                                        id='pds_aprovinceperm',
                                                        options=[
                                                        ],
                                                        placeholder="Please select permanent province address",
                                                    ),
                                                    dbc.FormFeedback(
                                                        "Please enter province.", valid=False)
                                                ], width=8)
                                            ], row=True),
                                        ], id="div_provperm"),
                                        dbc.Col([
                                            dbc.FormGroup([
                                                dbc.Label(
                                                    "City/Municipality*", width=4, style={"text-align": "left", 'color': 'black'}, id='pds_citymunpermlabel'),
                                                dbc.Col([
                                                    dcc.Dropdown(
                                                        id='pds_citymunperm',
                                                        options=[
                                                        ],
                                                        placeholder="Select city/municipality name",
                                                    ),
                                                    dbc.FormFeedback(
                                                        "Please enter city/municipality.", valid=False)
                                                ], width=8)
                                            ], row=True),
                                        ], id="div_cityperm"),
                                    ]),


                                    dbc.Row([
                                        dbc.Col([
                                            dbc.FormGroup([
                                                dbc.Label("House Number, Street Address*",
                                                          width=4, style={"text-align": "left"}),
                                                dbc.Col([
                                                    dbc.Input(
                                                        type="text", id="pds_streetaddressperm", placeholder="Enter house and street address"
                                                    ),
                                                    dbc.FormFeedback(
                                                        "Please enter house and street address", valid=False)
                                                ], width=8)
                                            ], row=True),
                                        ]),
                                        dbc.Col([
                                            dbc.FormGroup([
                                                dbc.Label("Subdivision/Village", width=4,
                                                          style={"text-align": "left"}),
                                                dbc.Col([
                                                    dbc.Input(
                                                        type="text", id="pds_subdvillageperm", placeholder="Enter subdivision/village name"
                                                    ),
                                                    dbc.FormFeedback(
                                                        "Please enter subdivision/village name", valid=False)
                                                ], width=8)
                                            ], row=True),
                                        ]),

                                    ]),
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.FormGroup([
                                                dbc.Label("Barangay*", width=4,
                                                          style={"text-align": "left"}),
                                                dbc.Col([
                                                    dbc.Input(
                                                        type="text", id="pds_brgyaddressperm", placeholder="Enter brgy name"
                                                    ),
                                                    dbc.FormFeedback(
                                                        "Please enter barangay.", valid=False)
                                                ], width=8)
                                            ], row=True),
                                        ]),
                                        dbc.Col([
                                            dbc.FormGroup([
                                                dbc.Label("Zip Code*", width=4,
                                                          style={"text-align": "left"}),
                                                dbc.Col([
                                                    dbc.Input(
                                                        type="text", id="pds_zipcodeperm", placeholder="Enter zip code"
                                                    ),
                                                    dbc.FormFeedback(
                                                        "Please enter zip code.", valid=False)
                                                ], width=8)
                                            ], row=True),
                                        ]),
                                    ]),
                                    ]),
                        html.Hr(),
                        dbc.Row([
                            dbc.Col([
                                html.H4("Government Identification Numbers")
                            ]),
                            dbc.Col([

                            ]),

                        ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("GSIS BP No.*", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Input(
                                            type="text", id="pds_gsis", placeholder="Enter GSIS number"
                                        ),
                                        dbc.FormFeedback(
                                            "Please enter valid GSIS Number", valid=False)
                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("PAG-IBIG ID No.", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Input(
                                            type="text", id="pds_pagibig", placeholder="Enter PAG-IBIG No."
                                        ),
                                        dbc.FormFeedback(
                                            "Please enter  PAG-IBIG No.", valid=False)
                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Philhealth No.", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Input(
                                            type="text", id="pds_philhealth", placeholder="Enter Philhealth number"
                                        ),
                                        dbc.FormFeedback(
                                            "Please enter Philhealth number", valid=False)
                                    ], width=8)
                                ], row=True),
                            ]),
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("SSS No.", width=4, style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Input(
                                            type="text", id="pds_sss", placeholder="Enter SSS number"
                                        ),
                                        dbc.FormFeedback(
                                            "Please enter valid SSS Number", valid=False)
                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("TIN", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Input(
                                            type="text", id="pds_tin", placeholder="Enter TIN."
                                        ),
                                        dbc.FormFeedback("Please enter 12 digit TIN.", valid=False)
                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([

                            ]),
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Government ID", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dcc.Dropdown(
                                            id='pds_governmentid',
                                            options=[
                                                {"label": "Driver's License", "value": 1},
                                                {"label": "Passport", "value": 2},
                                                {"label": "UMID", "value": 3},
                                                {"label": "PRC ID", "value": 4},
                                            ],

                                            placeholder="Please select Government ID",
                                        ),
                                        dbc.FormFeedback(
                                            "Please select sample government ID", valid=False)
                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Government ID #", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Input(
                                            type="text", id="pds_govidnumber", placeholder="Enter ID number of Government ID Selected"
                                        ),
                                        dbc.FormFeedback(
                                            "Please enter ID number of Government ID Selected.", valid=False)
                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([

                            ]),
                        ]),

                        html.Hr(),
                        html.Div([
                            dbc.Row([
                                dbc.Col([
                                    html.H4("Degrees Earned*", id='pds_degreeslabel')
                                ]),
                                dbc.Col([

                                ]),

                            ]),
                            html.Br(),
                            html.Div([
                                dbc.Button("Add Degree", color="primary", className="mr-1",
                                           id="pds_btn_add_degree"),
                            ], style={"width": "32%", "verticalAlign": "top", "display": "inline-block", "margin-right": "1%"}),
                            html.Div([

                            ], style={"width": "32%", "verticalAlign": "top", "display": "inline-block", "margin-right": "1%"}),
                            html.Div([
                                dbc.Button("Delete Selected Degree", color="primary", className="mr-1",
                                           id="pds_btn_delete_degree"),
                            ], style={"width": "32%", "verticalAlign": "top", "display": "inline-block", "margin-right": "1%", 'display':'none'}),

                            html.Br(),
                            html.Br(),

                            dbc.Modal(
                                [
                                    dbc.ModalHeader(
                                        "Add a Degree"),
                                    dbc.ModalBody([
                                        html.Br(),
                                        html.Div([
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.FormGroup([
                                                        html.Div([
                                                            dbc.Label("Please input all required fields", width=12, style={
                                                                      "text-align": "left", "color": "red"}),
                                                        ], id='pds_degreevalidationtext')

                                                    ], row=True),
                                                ]),
                                            ]),

                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.FormGroup([
                                                        dbc.Label("Degree*", width=4, style={
                                                            "text-align": "left"}),
                                                        dbc.Col([
                                                            dcc.Dropdown(
                                                                id='pds_degree',
                                                                options=[
                                                                ],
                                                                placeholder="Please select degree",
                                                            ),
                                                            dbc.FormFeedback(
                                                                "Please select sample government ID", valid=False)
                                                        ], width=8)
                                                    ], row=True),
                                                ]),
                                                dbc.Col([
                                                    dbc.FormGroup([
                                                        dbc.Label("Program*", width=4,
                                                                  style={"text-align": "left"}),
                                                        dbc.Col([
                                                            dcc.Dropdown(
                                                                id='pds_program',
                                                                options=[
                                                                    {"label": "Program 1",
                                                                     "value": "1"},
                                                                    {"label": "Program 2",
                                                                     "value": "2"},
                                                                    {"label": "Program 3",
                                                                     "value": "3"}
                                                                ],

                                                                placeholder="Please select program",
                                                            ),
                                                            dbc.FormFeedback(
                                                                "Please enter ID number of Government ID Selected.", valid=False)
                                                        ], width=8)
                                                    ], row=True),
                                                ]),

                                            ]),
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.FormGroup([
                                                        dbc.Label("Institution*", width=2,
                                                                  style={"text-align": "left"}),
                                                        dbc.Col([
                                                            dcc.Dropdown(
                                                                id='pds_institution',
                                                                options=[
                                                                    {"label": "Institution 1",
                                                                     "value": "1"},
                                                                    {"label": "Institution 2",
                                                                     "value": "2"},
                                                                    {"label": "Institution 3",
                                                                     "value": "3"}
                                                                ],
                                                                #style={"width":"100%",'display': 'inline-block'},
                                                                # optionHeight=50,
                                                                placeholder="Please select institution",
                                                            ),
                                                            dbc.FormFeedback(
                                                                "Please select institution", valid=False)
                                                        ], width=10)
                                                    ], row=True),
                                                ]),
                                            ]),
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.FormGroup([
                                                        dbc.Label(
                                                            "Date of Graduation", width=4, style={"text-align": "left"}),
                                                        dbc.Col([
                                                            dcc.DatePickerSingle(
                                                                id='pds_educyear', placeholder="mm/dd/yyyy"),
                                                            dbc.FormFeedback(
                                                                "Please enter ID number of Government ID Selected.", valid=False)
                                                        ], width=8)
                                                    ], row=True),
                                                ]),
                                                dbc.Col([
                                                    dbc.FormGroup([
                                                        dbc.Label(
                                                            "General Weighted Average in Course Completed", width=4, style={"text-align": "left"}),
                                                        dbc.Col([
                                                            dbc.Input(
                                                                type="number", id="pds_gwa", placeholder="Enter general weighted average"
                                                            ),
                                                            dbc.FormFeedback(
                                                                "Please select institution", valid=False)
                                                        ], width=8)
                                                    ], row=True),
                                                ]),
                                            ]),
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.FormGroup([
                                                        dbc.Label("Start Date:", width=4,
                                                                  style={"text-align": "left"}),
                                                        dbc.Col([
                                                            dcc.DatePickerSingle(id='pds_startdate', placeholder="mm/dd/yyyy",
                                                                                 #     max_date_allowed=date.today()
                                                                                 ),
                                                            dbc.FormFeedback(
                                                                "Please select start date of program enrollment.", valid=False)
                                                        ], width=8)
                                                    ], row=True),
                                                ]),
                                                dbc.Col([
                                                    dbc.FormGroup([
                                                        dbc.Label("End Date:", width=4,
                                                                  style={"text-align": "left"}),
                                                        dbc.Col([
                                                            dcc.DatePickerSingle(id='pds_enddate', placeholder="mm/dd/yyyy",
                                                                                 # max_date_allowed=date.today()
                                                                                 ),
                                                            dbc.FormFeedback(
                                                                "Please select end date of program enrollment.", valid=False)
                                                        ], width=8)
                                                    ], row=True),
                                                ]),
                                            ]),
                                        ]),

                                        html.Br(),
                                        html.Div([
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.FormGroup([
                                                        dbc.Label(
                                                            "Weighted Average in major course", width=4, style={"text-align": "left"}),
                                                        dbc.Col([
                                                            dbc.Input(
                                                                type="number", id="pds_wamajor", placeholder="Enter weighted average"
                                                            ),
                                                            dbc.FormFeedback(
                                                                "Please select start date of program enrollment.", valid=False)
                                                        ], width=8)
                                                    ], row=True),
                                                ]),
                                                dbc.Col([
                                                    dbc.FormGroup([
                                                        dbc.Label(
                                                            "Number of Failing Marks*", width=4, style={"text-align": "left"}),
                                                        dbc.Col([
                                                            dbc.Input(
                                                                type="number", id="pds_fail", placeholder="Enter number of failing marks", value=0
                                                            ),
                                                            dbc.FormFeedback(
                                                                "Please select end date of program enrollment.", valid=False)
                                                        ], width=8)
                                                    ], row=True),
                                                ]),
                                            ]),


                                        ]),

                                        dbc.Row([
                                            dbc.Col([

                                            ]),
                                            dbc.Col([
                                                dbc.Alert('Please make sure that failing mark/s, if any, are encoded accurately. This data may be crucial in determining the process flow of the Basic Paper.', color = 'danger', )
                                            ])


                                        ]),
                                    ]),
                                    dbc.ModalFooter([
                                        dbc.Button(
                                                    "Save and Close", id="pds_modal_bp_degree_close", style={"float": "left"}, color='primary'),
                                        dbc.Button(
                                            "Cancel", id="pds_modal_bp_degree_cancel", className="ml-auto")
                                    ]),
                                ],
                                id="pds_modal_bp_select_degree",
                                centered=True,
                                backdrop='static',
                                size="xl",
                            )

                        ]),


                        html.Div([

                        ], id="pds_currentdegreediv"),
                        html.Hr(),
                        html.Div([
                            dbc.Row([
                                dbc.Col([
                                    html.H4("Eligibilities*", id='pds_eligibilitieslabel')
                                ]),
                                dbc.Col([

                                ]),

                            ]),

                            html.Div([
                                dbc.FormGroup([
                                    dbc.Checkbox(
                                        id="pds_eligibilities_checkbox", className="form-check-input"
                                    ),
                                    dbc.Label(
                                        "No Required Eligibilities",
                                        html_for="pds_eligibilities_checkbox",
                                        className="form-check-label",
                                    ),
                                ], check=True,),
                            ]),

                            html.Br(),
                            html.Div([
                                dbc.Button("Add Eligibilities", color="primary", className="mr-1",
                                           id="pds_btn_add_eligibilities"),
                            ], style={"width": "32%", "verticalAlign": "top", "display": "inline-block", "margin-right": "1%"}),
                            html.Div([

                            ], style={"width": "32%", "verticalAlign": "top", "display": "inline-block", "margin-right": "1%"}),
                            html.Div([
                                dbc.Button("Delete Selected Eligibilities", color="primary", className="mr-1",
                                           id="pds_btn_delete_eligibilities"),
                            ]
                                # , style={"width": "32%", "verticalAlign": "top", "display": "inline-block", "margin-right": "1%"}
                                , style={"display": "none"}

                            ),

                            dbc.Modal(
                                [
                                    dbc.ModalHeader(
                                        "Add an Eligibility"),
                                    dbc.ModalBody([
                                        html.Br(),
                                        html.Div([
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.FormGroup([
                                                        dbc.Label("Select Eligibility", width=4, style={
                                                            "text-align": "left"}),
                                                        dbc.Col([
                                                            dcc.Dropdown(
                                                                id='pds_eligibility',
                                                                options=[
                                                                ],
                                                                placeholder="Please select eligibility",
                                                            ),
                                                            dbc.FormFeedback(
                                                                "Please select sample government ID", valid=False)
                                                        ], width=8)
                                                    ], row=True),
                                                ]),
                                                dbc.Col([
                                                    dbc.FormGroup([
                                                        dbc.Label("Rating", width=4, style={
                                                            "text-align": "left"}),
                                                        dbc.Col([
                                                            dbc.Input(
                                                                type="number", id="pds_eligibilityrating", placeholder="Enter rating"
                                                            ),
                                                            dbc.FormFeedback(
                                                                "Please enter rating.", valid=False)
                                                        ], width=8)
                                                    ], row=True),
                                                ]),

                                            ]),
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.FormGroup([
                                                        dbc.Label(
                                                            "Date of Examination/Conferment*", width=4, style={"text-align": "left"}),
                                                        dbc.Col([
                                                            dcc.DatePickerSingle(id='pds_eligibility_date_of_exam', placeholder="mm/dd/yyyy",
                                                                                 max_date_allowed=date.today()),
                                                            dbc.FormFeedback(
                                                                "Please select institution", valid=False)
                                                        ], width=8)
                                                    ], row=True),
                                                ]),
                                            ]),
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.FormGroup([
                                                        dbc.Label("Place of Conferment", width=4, style={
                                                            "text-align": "left"}),
                                                        dbc.Col([
                                                            dbc.Input(
                                                                type="text", id="pds_placeofconferment", placeholder="Enter place of conferment."
                                                            ),

                                                        ], width=8)
                                                    ], row=True),
                                                ]),
                                                dbc.Col([
                                                    dbc.FormGroup([
                                                        dbc.Label("License Number if Applicable", width=4, style={
                                                            "text-align": "left"}),
                                                        dbc.Col([
                                                            dbc.Input(
                                                                type="number", id="pds_licensenumber", placeholder="Enter license number"
                                                            ),

                                                        ], width=8)
                                                    ], row=True),
                                                ]),
                                            ]),
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.FormGroup([
                                                        dbc.Label(
                                                            "Start Date of Eligibility:", width=4, style={"text-align": "left"}),
                                                        dbc.Col([
                                                            dcc.DatePickerSingle(id='pds_eligibilitystartdate', placeholder="mm/dd/yyyy",
                                                                                 #     max_date_allowed=date.today()
                                                                                 ),

                                                        ], width=8)
                                                    ], row=True),
                                                ]),
                                                dbc.Col([
                                                    dbc.FormGroup([
                                                        dbc.Label(
                                                            "End Date of Eligibility:", width=4, style={"text-align": "left"}),
                                                        dbc.Col([
                                                            dcc.DatePickerSingle(id='pds_eligibilityenddate', placeholder="mm/dd/yyyy",
                                                                                 # max_date_allowed=date.today()
                                                                                 ),

                                                        ], width=8)
                                                    ], row=True),
                                                ]),
                                            ]),
                                        ]),


                                    ]),
                                    dbc.ModalFooter([
                                        dbc.Button(
                                                    "Save and Close", id="pds_modal_bp_eligibility_close", style={"float": "left"}, color='primary'),
                                        dbc.Button(
                                            "Cancel", id="modal_bp_eligibility_cancel", className="ml-auto")
                                    ]),
                                ],
                                id="pds_modal_bp_select_eligibility",
                                centered=True,
                                backdrop='static',
                                size="xl",
                            )

                        ]),
                        html.Br(),
                        html.Div([

                        ], id="pds_currenteligibilitiesdiv"),
                        html.Hr(),

                        html.Br(),

                    ]),
                ]),
            ], className='border-dark'),

            ###

            html.Br(),
            html.Br(),

            dbc.Button("Show Old Values", color="info", className="mr-1", id="pds_oldvaluesbtn"),

            html.Br(),
            html.Br(),

            dbc.Collapse([
                dbc.Card([

                    dbc.CardHeader(
                        html.H4("Old SQL PDS Values"),
                        style={"background-color": "rgb(123,20,24)", 'color': 'white'}
                    ),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.H4("Personal Data")

                            ]),
                            dbc.Col([
                            ]),
                        ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Title", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldtitle",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Sex", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldsex",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Date of Birth", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_olddob",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                        ]),

                        dbc.Row([
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Civil Status", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldcstat",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Citizenship", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldcitizenship",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Blood Type", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldbltype",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                        ]),

                        dbc.Row([
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("TIN", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldtin",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Other Q", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldotherq",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Encode", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldencode",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                        ]),

                        dbc.Row([
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("HRMO", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldhrmo",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("REM", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldrem",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Created At", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldcreatedat",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                        ]),

                        dbc.Row([
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Updated At", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldupdatedat",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Appointment Clean", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldapptclean",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Appointment Remarks", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldapptremarks",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Appointment Name", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldapptname",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Appointment Timestamp", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldtimestamp",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Leaves Clean", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldleaveclean",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                        ]),

                        dbc.Row([
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Leave Remarks", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldleaveremarks",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Leave Name", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldleavename",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Leave Timestamp", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldleavetimestamp",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                        ]),

                        dbc.Row([
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("System Clean", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldsysclean",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("System Remarks", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldsysremarks",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("System Timestamp", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldsystimestamp",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                        ]),

                        dbc.Row([
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Leave Remarks 2", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldleaveremarks2",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Leave Remarks 3", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldleaveremarks3",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Address", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldaddress",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                        ]),

                        dbc.Row([
                            dbc.Col([
                                html.H4("Educational Background")

                            ]),
                            dbc.Col([
                            ]),
                        ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("School", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldwhr",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Degree", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldeduc",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Major", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldmajor",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                        ]),



                        dbc.Row([
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Year Graduated", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldwhn",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                # dbc.FormGroup([
                                #     dbc.Label("Degree", width=4,
                                #               style={"text-align": "left"}),
                                #     dbc.Col([
                                #         dbc.Label(
                                #             children="<null>", id="pds_oldeduc",
                                #         ),
                                #
                                #     ], width=8)
                                # ], row=True),
                            ]),
                            dbc.Col([
                                # dbc.FormGroup([
                                #     dbc.Label("Major", width=4,
                                #               style={"text-align": "left"}),
                                #     dbc.Col([
                                #         dbc.Label(
                                #             children="<null>", id="pds_oldmajor",
                                #         ),
                                #
                                #     ], width=8)
                                # ], row=True),
                            ]),
                        ]),

                        dbc.Row([
                            dbc.Col([
                                html.H4("Eligibilities")

                            ]),
                            dbc.Col([
                            ]),
                        ]),

                        dbc.Row([
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("CSE", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldcse",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("CSE Year", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldcseyear",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                            dbc.Col([
                                dbc.FormGroup([
                                    dbc.Label("Rating", width=4,
                                              style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children="<null>", id="pds_oldrating",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                        ]),


                    ]),

                ], className='border-dark',)
            ], id='pds_oldcollapse'),
            ####

            html.Br(),
            html.Div([
                dcc.Input(id='pds_submit_summary', type='text', value="0")
            ], style={'display': 'none'}),
            html.Div([
                dcc.Input(id='pds_load_bp', type='text', value="0")
            ], style={'display': 'none'}),
            html.Div([
                dcc.Input(id='pds_degrees_summary', type='text', value="0")
            ], style={'display': 'none'}),
            html.Div([
                # dbc.Label('ELIGSUMMARYHERE4'),
                dcc.Input(id='pds_elig_summary', type='text', value="0")
            ], style={'display': 'none'}),
            html.Div([
                dcc.Input(id='pds_educ_id_store', type='text', value="-1")
            ], style={'display': 'none'}),
            html.Div([
                dcc.Input(id='pds_elig_id_store', type='text', value="-1")
            ], style={'display': 'none'}),

            html.Div(
                html.Div(
                    [
                        dbc.Spinner(
                            [
                                dbc.Button("Submit", color="primary", className="mr-1",
                                           id="pds_submitbtn"),
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader(
                                            "Personal Data Entry Submitted", id='pds_modalhead'),
                                        dbc.ModalBody(
                                            "Successfully submitted personal data entry.  ", id='pds_modalbody'),
                                        dbc.ModalFooter(
                                            [dbc.Button("Close and Add New", id="pds_close", className="ml-auto", href="/settings/settings_personal_data"),
                                             dbc.Button("Return to Home", id="pds_closeret", className="ml-auto", href="/home")]
                                        ),
                                    ],
                                    id="pds_resultmodal",
                                    centered=True,
                                    backdrop='static'
                                ),

                            ],
                            color='danger'
                        )
                    ]
                ), style={"width": "auto", "display": "inline-block", "margin-right": "2%"}),
            html.Div(
                html.Div([
                    dbc.Spinner(
                        [
                            dbc.Button("Cancel Editing", color="secondary", className="mr-1",
                                       id="pds_canceleditbutton", href="/settings/settings_personal_data"),
                        ],
                        color='danger'
                    ),
                    # dbc.Modal(
                    #     [
                    #         dbc.ModalHeader(
                    #             "Personal Data Entry Edited"),
                    #         dbc.ModalBody(
                    #             "Successfully edited personal data entry."),
                    #         dbc.ModalFooter(
                    #             [
                    #                 dbc.Button("Back", id="pds_editcloseret", className="ml-auto", href="/settings/settings_personal_data")]
                    #         ),
                    #     ],
                    #     id="pds_editresultmodal",
                    #     centered=True,
                    #     backdrop='static'
                    # ),

                    dbc.Modal(
                        [
                            dbc.ModalHeader(
                                "Personal Data Entry Confirmation"),
                            dbc.ModalBody([
                                dbc.Col([
                                    dbc.Row(dbc.Label("Confirm Data Entry Submission.")),
                                    dbc.Row(dbc.Label('WARNING: Duplicate Entry Detected. An existing personal data entry with the same details already exist. Please consider this moving forward.', color = 'danger', id = 'pds_duplimodalwarning',
                                              style = {'display':'inline'}))
                                ]),
                            ]),
                            dbc.ModalFooter(
                                [
                                    dbc.Button("Confirm", id="pds_confirmsubmitgo",
                                               className="mr-1", color='primary'),
                                    dbc.Button("Back", id="pds_confirmsubmitback",
                                               className="ml-auto")
                                ]
                            ),
                        ],
                        id="pds_confirmsubmitmodal",
                        centered=True,
                        backdrop='static'
                    )
                ]
                ), style={"width": "auto", "display": "inline-block", "margin-right": "2%"}),
            html.Div(html.Div(
                [
                    dbc.Spinner(
                        [
                            dbc.Button("Delete Entry", color="danger", className="mr-1",
                                       id="pds_deletebutton"),
                        ],
                        color='secondary'
                    )
                ]
            ), style={"width": "auto", "display": "inline-block", "margin-right": "2%"}, id='pds_deletebuttondiv'),
            dbc.Modal(
                [
                    dbc.ModalHeader(
                        "Delete Personal Data Entry Confirmation"),
                    dbc.ModalBody(
                        "Are you sure you want to delete Personal Data Entry?"),
                    dbc.ModalFooter(
                        [
                            dbc.Button("Confirm Deletion", id="pds_deletemodalconfirm", className="mr-1",
                                       color='danger'),
                            dbc.Button("Back", id="pds_deletemodalcancel", className="ml-auto")
                        ]
                    ),
                ],
                id="pds_deletemodal",
                centered=True,
                backdrop='static'
            ),

            dbc.Modal(
                [
                    dbc.ModalHeader(
                        "Deletion Confirmation"),
                    dbc.ModalBody(
                        "Personal data entry has been successfully deleted."),
                    dbc.ModalFooter(
                        [

                            dbc.Button("Back to Main Menu", href='/home',
                                       className="mr-1", color='danger'),
                            dbc.Button("Process Another Entry",
                                       href='/settings/settings_personal_data', className="ml-auto")
                        ]
                    ),
                ],
                id="pds_deletemodal2",
                centered=True,
                backdrop='static'
            ),

            dbc.Modal(
                [
                    dbc.ModalHeader(
                        "Duplicate Entry Detected", id='pds_duplimodalhead'),
                    dbc.ModalBody([


                        dbc.Label("Personal data entry has been blocked since an existing entry with the same details has been found. Please contact HRDO if you wish to proceed. Duplicate person details: "),
                        html.Div(id = 'pds_duplimodaldiv'),


                    ],id='pds_duplimodalbody'),
                    dbc.ModalFooter(
                        [dbc.Button("Close", id="pds_duplimodalclose", className="ml-auto",
                                    # href="/settings/settings_personal_data"
                                    ),
                         # dbc.Button("Return to Home", id="pds_closeret", className="ml-auto", href="/home")
                         ]
                    ),
                ],
                id="pds_duplimodal",
                centered=True,
                backdrop='static'
            ),


        ]),

        html.Div([
            dcc.Input(id='pds_valid_status', type='text', value="0")
        ], style={'display': 'none'}),



    ], id="pds_maindiv", style={'display': 'inline'}),
])

@app.callback(
    [
        Output('pds_educ_id_store', 'value')

    ],
    [
        Input('pds_btn_add_degree', 'n_clicks'),
        Input({'type': 'pds_dynamiceducedit', 'index': ALL}, 'n_clicks'),

    ]


)

def storeproxyvalueeducid(pds_btn_add_degree, pds_dynamiceducedit):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == 'pds_btn_add_degree':
            pds_educ_id_store_return_value = -1

        elif "pds_dynamiceducedit" in str(eventid):

            pds_educ_id_store_return_value = json.loads(eventid)["index"]

        return [pds_educ_id_store_return_value]

    else:
        raise PreventUpdate

@app.callback(
    [
        Output('pds_elig_id_store', 'value')

    ],
    [
        Input('pds_btn_add_eligibilities', 'n_clicks'),
        Input({'type': 'pds_dynamiceligedit', 'index': ALL}, 'n_clicks'),

    ]
)

def storeproxyvalueeligid(pds_btn_add_eligibilities, pds_dynamiceligedit):

    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == 'pds_btn_add_eligibilities':

            pds_elig_id_store_return_value = -1
            return [pds_elig_id_store_return_value]
        elif "pds_dynamiceligedit" in str(eventid):


            pds_elig_id_store_return_value = json.loads(eventid)["index"]
            return [pds_elig_id_store_return_value]



    else:
        raise PreventUpdate



@app.callback(
    [
        Output('pds_load_bp', 'value'),
        Output('pds_countryofcit', 'options'),
        Output('pds_institution', 'options'),
        Output('pds_degree', 'options'),
        Output('pds_program', 'options'),

        Output('pds_civilstatus', 'options'),
        Output('pds_addcountrycurr', 'options'),
        Output('pds_addcountryperm', 'options'),
        Output('pds_bloodtype', 'options'),
        Output('pds_regionperm', 'options'),

        Output('pds_governmentid', 'options'),
        Output('pds_eligibility', 'options'),
        Output('pds_regioncurr', 'options'),
        Output('pds_title', 'options'),

        Output('pds_pobprovince', 'options'),
        Output('pds_pobcountry', 'options'),
        Output("pds_temp_unit", "options"),
        Output('pds_deletebuttondiv', 'style'),
        Output('pds_oldvaluesbtn', 'style'),
        Output('pds_editheader', 'style'),
        Output('pds_createheader', 'style'),
        Output('pds_maindiv', 'style'),
        Output('pds_valid_status', 'value'),
        Output('pds_temp_unit', 'disabled'),
        Output('pds_addempnum_div', 'style')

    ],
    [
        Input('url', 'pathname'),

    ],
    [
        State('url', 'search'),
        State('sessioncurrentunit', 'data'),
        State('sessionlistofunits', 'data'),
        State('pds_valid_status', 'value'),
        State('sessioncurrentrole', 'data')
    ],)
def fillindropdowns(path, url, sessioncurrentunit, sessionlistofunits, pds_valid_status, sessioncurrentrole):
    pds_addempnum_div = {'display':'none'}
    pds_temp_unit_disabled = False
    parsed = urlparse.urlparse(url)
    if parse_qs(parsed.query):
        listofallowedunits = tuple(sessionlistofunits[str(sessioncurrentunit)])
        mode = str(parse_qs(parsed.query)['mode'][0])

        if mode == "add":
            pds_deletebuttondiv_style = {"width": "auto", "display": "none", "margin-right": "2%"}
            pds_oldvaluesbtn_style = {"display": "none"}
            pds_editheader_style = {"display": "none"}
            pds_createheader_style = {"display": "block"}
            pds_load_bp = 1
            pds_valid_status = 1
            pdsmaindiv_style = {'display': 'inline'}


            if sessioncurrentrole in [1, 27]:
                pds_addempnum_div = {'display': 'inline'}
            # sqlcommand2 = '''SELECT person_temp_unit_id
            #                                 FROM persons p
            #                                 WHERE p.person_id = %s
            #                             '''
            #
            # values2 = (person_id,)
            # columns2 = ['person_temp_unit_id']
            # df2 = securequerydatafromdatabase(sqlcommand2, values2, columns2)
            #
            # if df2["person_temp_unit_id"][0] in sessionlistofunits[str(sessioncurrentunit)]:
            #
            #     pds_valid_status = 1
            #     pdsmaindiv_style = {'display': 'inline'}
            #
            # else:
            #
            #     pds_valid_status = 0
            #     pdsmaindiv_style = {'display': 'none'}

        else:
            person_id = str(parse_qs(parsed.query)['uid'][0])

            sqlei = '''
                SELECT emp_id
                FROM employees
                WHERE person_id = %s
                AND emp_delete_ind = %s
            '''

            valuesei = (person_id, False)

            columnsei = ['emp_id']

            dfei = securequerydatafromdatabase(sqlei, valuesei, columnsei)

            if not dfei.empty:
                pds_temp_unit_disabled = True


            pds_deletebuttondiv_style = {"width": "auto",
                                         "display": "inline-block", "margin-right": "2%"}
            pds_oldvaluesbtn_style = {"display": "inline"}
            pds_editheader_style = {"display": "block"}
            pds_createheader_style = {"display": "none"}
            pds_load_bp = 2

            sqlcommand = '''SELECT eu.unit_id
                    FROM persons p
                    INNER JOIN employees e ON p.person_id = e.person_id
                    INNER JOIN emp_units eu ON eu.emp_id = e.emp_id
                    WHERE p.person_id = %s
                    AND emp_unit_delete_ind = %s
                    AND emp_unit_is_primary_home_unit = %s
                        '''

            values = (person_id, False, True)
            columns = ['emp_primary_home_unit_id']
            df = securequerydatafromdatabase(sqlcommand, values, columns)


            if not df.empty:

                if df["emp_primary_home_unit_id"][0] in sessionlistofunits[str(sessioncurrentunit)] or sessioncurrentrole in [1]:

                    pds_valid_status = 1
                    pdsmaindiv_style = {'display': 'inline'}

                else:

                    pds_valid_status = 0
                    pdsmaindiv_style = {'display': 'none'}

            else:

                sqlcommand2 = '''SELECT person_temp_unit_id
                                        FROM persons
                                        WHERE person_id = %s
                            '''

                values2 = (person_id,)
                columns2 = ['person_temp_unit_id']
                df2 = securequerydatafromdatabase(sqlcommand2, values2, columns2)

                if df2["person_temp_unit_id"][0] in sessionlistofunits[str(sessioncurrentunit)] or sessioncurrentrole in [1]:
                    pds_valid_status = 1
                    pdsmaindiv_style = {'display': 'inline'}

                else:

                    pds_valid_status = 0
                    pdsmaindiv_style = {'display': 'none'}

        countryoptions = commonmodules.queryfordropdown('''
            SELECT country_name as label, country_id as value
           FROM countries
           WHERE country_delete_ind = %s

           ORDER BY country_name
        ''', (False, ))

        institutions = commonmodules.queryfordropdown('''
            SELECT school_name as label, school_id as value
           FROM schools
           WHERE school_delete_ind = %s
           ORDER BY school_name
        ''', (False, ))

        degrees = commonmodules.queryfordropdown('''
            SELECT degree_name as label, degree_id as value
           FROM degrees
           WHERE degree_delete_ind = %s
           ORDER BY degree_name
        ''', (False, ))

        programs = commonmodules.queryfordropdown('''
            SELECT program_name as label, program_id as value
           FROM programs
           WHERE program_delete_ind = %s
           ORDER BY program_name
        ''', (False, ))

        civilstatuses = commonmodules.queryfordropdown('''
            SELECT civil_status_code as label, civil_status_id as value
           FROM civil_statuses
           WHERE civil_status_delete_ind = %s
           ORDER BY civil_status_code
        ''', (False,))

        regions = commonmodules.queryfordropdown('''
            SELECT region as label, region_id as value
           FROM regions
           WHERE region_delete_ind = %s
           ORDER BY region
        ''', (False,))

        bloodtypes = commonmodules.queryfordropdown('''
            SELECT blood_type as label, blood_type_id as value
           FROM blood_types
           WHERE blood_type_delete_ind = %s
           ORDER BY blood_type
        ''', (False,))

        # plantilla_items = commonmodules.queryfordropdown('''
        #     SELECT plantilla_number as label, plantilla_id as value
        #    FROM plantilla_items
        #    WHERE plantilla_delete_ind = %s
        #    ORDER BY plantilla_number
        # ''', (False,))

        eligibilities = commonmodules.queryfordropdown('''

            SELECT eligibility_code as label, eligibility_id as value
           FROM eligibilities
           WHERE eligibility_delete_ind = %s
           ORDER BY eligibility_code


           ''', (False,))

        pds_governmentid = commonmodules.queryfordropdown('''
            SELECT gov_id_type as label, gov_id_type_id as value
           FROM government_id_types
           WHERE gov_id_type_delete_ind = %s
           ORDER BY gov_id_type

           ''', (False,))

        pdstitles = commonmodules.queryfordropdown('''
           SELECT title as label, title_id as value
           FROM titles
           WHERE title_delete_ind = %s
           ORDER BY title_id

           ''', (False,))

        pds_pobprovinces = commonmodules.queryfordropdown('''
           SELECT prov_name as label, prov_id as value
           FROM provinces
           WHERE prov_delete_ind = %s
           ORDER BY prov_id
          ''', (False,))

        pds_pobcountries = commonmodules.queryfordropdown('''
           SELECT country_name as label, country_id as value
           FROM countries
           WHERE country_delete_ind = %s
           ORDER BY country_name
          ''', (False,))

        listofunits = commonmodules.queryfordropdown('''
            SELECT unit_name as label, unit_id as value
           FROM units
           WHERE unit_delete_ind = %s AND unit_id IN %s
           ORDER BY unit_name
        ''', (False, listofallowedunits))

        if sessioncurrentrole in [1, 27]:
            pds_deletebuttondiv_style = pds_deletebuttondiv_style
        else:
            pds_deletebuttondiv_style = {'display':'none'}

        if sessioncurrentrole in [1, 27]:
            pds_deletebuttondiv_style = pds_deletebuttondiv_style
        else:
            pds_deletebuttondiv_style = {'display':'none'}


        return [pds_load_bp, countryoptions, institutions, degrees, programs,
                # salarygrades,
                civilstatuses, countryoptions, countryoptions, bloodtypes, regions,
                # plantilla_items,
                pds_governmentid, eligibilities, regions, pdstitles,
                pds_pobprovinces, pds_pobcountries, listofunits,
                pds_deletebuttondiv_style, pds_oldvaluesbtn_style,
                pds_editheader_style, pds_createheader_style,
                pdsmaindiv_style, pds_valid_status, pds_temp_unit_disabled, pds_addempnum_div]
    else:
        raise PreventUpdate


@app.callback([
    Output('pds_pobcity', 'options'),

],
    [
    Input('pds_pobprovince', 'value'),
],
)
def toggle_cities_from_provinces_pob(pds_pobprovince):
    if isinstance(pds_pobprovince, int):

        pds_citymuncurrent = commonmodules.queryfordropdown('''
                SELECT city_name as label, city_id as value
               FROM cities
               WHERE city_delete_ind = %s and prov_id = %s
               ORDER BY city_name
            ''', (False, pds_pobprovince))

        return [pds_citymuncurrent]

    else:
        raise PreventUpdate


@app.callback([
    Output('pds_aprovincecurr', 'options')
],
    [
    Input('pds_regioncurr', 'value'),

],
    [
    State('pds_aprovincecurr', 'options')
],)
def toggle_provinces_from_region_temp(bporegioncurr, bpoaprovincecurrops):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'pds_regioncurr' and bporegioncurr:
            bpoaprovincecurrops = commonmodules.queryfordropdown('''
                    SELECT prov_name as label, prov_id as value
                   FROM provinces
                   WHERE prov_delete_ind = %s and region_id = %s
                   ORDER BY prov_name
                ''', (False, bporegioncurr))

            return [bpoaprovincecurrops]

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback([Output('pds_aprovinceperm', 'options'), ],
              [
    Input('pds_regionperm', 'value'),
],
    [
    State('pds_aprovinceperm', 'options'),
],)
def toggle_provinces_from_region_perm(bporegionperm, bpoaprovincepermops):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'pds_regionperm' and bporegionperm:
            bpoaprovincepermops = commonmodules.queryfordropdown('''
                    SELECT prov_name as label, prov_id as value
                   FROM provinces
                   WHERE prov_delete_ind = %s and region_id = %s
                   ORDER BY prov_name
                ''', (False, bporegionperm))

            return [bpoaprovincepermops]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback([
    Output('pds_citymuncurrent', 'options'),

],
    [
    Input('pds_aprovincecurr', 'value'),

],
    [
    State('pds_citymuncurrent', 'options'),

],)
def toggle_cities_from_provinces_temp(bpoaprovincecurr, pds_citymuncurrent):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'pds_aprovincecurr' and bpoaprovincecurr:
            pds_citymuncurrent = commonmodules.queryfordropdown('''
                    SELECT city_name as label, city_id as value
                   FROM cities
                   WHERE city_delete_ind = %s and prov_id = %s
                   ORDER BY city_name
                ''', (False, bpoaprovincecurr))

            return [pds_citymuncurrent]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback([
    Output('pds_citymunperm', 'options')
],
    [

    Input('pds_aprovinceperm', 'value'),
],
    [

    State('pds_citymunperm', 'options')
],)
def toggle_cities_from_provinces_perm(bpoaprovinceperm, pds_citymunperm):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'pds_aprovinceperm' and bpoaprovinceperm:
            pds_citymunperm = commonmodules.queryfordropdown('''
                    SELECT city_name as label, city_id as value
                   FROM cities
                   WHERE city_delete_ind = %s and prov_id = %s
                   ORDER BY city_name
                ''', (False, bpoaprovinceperm))

            return [pds_citymunperm]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback(
    [Output("pds_modal_bp_select_degree", "is_open"),
     Output('pds_currentdegreediv', 'children'),
     Output('sessiondegrees', 'data'),
     Output('sessiondegreesprocessed', 'data'),
     Output('sessionpersoneducid', 'data'),
     Output('pds_degrees_summary', 'value'),
     Output('pds_degreevalidationtext', 'style')
     ],
    [Input("pds_btn_add_degree", "n_clicks"),
     Input({'type': 'pds_dynamiceducedit', 'index': ALL}, 'n_clicks'),
     Input({'type': 'pds_dynamiceducdelete', 'index': ALL}, 'n_clicks'),
     Input("pds_btn_delete_degree", "n_clicks"),
     Input("pds_modal_bp_degree_close", "n_clicks"),
     Input("pds_modal_bp_degree_cancel", "n_clicks"),
     Input('pds_submit_summary', 'value'),
     Input('pds_load_bp', 'value'),
     ],
    [State("pds_modal_bp_select_degree", "is_open"),
     State("pds_degree", "value"),
     State("pds_program", "value"),
     State("pds_educyear", "date"),
     State("pds_institution", "value"),
     State("pds_gwa", "value"),
     State("pds_wamajor", "value"),
     State("pds_fail", "value"),
     State('sessiondegrees', 'data'),
     State("pds_degree", "options"),
     State("pds_program", "options"),
     State("pds_institution", "options"),
     State('sessiondegreesprocessed', 'data'),
     State('pds_currentdegreediv', 'children'),
     State("pds_startdate", "date"),
     State("pds_enddate", "date"),
     State("url", "search"),
     State('sessionpersoneducid', 'data'),
     State("sessionpersonid", 'data'),
     State('current_user_id', 'data'),
     State('pds_educ_id_store', 'value'),
     State('pds_degrees_summary', 'value')



     ],
)
def toggle_modal_degrees(pds_btn_add_degree,
                         pds_dynamiceducedit, pds_dynamiceducdelete,
                         pds_btn_delete_degree, pds_modal_bp_degree_close, pds_modal_bp_degree_cancel, pds_submit_summary, pds_load_bp, is_open,
                         pds_degree, pds_program, pds_educyear, pds_institution,
                         pds_gwa, pds_wamajor, pds_fail, sessiondegrees,
                         pds_degree_ops, pds_program_ops, pds_institution_ops, sessiondegreesprocessed,
                         pds_currentdegreediv, pds_startdate, pds_enddate, url, sessionpersoneducid, person_id, current_user_id, pds_educ_id_store, pds_degrees_summary_state
                         ):
    ctx = dash.callback_context

    if ctx.triggered:

        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if not pds_fail:
            pds_fail = 0

        if eventid == 'pds_btn_add_degree' or "pds_dynamiceducedit" in str(eventid):#Add Degree Button (Open modal)

            df = pd.DataFrame.from_dict(sessiondegreesprocessed, orient='columns')
            # if len(sessiondegreesprocessed) > 0:
            #     df = addcheckboxtocolumn(df)

            editbtncol = {}
            deletebtncol = {}
            for index, row in df.iterrows():
                editbtncol[index] = dbc.Button("Edit", id={'index': index, 'type': 'pds_dynamiceducedit'}, color = 'primary')
                deletebtncol[index] = dbc.Button("Delete", id={'index': index, 'type': 'pds_dynamiceducdelete'}, color = 'primary')
            data_dict = df.to_dict()
            dictionarydata = {'Edit': editbtncol}
            dictionarydata2 = {'Delete': deletebtncol}
            data_dict.update(dictionarydata)
            data_dict.update(dictionarydata2)
            df = pd.DataFrame.from_dict(data_dict)



            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

            if eventid == 'pds_btn_add_degree':
                pds_degrees_summary = -1
            else:
                index = json.loads(eventid)["index"]
                pds_degrees_summary = index


            return [True, table, sessiondegrees, sessiondegreesprocessed, sessionpersoneducid, pds_degrees_summary, {'display': 'none'}]

        elif "pds_dynamiceducdelete" in str(eventid):


            index = json.loads(eventid)["index"]


            del sessiondegreesprocessed[index]
            del sessiondegrees[index]

            df = pd.DataFrame.from_dict(sessiondegreesprocessed, orient='columns')

            editbtncol = {}
            deletebtncol = {}

            for index, row in df.iterrows():

                editbtncol[index] = dbc.Button("Edit", id={'index': index, 'type': 'pds_dynamiceducedit'},
                                               color='primary')
                deletebtncol[index] = dbc.Button("Delete", id={'index': index, 'type': 'pds_dynamiceducdelete'},
                                                 color='primary')
            data_dict = df.to_dict()
            dictionarydata = {'Edit': editbtncol}
            dictionarydata2 = {'Delete': deletebtncol}
            data_dict.update(dictionarydata)
            data_dict.update(dictionarydata2)
            df = pd.DataFrame.from_dict(data_dict)

            # df = pd.DataFrame.from_dict(sessiondegreesprocessed, orient='columns')

            # if len(sessiondegreesprocessed) > 0:
            #     df = addcheckboxtocolumn(df)
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

            return [False, table, sessiondegrees, sessiondegreesprocessed, sessionpersoneducid, pds_degrees_summary_state, {'display': 'none'}]


        #
        # if "pds_dynamiceducedit" in str(eventid):#dynamic edit button
        #
        #     df = pd.DataFrame.from_dict(sessiondegreesprocessed, orient='columns')
        #     if len(sessiondegreesprocessed) > 0:
        #         df = addcheckboxtocolumn(df)
        #     table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
        #     return [True, table, sessiondegrees, sessiondegreesprocessed, sessionpersoneducid, 1, {'display': 'none'}]


        elif eventid in ['pds_modal_bp_degree_close']:#save and close modal

            if pds_degree and pds_program and pds_institution:#degrees validation
                # if pds_degree and pds_program and pds_institution and (float(pds_gwa) >= 0) and (float(pds_fail) >= 0):

                pds_submit_summary = int(pds_submit_summary)

                if pds_educ_id_store == -1:
                    degree = [(i, d) for i, d in enumerate(pds_degree_ops) if pds_degree in d.values()]
                    if degree:
                        degree = degree[0][1]['label']
                    program = [(i, d) for i, d in enumerate(
                        pds_program_ops) if pds_program in d.values()]
                    if program:
                        program = program[0][1]['label']
                    institution = [(i, d) for i, d in enumerate(
                        pds_institution_ops) if pds_institution in d.values()]
                    if institution:
                        institution = institution[0][1]['label']
                    new_row = {'Degree': degree, 'Program': program, 'Graduation Date': pds_educyear, 'Start Date': pds_startdate, 'End Date': pds_enddate,
                               'Institution': institution, "GWA": pds_gwa, "Weighted Average": pds_wamajor, "Number of Failing Marks": pds_fail}
                    sessiondegreesprocessed.append(new_row)
                    new_row_raw = {'Degree': pds_degree, 'Program': pds_program, 'Graduation Date': pds_educyear, 'Start Date': pds_startdate, 'End Date': pds_enddate,
                                   'Institution': pds_institution, "GWA": pds_gwa, "Weighted Average": pds_wamajor, "Number of Failing Marks": pds_fail}
                    sessiondegrees.append(new_row_raw)

                elif pds_educ_id_store >= -1:

                    degree = [(i, d) for i, d in enumerate(pds_degree_ops) if pds_degree in d.values()]
                    if degree:
                        degree = degree[0][1]['label']
                    program = [(i, d) for i, d in enumerate(
                        pds_program_ops) if pds_program in d.values()]
                    if program:
                        program = program[0][1]['label']
                    institution = [(i, d) for i, d in enumerate(
                        pds_institution_ops) if pds_institution in d.values()]
                    if institution:
                        institution = institution[0][1]['label']


                    # new_row = {'Degree': degree, 'Program': program, 'Graduation Date': pds_educyear, 'Start Date': pds_startdate, 'End Date': pds_enddate,
                    #            'Institution': institution, "GWA": pds_gwa, "Weighted Average": pds_wamajor, "Number of Failing Marks": pds_fail}
                    # new_row_raw = {'Degree': pds_degree, 'Program': pds_program, 'Graduation Date': pds_educyear, 'Start Date': pds_startdate, 'End Date': pds_enddate,
                    #                'Institution': pds_institution, "GWA": pds_gwa, "Weighted Average": pds_wamajor, "Number of Failing Marks": pds_fail}

                    if sessiondegrees[pds_educ_id_store].get("Entry ID") is not None:
                        new_row = {'Entry ID': sessiondegrees[pds_educ_id_store].get("Entry ID"), 'Degree': degree, 'Program': program, 'Graduation Date': pds_educyear,
                                   'Start Date': pds_startdate, 'End Date': pds_enddate,
                                   'Institution': institution, "GWA": pds_gwa, "Weighted Average": pds_wamajor,
                                   "Number of Failing Marks": pds_fail}
                        new_row_raw = {'Entry ID': sessiondegrees[pds_educ_id_store].get("Entry ID"), 'Degree': pds_degree, 'Program': pds_program, 'Graduation Date': pds_educyear,
                                       'Start Date': pds_startdate, 'End Date': pds_enddate,
                                       'Institution': pds_institution, "GWA": pds_gwa, "Weighted Average": pds_wamajor,
                                       "Number of Failing Marks": pds_fail}
                    else:
                        new_row = {'Degree': degree, 'Program': program, 'Graduation Date': pds_educyear,
                                   'Start Date': pds_startdate, 'End Date': pds_enddate,
                                   'Institution': institution, "GWA": pds_gwa, "Weighted Average": pds_wamajor,
                                   "Number of Failing Marks": pds_fail}
                        new_row_raw = {'Degree': pds_degree, 'Program': pds_program, 'Graduation Date': pds_educyear,
                                       'Start Date': pds_startdate, 'End Date': pds_enddate,
                                       'Institution': pds_institution, "GWA": pds_gwa, "Weighted Average": pds_wamajor,
                                       "Number of Failing Marks": pds_fail}
                        # new_row["Entry ID"] = sessiondegrees[pds_educ_id_store].get("Entry ID")
                        # new_row_raw["Entry ID"] = sessiondegrees[pds_educ_id_store].get("Entry ID")
                    sessiondegreesprocessed.append(new_row)
                    sessiondegrees.append(new_row_raw)

                    del sessiondegreesprocessed[pds_educ_id_store]
                    del sessiondegrees[pds_educ_id_store]


                    # sessiondegreesprocessed[pds_submit_summary]['Degree'] = degree
                    # sessiondegreesprocessed[pds_submit_summary]['Program'] = program
                    # sessiondegreesprocessed[pds_submit_summary]['Graduation Date'] = pds_educyear
                    # sessiondegreesprocessed[pds_submit_summary]['Start Date'] = pds_startdate
                    # sessiondegreesprocessed[pds_submit_summary]['End Date'] = pds_enddate
                    # sessiondegreesprocessed[pds_submit_summary]['Institution'] = institution
                    # sessiondegreesprocessed[pds_submit_summary]['GWA Date'] = pds_gwa
                    # sessiondegreesprocessed[pds_submit_summary]['Weighted Average'] = pds_wamajor
                    # sessiondegreesprocessed[pds_submit_summary]['Number of Failing Marks'] = pds_fail


                    # new_row_raw = {'Degree': pds_degree, 'Program': pds_program, 'Graduation Date': pds_educyear, 'Start Date': pds_startdate, 'End Date': pds_enddate,
                    #                'Institution': pds_institution, "GWA": pds_gwa, "Weighted Average": pds_wamajor, "Number of Failing Marks": pds_fail}
                    # sessiondegrees.append(new_row_raw)
                    # del sessiondegrees[pds_educ_id_store]

                    # sessiondegrees[pds_submit_summary]['Degree'] = pds_degree
                    # sessiondegrees[pds_submit_summary]['Program'] = pds_program
                    # sessiondegrees[pds_submit_summary]['Graduation Date'] = pds_educyear
                    # sessiondegrees[pds_submit_summary]['Start Date'] = pds_startdate
                    # sessiondegrees[pds_submit_summary]['End Date'] = pds_enddate
                    # sessiondegrees[pds_submit_summary]['Institution'] = pds_institution
                    # sessiondegrees[pds_submit_summary]['GWA Date'] = pds_gwa
                    # sessiondegrees[pds_submit_summary]['Weighted Average'] = pds_wamajor
                    # sessiondegrees[pds_submit_summary]['Number of Failing Marks'] = pds_fail
                    #


                parsed = urlparse.urlparse(url)
                mode = str(parse_qs(parsed.query)['mode'][0])

                # if mode == "edit":
                #
                #     uid = str(parse_qs(parsed.query)['uid'][0])
                #
                #     insertdegrees([new_row_raw], uid, current_user_id)#insert for edit mode
                #     sql = ''' SELECT person_educ_id
                #     FROM basic_papers bp INNER JOIN persons p on p.person_id = bp.person_id
                #     INNER JOIN person_educational_backgrounds peb on peb.person_id = p.person_id
                #     WHERE bp_id = %s  AND person_educ_delete_ind=%s'''
                #     values = (uid, False)
                #     columns = ['person_educ_id']
                #     df = securequerydatafromdatabase(sql, values, columns)
                #     sessionpersoneducid = df['person_educ_id'].to_list()

                df = pd.DataFrame.from_dict(sessiondegreesprocessed, orient='columns')

                editbtncol = {}
                deletebtncol = {}

                for index, row in df.iterrows():
                    editbtncol[index] = dbc.Button("Edit", id={'index': index, 'type': 'pds_dynamiceducedit'},
                                                   color='primary')
                    deletebtncol[index] = dbc.Button("Delete", id={'index': index, 'type': 'pds_dynamiceducdelete'},
                                                     color='primary')
                data_dict = df.to_dict()
                dictionarydata = {'Edit': editbtncol}
                dictionarydata2 = {'Delete': deletebtncol}
                data_dict.update(dictionarydata)
                data_dict.update(dictionarydata2)
                df = pd.DataFrame.from_dict(data_dict)

                # df = pd.DataFrame.from_dict(sessiondegreesprocessed, orient='columns')

                # if len(sessiondegreesprocessed) > 0:
                #     df = addcheckboxtocolumn(df)
                table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)




                return [False, table, sessiondegrees, sessiondegreesprocessed, sessionpersoneducid, -1, {'display': 'none'}]


            else:#incomplete fields
                df = pd.DataFrame.from_dict(sessiondegreesprocessed, orient='columns')
                # if len(sessiondegreesprocessed) > 0:
                #     df = addcheckboxtocolumn(df)

                editbtncol = {}
                deletebtncol = {}
                for index, row in df.iterrows():
                    editbtncol[index] = dbc.Button("Edit", id={'index': index, 'type': 'pds_dynamiceducedit'},
                                                   color='primary')
                    deletebtncol[index] = dbc.Button("Delete", id={'index': index, 'type': 'pds_dynamiceducdelete'},
                                                     color='primary')
                data_dict = df.to_dict()
                dictionarydata = {'Edit': editbtncol}
                dictionarydata2 = {'Delete': deletebtncol}
                data_dict.update(dictionarydata)
                data_dict.update(dictionarydata2)
                df = pd.DataFrame.from_dict(data_dict)


                table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

                return [True, table, sessiondegrees, sessiondegreesprocessed, sessionpersoneducid, -1, {'display': 'inline'}]

        elif eventid in ['pds_modal_bp_degree_cancel']:#cancel and close modal

            df = pd.DataFrame.from_dict(sessiondegreesprocessed, orient='columns')
            # if len(sessiondegreesprocessed) > 0:
            #     df = addcheckboxtocolumn(df)

            editbtncol = {}
            deletebtncol = {}
            for index, row in df.iterrows():
                editbtncol[index] = dbc.Button("Edit", id={'index': index, 'type': 'pds_dynamiceducedit'}, color = 'primary')
                deletebtncol[index] = dbc.Button("Delete", id={'index': index, 'type': 'pds_dynamiceducdelete'}, color = 'primary')
            data_dict = df.to_dict()
            dictionarydata = {'Edit': editbtncol}
            dictionarydata2 = {'Delete': deletebtncol}
            data_dict.update(dictionarydata)
            data_dict.update(dictionarydata2)
            df = pd.DataFrame.from_dict(data_dict)

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
            return [False, table, sessiondegrees, sessiondegreesprocessed, sessionpersoneducid, -2, {'display': 'none'}]

        elif eventid in ['pds_btn_delete_degree']:#delete degree button

            rowstodelete = returnselectedrows(pds_currentdegreediv, 11)
            parsed = urlparse.urlparse(url)
            mode = str(parse_qs(parsed.query)['mode'][0])

            if mode == "edit":
                uid = str(parse_qs(parsed.query)['uid'][0])

                degreeslist = []
                for index in range(len(sessiondegreesprocessed)):
                    if index in rowstodelete:
                        degreeslist.append(sessiondegrees[index])


                for item in degreeslist:
                    # if item['Program'] is None:
                    #     sqlbpfields = """
                    #         UPDATE person_educational_backgrounds
                    #            SET person_educ_delete_ind=%s
                    #          WHERE person_id=%s
                    #            AND person_degree_id=%s
                    #            AND person_program_id IS NULL
                    #            AND person_educ_start_date = %s
                    #            AND person_educ_school_id = %s
                    #     """
                    #     bpfields = [True, person_id, item["Degree"], item['Start Date'], item['Institution']]
                    # elif item['Start Date'] is None:
                    #     sqlbpfields = """
                    #         UPDATE person_educational_backgrounds
                    #            SET person_educ_delete_ind=%s
                    #          WHERE person_id=%s
                    #            AND person_degree_id = %s
                    #            AND person_program_id = %s
                    #            AND person_educ_start_date IS NULL
                    #            AND person_educ_school_id = %s
                    #     """
                    #     bpfields = [True, person_id, item["Degree"], item['Program'], item['Institution'],]
                    # elif item['Institution'] is None:
                    #     sqlbpfields = """
                    #         UPDATE person_educational_backgrounds
                    #            SET person_educ_delete_ind=%s
                    #          WHERE person_id=%s
                    #            AND person_degree_id=%s
                    #            AND person_program_id = %s
                    #            AND person_educ_start_date = %s
                    #            AND person_educ_school_id IS NULL
                    #     """
                    #     bpfields = [True, person_id, item["Degree"], item['Program'], item['Start Date'],]
                    # else:
                    sqlbpfields = """
                        UPDATE person_educational_backgrounds
                           SET person_educ_delete_ind=%s
                         WHERE person_id=%s
                           AND person_educ_id = %s
                    """
                    bpfields = [True, person_id, item['Person Educ ID']]
                    modifydatabase(sqlbpfields, bpfields)


            processedlist = []
            for index in range(len(sessiondegreesprocessed)):
                if index not in rowstodelete:
                    processedlist.append(sessiondegreesprocessed[index])

            sessiondegreesprocessed = processedlist
            processedlist2 = []

            for index in range(len(sessiondegrees)):
                if index not in rowstodelete:
                    processedlist2.append(sessiondegrees[index])

            sessiondegrees = processedlist2

            df = pd.DataFrame.from_dict(sessiondegreesprocessed, orient='columns')
            # if len(sessiondegreesprocessed) > 0:
            #     df = addcheckboxtocolumn(df)

            editbtncol = {}
            deletebtncol = {}
            for index, row in df.iterrows():
                editbtncol[index] = dbc.Button("Edit", id={'index': index, 'type': 'pds_dynamiceducedit'}, color = 'primary')
                deletebtncol[index] = dbc.Button("Delete", id={'index': index, 'type': 'pds_dynamiceducdelete'}, color = 'primary')
            data_dict = df.to_dict()
            dictionarydata = {'Edit': editbtncol}
            dictionarydata2 = {'Delete': deletebtncol}
            data_dict.update(dictionarydata)
            data_dict.update(dictionarydata2)
            df = pd.DataFrame.from_dict(data_dict)

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
            return [False, table, sessiondegrees, sessiondegreesprocessed, sessionpersoneducid, -1, {'display': 'none'}]

        elif eventid == "pds_submit_summary":#submit PDS button

            if pds_submit_summary == 1:
                return [False, [], [], [], [], 1, {'display': 'none'}]
            else:
                df = pd.DataFrame.from_dict(sessiondegreesprocessed, orient='columns')
                # if len(sessiondegreesprocessed) > 0:
                #     df = addcheckboxtocolumn(df)
                table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
                return [False, table, sessiondegrees, sessiondegreesprocessed, sessionpersoneducid, -1, {'display': 'none'}]

        elif eventid == "pds_load_bp" and pds_load_bp == 2:#if page load/page open

            parsed = urlparse.urlparse(url)
            uid = str(parse_qs(parsed.query)['uid'][0])

            sql = ''' SELECT person_degree_id, degree_name, person_program_id, program_name, person_educ_grad_date, person_educ_start_date, person_educ_end_date,
            person_educ_school_id,school_name, person_educ_gwa_completed, person_educ_wa_major, person_number_failing_marks, person_educ_id
            FROM persons p
            LEFT JOIN person_educational_backgrounds peb on peb.person_id = p.person_id
            LEFT JOIN degrees d on d.degree_id = peb.person_degree_id
            LEFT JOIN programs prg on prg.program_id = peb.person_program_id
            LEFT JOIN schools s on s.school_id = peb.person_educ_school_id
            WHERE p.person_id = %s AND person_educ_delete_ind=%s
            ORDER BY person_educ_id ASC'''
            values = (uid, False)
            columns = ['person_degree_id', 'degree_name', 'person_program_id', 'program_name', 'person_educ_grad_date', 'person_educ_start_date', 'person_educ_end_date',
                       'person_educ_school_id', 'school_name', 'person_educ_gwa_completed', 'person_educ_wa_major', 'person_number_failing_marks', 'person_educ_id']
            df = securequerydatafromdatabase(sql, values, columns)

            editbtncol = {}
            deletebtncol = {}
            for index, row in df.iterrows():
                editbtncol[index] = dbc.Button("Edit", id={'index': index, 'type': 'pds_dynamiceducedit'}, color = 'primary')
                deletebtncol[index] = dbc.Button("Delete", id={'index': index, 'type': 'pds_dynamiceducdelete'}, color = 'primary')
            data_dict = df.to_dict()
            dictionarydata = {'Edit': editbtncol}
            dictionarydata2 = {'Delete': deletebtncol}
            data_dict.update(dictionarydata)
            data_dict.update(dictionarydata2)
            df = pd.DataFrame.from_dict(data_dict)


            dfsessiondegrees = df[['person_educ_id', 'person_degree_id', 'person_program_id', 'person_educ_grad_date', 'person_educ_start_date', 'person_educ_end_date',
                                   'person_educ_school_id', 'person_educ_gwa_completed', 'person_educ_wa_major', 'person_number_failing_marks']].copy()
            dfsessiondegrees.columns = ["Entry ID","Degree", "Program", "Graduation Date", "Start Date",
                                        "End Date", "Institution", "GWA", "Weighted Average", "Number of Failing Marks"]
            sessiondegrees = dfsessiondegrees.to_dict('records')

            sessiondegreesprocesseddf = df[['person_educ_id', 'degree_name', 'program_name', 'person_educ_grad_date', 'person_educ_start_date',
                                            'person_educ_end_date', 'school_name', 'person_educ_gwa_completed', 'person_educ_wa_major', 'person_number_failing_marks', 'Edit', 'Delete']].copy()
            sessiondegreesprocesseddf.columns = ["Entry ID", "Degree", "Program", "Graduation Date", "Start Date",
                                                 "End Date", "Institution", "GWA", "Weighted Average", "Number of Failing Marks", 'Edit', 'Delete']

            table = sessiondegreesprocesseddf
            sessiondegreesprocessed = sessiondegreesprocesseddf.to_dict('records')
            sessiondegreesprocesseddf = pd.DataFrame.from_dict(
                sessiondegreesprocessed, orient='columns')
            # if len(sessiondegreesprocesseddf) > 0:
            #     sessiondegreesprocesseddf = addcheckboxtocolumn(sessiondegreesprocesseddf)


            table = dbc.Table.from_dataframe(
                sessiondegreesprocesseddf, striped=True, bordered=True, hover=True)
            sessionpersoneducid = df['person_educ_id'].to_list()

            return [False, table, sessiondegrees, sessiondegreesprocessed, sessionpersoneducid, -1, {'display': 'none'}]

        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback(
    [
        Output("pds_degree", "value"),
        Output("pds_program", "value"),
        Output("pds_educyear", "date"),
        Output("pds_institution", "value"),
        Output("pds_gwa", "value"),
        Output("pds_wamajor", "value"),
        Output("pds_fail", "value"),
        Output("pds_startdate", "date"),
        Output("pds_enddate", "date"),
    ],
    [
        Input("pds_degrees_summary", "value"),
        # Input({'type': 'pds_dynamiceducedit', 'index': ALL}, 'n_clicks')
    ],
    [
        State("pds_degree", "value"),
        State("pds_program", "value"),
        State("pds_educyear", "date"),
        State("pds_institution", "value"),
        State("pds_gwa", "value"),
        State("pds_wamajor", "value"),
        State("pds_fail", "value"),
        State("pds_startdate", "date"),
        State("pds_enddate", "date"),
        State('sessiondegrees', 'data'),
        State('sessiondegreesprocessed', 'data')

    ],
)
def toggle_modal_degrees_values(pds_degrees_summary,
                                # pds_dynamiceducedit,
                                pds_degree, pds_program, pds_educyear, pds_institution,
                                pds_gwa, pds_wamajor, pds_fail, pds_startdate, pds_enddate,
                                sessiondegrees, sessiondegreesprocessed
                                ):

    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if pds_degrees_summary == -1:
            pds_degree = ""
            pds_program = ""
            pds_educyear = date.today()
            pds_institution = ""
            pds_gwa = ""
            pds_wamajor = ""
            pds_fail = 0
            pds_startdate = date.today()
            pds_enddate = date.today()

        elif pds_degrees_summary >= 0:

            # index = json.loads(eventid)["index"]
            index = pds_degrees_summary

            pds_degree = sessiondegrees[index]['Degree']
            pds_program = sessiondegrees[index]['Program']
            pds_educyear = sessiondegrees[index]['Graduation Date']
            pds_institution = sessiondegrees[index]['Institution']
            pds_gwa = sessiondegrees[index]['GWA']
            pds_wamajor = sessiondegrees[index]['Weighted Average']
            pds_fail = sessiondegrees[index]['Number of Failing Marks']
            pds_startdate = sessiondegrees[index]['Start Date']
            pds_enddate = sessiondegrees[index]['End Date']


    return [pds_degree, pds_program, pds_educyear, pds_institution,
            pds_gwa, pds_wamajor, pds_fail, pds_startdate, pds_enddate]


def addcheckboxtocolumn(df):
    linkcolumn = {}
    for index, row in df.iterrows():
        linkcolumn[index] = dbc.Checklist(options=[{"label": "", "value": 1}], value=[])
    data_dict = df.to_dict()
    dictionarydata = {'Select': linkcolumn}
    data_dict.update(dictionarydata)
    df = pd.DataFrame.from_dict(data_dict)
    return df


def returnselectedrows(dftable, ncolumns):
    selectedrows = []
    if dftable:
        for i in range(0, len(dftable['props']['children'][1]['props']['children'])):
            if 1 in dftable['props']['children'][1]['props']['children'][i]['props']['children'][ncolumns-1]['props']['children']['props']['value']:
                selectedrows.append(i)

    return selectedrows


@app.callback([
    Output('pds_divforeigncit', 'style'),
],
    [
    Input('pds_citizenship', 'value'),
],)
def toggle_pds_divforeigncit(bpocitizenship):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'pds_citizenship':
            if bpocitizenship == 1:
                return [{'display': 'none'}]
            else:
                return [{'display': 'inline'}]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback([
    Output('pds_addcountryperm', 'disabled'),
    Output('pds_regionperm', 'disabled'),
    Output('pds_aprovinceperm', 'disabled'),
    Output('pds_citymunperm', 'disabled'),
    Output('pds_streetaddressperm', 'disabled'),
    Output('pds_subdvillageperm', 'disabled'),
    Output('pds_brgyaddressperm', 'disabled'),
    Output('pds_zipcodeperm', 'disabled'),
],
    [
    Input('pds_permsameascurrent', 'checked'),
],
[


]
)
def toggle_perm_adds(pds_permsameascurrent):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'pds_permsameascurrent':
            if pds_permsameascurrent:
                return [True, True, True, True, True, True, True, True]
            else:
                return [False, False, False, False, False, False, False, False]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback([
    Output('pds_enddate', 'min_date_allowed'),
],
    [
    Input('pds_startdate', 'date'),
],
)
def degree_mindate_pds_startdate(pds_startdate):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'pds_startdate':
            return [pds_startdate]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback([
    Output('pds_startdate', 'max_date_allowed'),
],
    [
    Input('pds_enddate', 'date'),
],
)
def degree_mindate_pds_enddate(pds_enddate):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'pds_enddate':
            return [pds_enddate]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback([

    Output('pds_resultmodal', 'is_open'),
    Output('pds_submit_summary', 'value'),

],
    [
    Input('pds_confirmsubmitgo', 'n_clicks'),
],
    [
    State('pds_temp_unit', 'value'),
    State('pds_title', 'value'),
    State('pds_isactive', 'value'),
    State('pds_lastname', 'value'),
    State('pds_firstname', 'value'),
    State('pds_middlename', 'value'),
    State('pds_suffixname', 'value'),
    State('pds_dob', 'date'),
    State('pds_pob', 'value'),
    State('pds_sexatbirth', 'value'),
    State('pds_civilstatus', 'value'),
    State('pds_bloodtype', 'value'),

    State('pds_mobilecontactnumber', 'value'),
    State('pds_lanecontactnumber', 'value'),
    State('pds_email', 'value'),
    State('pds_citizenship', 'value'),
    State('pds_typeofcit', 'value'),
    State('pds_countryofcit', 'value'),
    State('pds_addcountrycurr', 'value'),
    State('pds_regioncurr', 'value'),
    State('pds_aprovincecurr', 'value'),
    State('pds_citymuncurrent', 'value'),

    State('pds_streetaddresscurr', 'value'),
    State('pds_subdvillagecurr', 'value'),
    State('pds_brgyaddresscurr', 'value'),
    State('pds_zipcodecurr', 'value'),
    State('pds_addcountryperm', 'value'),
    State('pds_regionperm', 'value'),
    State('pds_aprovinceperm', 'value'),
    State('pds_citymunperm', 'value'),
    State('pds_streetaddressperm', 'value'),
    State('pds_subdvillageperm', 'value'),

    State('pds_brgyaddressperm', 'value'),
    State('pds_zipcodeperm', 'value'),
    State('pds_gsis', 'value'),
    State('pds_pagibig', 'value'),
    State('pds_philhealth', 'value'),
    State('pds_sss', 'value'),
    State('pds_tin', 'value'),
    State('pds_governmentid', 'value'),
    State('pds_govidnumber', 'value'),
    State('pds_permsameascurrent', 'checked'),

    State('sessiondegrees', 'data'),
    State('current_user_id', 'data'),
    State('sessioncurrentunit', 'data'),
    State("url", "search"),
    State("sessionpersonid", 'data'),
    State("sessionpersoneducid", 'data'),
    State('sessioneligibilities', 'data'),
    State('pds_eligibilities_checkbox', 'checked'),
    State('pds_pobislocal', 'value'),

    State('pds_pobprovince', 'value'),
    State('pds_pobcity', 'value'),
    State('pds_pobcountry', 'value'),
    State('pds_addempnum', 'value'),
    State('pds_empnum', 'value'),
    State('sessioncurrentrole', 'data')




]

)
def save_bp(pds_confirmsubmitgo,
            pds_temp_unit,
            pds_title,
            pds_isactive,
            pds_lastname,
            pds_firstname,
            pds_middlename,
            pds_suffixname,
            pds_dob,
            pds_pob,
            pds_sexatbirth,
            pds_civilstatus,
            pds_bloodtype,
            pds_mobilecontactnumber,
            pds_lanecontactnumber,
            pds_email,
            pds_citizenship,
            pds_typeofcit,
            pds_countryofcit,
            pds_addcountrycurr,
            pds_regioncurr,
            pds_aprovincecurr,
            pds_citymuncurrent,
            pds_streetaddresscurr,
            pds_subdvillagecurr,
            pds_brgyaddresscurr,
            pds_zipcodecurr,
            pds_addcountryperm,
            pds_regionperm,
            pds_aprovinceperm,
            pds_citymunperm,
            pds_streetaddressperm,
            pds_subdvillageperm,
            pds_brgyaddressperm,
            pds_zipcodeperm,
            pds_gsis,
            pds_pagibig,
            pds_philhealth,
            pds_sss,
            pds_tin,
            pds_governmentid,
            pds_govidnumber,

            pds_permsameascurrent,
            sessiondegrees,
            current_user_id,
            sessioncurrentunit,
            url,
            # bp_emp_type,
            person_id,
            sessionpersoneducid,


            sessioneligibilities,
            pds_eligibilities_checkbox,

            pds_pobislocal,
            pds_pobprovince,
            pds_pobcity,
            pds_pobcountry,
            pds_addempnum,
            pds_empnum,
            sessioncurrentrole


            ):

    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    savemode = str(parse_qs(parsed.query)['mode'][0])
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid in ['pds_confirmsubmitgo']:

            if pds_permsameascurrent:

                pds_addcountryperm, pds_regionperm, pds_aprovinceperm, pds_citymunperm, pds_streetaddressperm, pds_subdvillageperm, pds_brgyaddressperm, pds_zipcodeperm = setsameaddress(pds_addcountrycurr,
                                                                                                                                                                                          pds_regioncurr, pds_aprovincecurr, pds_citymuncurrent, pds_streetaddresscurr, pds_subdvillagecurr, pds_brgyaddresscurr, pds_zipcodecurr)

            persondetails = [pds_lastname, pds_firstname, pds_middlename, pds_suffixname, pds_dob, pds_pob, pds_sexatbirth, pds_civilstatus, pds_bloodtype,
                             pds_citizenship, pds_typeofcit, pds_countryofcit, pds_gsis, pds_pagibig, pds_philhealth, pds_sss, pds_tin]
            addresses = [pds_addcountrycurr, pds_regioncurr, pds_aprovincecurr, pds_citymuncurrent, pds_streetaddresscurr, pds_subdvillagecurr, pds_brgyaddresscurr, pds_zipcodecurr,
                         pds_addcountryperm, pds_regionperm, pds_aprovinceperm, pds_citymunperm, pds_streetaddressperm, pds_subdvillageperm, pds_brgyaddressperm, pds_zipcodeperm]
            degrees = sessiondegrees

            pds_lastname = safeupper(pds_lastname)
            pds_firstname = safeupper(pds_firstname)
            pds_middlename = safeupper(pds_middlename)
            pds_suffixname = safeupper(pds_suffixname)
            pds_pob = safeupper(pds_pob)

            pds_streetaddresscurr = safeupper(pds_streetaddresscurr)
            pds_subdvillagecurr = safeupper(pds_subdvillagecurr)
            pds_brgyaddresscurr = safeupper(pds_brgyaddresscurr)
            pds_streetaddressperm = safeupper(pds_streetaddressperm)
            pds_subdvillageperm = safeupper(pds_subdvillageperm)
            pds_brgyaddressperm = safeupper(pds_brgyaddressperm)

            if savemode == "add":  # add mode

                sqlperson = """
                    INSERT INTO persons (person_last_name, person_first_name, person_middle_name, person_name_extension,
                        person_dob, person_pob, person_sex_id, person_civil_status_id, person_blood_type_id, person_citizenship_id, person_citizenship_type_id,
                        person_country_citizenship_id, person_gsis_no, person_pagibig_no, person_philhealth_no, person_sss_no, person_tin, person_gov_id_type_id, person_gov_id_no,
                        person_inserted_by, person_inserted_on, person_delete_ind, person_temp_unit_id, person_title_id, person_is_active,
                        person_pob_is_local, person_pob_country_id, person_pob_city_id, person_pob_prov_id, person_entry_id)
                    VALUES (%s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s)
                    RETURNING person_id
                """

                if pds_pobislocal == 1:
                    pds_pobislocal = True
                    pds_pobcountry = 168
                    pds_pob = None

                else:
                    pds_pobislocal = False
                    pds_pobprovince = None
                    pds_pobcity = None

                persondetails = [pds_lastname, pds_firstname, pds_middlename, pds_suffixname,
                                 pds_dob, pds_pob, pds_sexatbirth, pds_civilstatus, pds_bloodtype, pds_citizenship, pds_typeofcit,
                                 pds_countryofcit, pds_gsis, pds_pagibig, pds_philhealth, pds_sss, pds_tin, pds_governmentid, pds_govidnumber,
                                 current_user_id, datetime.now(), False, pds_temp_unit, pds_title, pds_isactive,
                                 pds_pobislocal, pds_pobcountry, pds_pobcity, pds_pobprovince, 1
                                 ]

                person_id = modifydatabasereturnid(sqlperson, persondetails)

                # Insert Emp Number if toggled
                if int(sessioncurrentrole) in [1, 27] and 1 in pds_addempnum:
                    sqlemp = """
                            INSERT INTO employees (person_id, emp_number, emp_inserted_by, emp_inserted_on, emp_delete_ind)
                            VALUES (%s, %s, %s, %s, %s)
                        """
                    empdetails = (person_id, pds_empnum, current_user_id, datetime.now(), False)
                    modifydatabase(sqlemp, empdetails)

                # Insert Contact Numbers
                sqlcontact = """
                    INSERT INTO person_contact_numbers(person_id, person_contact_number,person_contact_type_id, person_contact_inserted_by,person_contact_inserted_on,person_contact_delete_ind )
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                contactdetails = [[person_id, pds_mobilecontactnumber, 2, current_user_id, datetime.now(), False], [person_id, pds_lanecontactnumber, 1, current_user_id, datetime.now(), False]]

                bulkmodifydatabase(sqlcontact, contactdetails)

                # Insert Personal Email
                sqlemail = """
                    INSERT INTO person_email_addresses(person_id, person_email_address,person_email_type_id,person_email_inserted_by,person_email_inserted_on,person_email_delete_ind )
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                emaildetails = [person_id, pds_email, 2, current_user_id, datetime.now(), False]
                modifydatabase(sqlemail, emaildetails)

                # Insert Addresses
                sqlpaddreses = """
                    INSERT INTO addresses (person_id, address_country_id, address_region_id, address_prov_id,
                        address_city_id, address_street, address_subdivision_village,address_brgy, address_zip_code, address_type_id,
                         address_inserted_by, address_inserted_on, address_delete_ind )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s)

                """
                addresses = [[person_id, pds_addcountrycurr, pds_regioncurr, pds_aprovincecurr, pds_citymuncurrent, pds_streetaddresscurr, pds_subdvillagecurr, pds_brgyaddresscurr, pds_zipcodecurr, 1, current_user_id, datetime.now(), False],
                             [person_id, pds_addcountryperm, pds_regionperm, pds_aprovinceperm, pds_citymunperm, pds_streetaddressperm, pds_subdvillageperm, pds_brgyaddressperm, pds_zipcodeperm, 2, current_user_id, datetime.now(), False]]
                bulkmodifydatabase(sqlpaddreses, addresses)

                # Insert Educational Backgrounds

                insertdegrees(degrees, person_id, current_user_id)#pds confirm button


                # Insert eligibilities

                insert_eligibilities(sessioneligibilities, person_id, current_user_id)

                pds_submit_summary = 1

            else:  # edit mode

                parsed = urlparse.urlparse(url)
                uid = str(parse_qs(parsed.query)['uid'][0])
                person_id = uid

                pds_deletebuttonind = False

                sqlperson = """
                    UPDATE persons SET person_last_name=%s, person_first_name=%s, person_middle_name=%s, person_name_extension=%s,
                        person_dob=%s, person_pob=%s, person_sex_id=%s, person_civil_status_id=%s, person_blood_type_id=%s,person_citizenship_id=%s, person_citizenship_type_id=%s,
                        person_country_citizenship_id=%s,person_gsis_no=%s, person_pagibig_no=%s,person_philhealth_no=%s,person_sss_no=%s,person_tin=%s, person_gov_id_type_id=%s, person_gov_id_no=%s,
                        person_last_modified_by=%s, person_last_modified_on=%s, person_delete_ind=%s, person_title_id = %s,
                        person_pob_is_local = %s, person_pob_country_id = %s, person_pob_city_id = %s, person_pob_prov_id = %s, person_temp_unit_id = %s, person_is_active = %s
                    WHERE person_id =%s
                """

                if pds_pobislocal == 1:
                    pds_pobislocal = True
                    pds_pobcountry = 168  # Philippines
                    pds_pob = None
                else:
                    pds_pobislocal = False
                    pds_pobprovince = None
                    pds_pobcity = None

                persondetails = [pds_lastname, pds_firstname, pds_middlename, pds_suffixname, pds_dob, pds_pob, pds_sexatbirth, pds_civilstatus, pds_bloodtype,
                                 pds_citizenship, pds_typeofcit, pds_countryofcit, pds_gsis, pds_pagibig, pds_philhealth, pds_sss, pds_tin, pds_governmentid, pds_govidnumber,
                                 current_user_id, datetime.now(), pds_deletebuttonind, pds_title,
                                 pds_pobislocal,
                                 pds_pobcountry,
                                 pds_pobcity,
                                 pds_pobprovince,
                                 pds_temp_unit,
                                 pds_isactive,

                                 person_id]

                modifydatabase(sqlperson, persondetails)

                sql1 = '''
                    SELECT person_contact_id
                    FROM person_contact_numbers
                    WHERE person_id = %s
                    AND person_contact_delete_ind = %s

                '''

                values1 = (person_id, False)
                columns1 = ['person_contact_id']
                dfcontactnos = securequerydatafromdatabase(sql1, values1, columns1)

                if dfcontactnos.empty:
                    sql7 = """
                        INSERT INTO person_contact_numbers(
                            person_id, person_contact_number, person_contact_type_id, person_contact_inserted_by, person_contact_inserted_on, person_contact_delete_ind)
                            VALUES (%s, %s, %s, %s, %s, %s);
                    """
                    values7 = [person_id, pds_mobilecontactnumber,
                               1, current_user_id, datetime.now(), False]

                    modifydatabase(sql7, values7)

                    sql8 = """
                         INSERT INTO person_contact_numbers(
                             person_id, person_contact_number, person_contact_type_id, person_contact_inserted_by, person_contact_inserted_on, person_contact_delete_ind)
                             VALUES (%s, %s, %s, %s, %s, %s);
                     """
                    values8 = [person_id, pds_lanecontactnumber, 2,
                               current_user_id, datetime.now(), pds_deletebuttonind]

                    modifydatabase(sql8, values8)

                else:

                    sqlcontact = """
                        UPDATE person_contact_numbers SET person_contact_number=%s, person_contact_inserted_by=%s,
                        person_contact_inserted_on=%s,person_contact_delete_ind=%s WHERE person_id=%s and person_contact_type_id=%s
                    """

                    contactdetails = [pds_mobilecontactnumber, current_user_id,
                                      datetime.now(), pds_deletebuttonind, person_id, 2]
                    modifydatabase(sqlcontact, contactdetails)

                    contactdetails = [pds_lanecontactnumber, current_user_id,
                                      datetime.now(), pds_deletebuttonind, person_id, 1]
                    modifydatabase(sqlcontact, contactdetails)

                sql8 = '''
                        SELECT person_email_id
                        FROM person_email_addresses
                        WHERE person_id = %s
                        AND person_email_delete_ind = %s

                    '''

                values8 = (person_id, False)
                columns8 = ['person_email_id']
                dfemails = securequerydatafromdatabase(sql8, values8, columns8)

                if dfemails.empty:

                    sqlemail = """
                        INSERT INTO person_email_addresses(
                            person_id, person_email_address, person_email_type_id, person_email_inserted_by, person_email_inserted_on, person_email_delete_ind)
                            VALUES (%s, %s, %s, %s, %s, %s);
                    """
                    emaildetails = [person_id, pds_email, 2, current_user_id,
                                    datetime.now(), pds_deletebuttonind]
                    modifydatabase(sqlemail, emaildetails)

                else:

                    sqlemail = """
                        UPDATE person_email_addresses SET person_email_address=%s,person_email_inserted_by=%s,person_email_inserted_on=%s,person_email_delete_ind=%s
                        WHERE person_id=%s and person_email_type_id=%s
                    """
                    emaildetails = [pds_email, current_user_id,
                                    datetime.now(), pds_deletebuttonind, person_id, 2]
                    modifydatabase(sqlemail, emaildetails)

                sql9 = '''
                    SELECT address_id
                    FROM addresses
                    WHERE person_id = %s
                    AND address_delete_ind = %s

                '''

                values9 = (person_id, False)
                columns9 = ['address_id']
                dfaddresses = securequerydatafromdatabase(sql9, values9, columns9)

                if dfaddresses.empty:

                    sqlpaddreses = """
                    INSERT INTO addresses(
                        person_id, address_country_id, address_region_id, address_prov_id, address_city_id, address_street, address_subdivision_village,
                        address_brgy, address_zip_code, address_inserted_by, address_inserted_on, address_delete_ind, address_type_id)
                        VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s);
                    """
                    print('HERE222', pds_regioncurr, pds_aprovincecurr, pds_citymuncurrent, pds_regionperm, pds_aprovinceperm, pds_citymunperm)
                    if len(pds_regioncurr) == 0:
                        pds_regioncurr = None
                    if len(pds_aprovincecurr) == 0:
                        pds_aprovincecurr = None
                    if len(pds_citymuncurrent) == 0:
                        pds_citymuncurrent = None
                    if len(pds_regionperm) == 0:
                        pds_regionperm = None
                    if len(pds_aprovinceperm) == 0:
                        pds_aprovinceperm = None
                    if len(pds_citymunperm) == 0:
                        pds_citymunperm = None

                    print('HERE223', pds_regioncurr, pds_aprovincecurr, pds_citymuncurrent, pds_regionperm,
                          pds_aprovinceperm, pds_citymunperm)

                    # print('HERE6362', pds_regioncurr, len(pds_regioncurr), pds_aprovincecurr, pds_citymuncurrent)

                    addresses = [person_id, pds_addcountrycurr, pds_regioncurr, pds_aprovincecurr, pds_citymuncurrent, pds_streetaddresscurr,
                                 pds_subdvillagecurr, pds_brgyaddresscurr, pds_zipcodecurr, current_user_id, datetime.now(), pds_deletebuttonind, 1]
                    modifydatabase(sqlpaddreses, addresses)

                    addresses = [person_id, pds_addcountryperm, pds_regionperm, pds_aprovinceperm, pds_citymunperm, pds_streetaddressperm,
                                 pds_subdvillageperm, pds_brgyaddressperm, pds_zipcodeperm, current_user_id, datetime.now(), pds_deletebuttonind, 2]
                    modifydatabase(sqlpaddreses, addresses)

                else:

                    sqlpaddreses = """
                        UPDATE addresses SET address_country_id= %s, address_region_id= %s, address_prov_id= %s,
                            address_city_id= %s, address_street= %s, address_subdivision_village= %s,address_brgy= %s, address_zip_code= %s,
                             address_inserted_by= %s, address_inserted_on= %s, address_delete_ind= %s
                        WHERE person_id = %s and address_type_id= %s
                    """
                    addresses = [pds_addcountrycurr, pds_regioncurr, pds_aprovincecurr, pds_citymuncurrent, pds_streetaddresscurr,
                                 pds_subdvillagecurr, pds_brgyaddresscurr, pds_zipcodecurr, current_user_id, datetime.now(), pds_deletebuttonind, person_id, 1]
                    modifydatabase(sqlpaddreses, addresses)
                    addresses = [pds_addcountryperm, pds_regionperm, pds_aprovinceperm, pds_citymunperm, pds_streetaddressperm,
                                 pds_subdvillageperm, pds_brgyaddressperm, pds_zipcodeperm, current_user_id, datetime.now(), pds_deletebuttonind, person_id, 2]
                    modifydatabase(sqlpaddreses, addresses)


                insertdegrees(degrees, person_id, current_user_id)
                insert_eligibilities(sessioneligibilities, person_id, current_user_id)
                pds_submit_summary = 2

            update_persons_history(person_id, current_user_id, pds_title, pds_lastname, pds_firstname, pds_middlename, pds_suffixname,
                                   pds_civilstatus,  pds_pobcountry,   pds_pobcity,  pds_pobprovince, pds_temp_unit, savemode)
            return [
                True,
                pds_submit_summary

            ]

        else:
            raise PreventUpdate

    else:
        raise PreventUpdate


def setsameaddress(pds_addcountrycurr, pds_regioncurr, pds_aprovincecurr, pds_citymuncurrent, pds_streetaddresscurr, pds_subdvillagecurr, pds_brgyaddresscurr, pds_zipcodecurr):

    return pds_addcountrycurr, pds_regioncurr, pds_aprovincecurr, pds_citymuncurrent, pds_streetaddresscurr, pds_subdvillagecurr, pds_brgyaddresscurr, pds_zipcodecurr


def checkstyle(isvalidcomponent):
    if isvalidcomponent:
        style = {"text-align": "left", 'color': 'red'}
    else:
        style = {"text-align": "left", 'color': 'black'}
    return style


def insertdegrees(degreeslist, person_id, current_user_id):

    #get list of entry ids:
    entryidlist = []
    for i in degreeslist:
        if i.get('Entry ID') is not None:

            entryidlist.append(i['Entry ID'])

    #delete educ rows
    sql8 = '''
            SELECT person_educ_id
            FROM person_educational_backgrounds
            WHERE person_id = %s
            AND person_educ_delete_ind = %s

        '''

    values8 = (person_id, False)
    columns8 = ['person_educ_id']
    dfexistingeducids = securequerydatafromdatabase(sql8, values8, columns8)

    dfexistingeducids_list = dfexistingeducids['person_educ_id'].tolist()

    for i in dfexistingeducids_list:
        if i not in entryidlist:

            sqldeleteeduc = '''
                UPDATE person_educational_backgrounds
                SET person_educ_delete_ind = %s
                WHERE person_educ_id = %s

            '''

            valuesdelete = (True, i)

            modifydatabase(sqldeleteeduc, valuesdelete)

    for i in range(0, len(degreeslist)):

        dict_temp = degreeslist[i]

        if dict_temp.get('Entry ID') is None:

            sqldegreesnew = """
                INSERT INTO person_educational_backgrounds(person_degree_id, person_program_id, person_educ_grad_date, person_educ_start_date,
                    person_educ_end_date, person_educ_school_id, person_educ_gwa_completed, person_educ_wa_major,
                    person_number_failing_marks,
                     person_id, person_educ_inserted_by, person_educ_created_on,person_educ_delete_ind  )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s,%s)

            """

            valuesnew = (dict_temp['Degree'], dict_temp['Program'], dict_temp['Graduation Date'], dict_temp['Start Date'] ,
                         dict_temp['End Date'], dict_temp['Institution'], dict_temp['GWA'], dict_temp['Weighted Average'],
                         dict_temp['Number of Failing Marks'],
                         person_id, current_user_id, datetime.now(), False)

            modifydatabase(sqldegreesnew, valuesnew)

        else:

            sqldegreesnew = """
                UPDATE person_educational_backgrounds
                SET person_degree_id = %s, person_program_id = %s, person_educ_grad_date = %s, person_educ_start_date = %s,
                    person_educ_end_date = %s, person_educ_school_id = %s, person_educ_gwa_completed = %s, person_educ_wa_major = %s,
                    person_number_failing_marks = %s,
                     person_id = %s, person_educ_inserted_by = %s, person_educ_created_on = %s, person_educ_delete_ind = %s

                WHERE person_educ_id = %s

            """

            valuesnew = (dict_temp['Degree'], dict_temp['Program'], dict_temp['Graduation Date'], dict_temp['Start Date'] ,
                         dict_temp['End Date'], dict_temp['Institution'], dict_temp['GWA'], dict_temp['Weighted Average'],
                         dict_temp['Number of Failing Marks'],
                         int(person_id), current_user_id, datetime.now(), False,
                         dict_temp['Entry ID'])

            modifydatabase(sqldegreesnew, valuesnew)

    # sqldegrees = """
    #     INSERT INTO person_educational_backgrounds(person_degree_id, person_program_id, person_educ_grad_date, person_educ_start_date,
    #         person_educ_end_date, person_educ_school_id, person_educ_gwa_completed, person_educ_wa_major, person_number_failing_marks,
    #          person_id, person_educ_inserted_by, person_educ_created_on,person_educ_delete_ind  )
    #     VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s,%s)
    #
    # """
    #
    # degressdf = pd.DataFrame(degreeslist)
    # degreesdf = degressdf.values.tolist()
    # finaldegrees = []
    # for item in degreesdf:
    #     item.append(person_id)
    #     item.append(current_user_id)
    #     item.append(datetime.now())
    #     item.append(False)
    #     finaldegrees.append(item)
    # bulkmodifydatabase(sqldegrees, finaldegrees)


def checkiflengthx(stringvar, x):
    isvalid = False
    isinvalid = False

    if len(str(stringvar)) == x:
        isvalid = True
        isinvalid = False
    else:
        isvalid = False
        isinvalid = True
    return isvalid, isinvalid


def checkiflengthten(stringvar):
    isvalid = False
    isinvalid = False

    if len(str(stringvar)) == 10:
        isvalid = True
        isinvalid = False
    else:
        isvalid = False
        isinvalid = True
    return isvalid, isinvalid


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
#
#
#


@app.callback([
    Output('pds_temp_unit', 'value'),
    Output('pds_title', 'value'),
    Output('pds_isactive', 'value'),
    Output('pds_lastname', 'value'),
    Output('pds_firstname', 'value'),
    Output('pds_middlename', 'value'),
    Output('pds_suffixname', 'value'),
    Output('pds_lastname', 'disabled'),
    Output('pds_firstname', 'disabled'),
    Output('pds_middlename', 'disabled'),

    Output('pds_suffixname', 'disabled'),
    Output('pds_dob', 'date'),
    Output('pds_pob', 'value'),
    Output('pds_sexatbirth', 'value'),
    Output('pds_civilstatus', 'value'),
    Output('pds_bloodtype', 'value'),
    Output('pds_mobilecontactnumber', 'value'),
    Output('pds_lanecontactnumber', 'value'),
    Output('pds_email', 'value'),
    Output('pds_citizenship', 'value'),

    Output('pds_typeofcit', 'value'),
    Output('pds_countryofcit', 'value'),
    Output('pds_addcountrycurr', 'value'),
    Output('pds_regioncurr', 'value'),
    Output('pds_aprovincecurr', 'value'),
    Output('pds_citymuncurrent', 'value'),
    Output('pds_streetaddresscurr', 'value'),
    Output('pds_subdvillagecurr', 'value'),
    Output('pds_brgyaddresscurr', 'value'),
    Output('pds_zipcodecurr', 'value'),

    Output('pds_addcountryperm', 'value'),
    Output('pds_regionperm', 'value'),
    Output('pds_aprovinceperm', 'value'),
    Output('pds_citymunperm', 'value'),
    Output('pds_streetaddressperm', 'value'),
    Output('pds_subdvillageperm', 'value'),
    Output('pds_brgyaddressperm', 'value'),
    Output('pds_zipcodeperm', 'value'),
    Output('pds_gsis', 'value'),
    Output('pds_pagibig', 'value'),

    Output('pds_philhealth', 'value'),
    Output('pds_sss', 'value'),
    Output('pds_tin', 'value'),
    Output('pds_governmentid', 'value'),
    Output('pds_govidnumber', 'value'),
    Output('sessionpersonid', 'data'),
    Output('pds_pobislocal', 'value'),
    Output('pds_pobprovince', 'value'),
    Output('pds_pobcity', 'value'),
    Output('pds_pobcountry', 'value'),

],
    [
    Input('pds_submit_summary', 'value'),
    Input('pds_load_bp', 'value')
], [
    State('pds_temp_unit', 'value'),
    State('pds_title', 'value'),
    State('pds_isactive', 'value'),
    State('pds_lastname', 'value'),
    State('pds_firstname', 'value'),
    State('pds_middlename', 'value'),
    State('pds_suffixname', 'value'),
    State('pds_dob', 'date'),
    State('pds_pob', 'value'),
    State('pds_sexatbirth', 'value'),
    State('pds_civilstatus', 'value'),
    State('pds_bloodtype', 'value'),
    State('pds_mobilecontactnumber', 'value'),
    State('pds_lanecontactnumber', 'value'),
    State('pds_email', 'value'),
    State('pds_citizenship', 'value'),
    State('pds_typeofcit', 'value'),
    State('pds_countryofcit', 'value'),
    State('pds_addcountrycurr', 'value'),
    State('pds_regioncurr', 'value'),
    State('pds_aprovincecurr', 'value'),
    State('pds_citymuncurrent', 'value'),
    State('pds_streetaddresscurr', 'value'),
    State('pds_subdvillagecurr', 'value'),
    State('pds_brgyaddresscurr', 'value'),
    State('pds_zipcodecurr', 'value'),
    State('pds_addcountryperm', 'value'),
    State('pds_regionperm', 'value'),
    State('pds_aprovinceperm', 'value'),
    State('pds_citymunperm', 'value'),
    State('pds_streetaddressperm', 'value'),
    State('pds_subdvillageperm', 'value'),
    State('pds_brgyaddressperm', 'value'),
    State('pds_zipcodeperm', 'value'),
    State('pds_gsis', 'value'),
    State('pds_pagibig', 'value'),
    State('pds_philhealth', 'value'),
    State('pds_sss', 'value'),
    State('pds_tin', 'value'),
    State('pds_governmentid', 'value'),
    State('pds_govidnumber', 'value'),

    State('url', 'search'),
    State('pds_valid_status', 'value'),

    State('pds_pobislocal', 'value'),
    State('pds_pobprovince', 'value'),
    State('pds_pobcity', 'value'),
    State('pds_pobcountry', 'value'),
    State('sessioncurrentrole', 'data'),




])
def clear_data(pds_submit_summary, pds_load_bp,
               pds_temp_unit,
               pds_title,
               pds_isactive,
               pds_lastname,
               pds_firstname,
               pds_middlename,
               pds_suffixname,
               pds_dob,
               pds_pob,
               pds_sexatbirth,
               pds_civilstatus,
               pds_bloodtype,
               pds_mobilecontactnumber,
               pds_lanecontactnumber,
               pds_email,
               pds_citizenship,
               pds_typeofcit,
               pds_countryofcit,
               pds_addcountrycurr,
               pds_regioncurr,
               pds_aprovincecurr,
               pds_citymuncurrent,
               pds_streetaddresscurr,
               pds_subdvillagecurr,
               pds_brgyaddresscurr,
               pds_zipcodecurr,
               pds_addcountryperm,
               pds_regionperm,
               pds_aprovinceperm,
               pds_citymunperm,
               pds_streetaddressperm,
               pds_subdvillageperm,
               pds_brgyaddressperm,
               pds_zipcodeperm,
               pds_gsis,
               pds_pagibig,
               pds_philhealth,
               pds_sss,
               pds_tin,
               pds_governmentid,
               pds_govidnumber,

               url,
               pds_valid_status,

               pds_pobislocal,
               pds_pobprovince,
               pds_pobcity,
               pds_pobcountry,
               sessioncurrentrole



               ):


    name_disabled = False


    if sessioncurrentrole in [2, 31, 32]:
        name_disabled = True


    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'pds_submit_summary':
            if pds_submit_summary == 2:

                return [
                    pds_temp_unit,
                    pds_title,
                    pds_isactive,
                    pds_lastname,
                    pds_firstname,
                    pds_middlename,
                    pds_suffixname,
                    name_disabled,
                    name_disabled,
                    name_disabled,
                    name_disabled,
                    pds_dob,

                    pds_pob,
                    pds_sexatbirth,
                    pds_civilstatus,
                    pds_bloodtype,
                    pds_mobilecontactnumber,

                    pds_lanecontactnumber,
                    pds_email,
                    pds_citizenship,
                    pds_typeofcit,
                    pds_countryofcit,

                    pds_addcountrycurr,
                    pds_regioncurr,
                    pds_aprovincecurr,
                    pds_citymuncurrent,
                    pds_streetaddresscurr,

                    pds_subdvillagecurr,
                    pds_brgyaddresscurr,
                    pds_zipcodecurr,
                    pds_addcountryperm,
                    pds_regionperm,

                    pds_aprovinceperm,
                    pds_citymunperm,
                    pds_streetaddressperm,
                    pds_subdvillageperm,
                    pds_brgyaddressperm,

                    pds_zipcodeperm,
                    pds_gsis,
                    pds_pagibig,
                    pds_philhealth,
                    pds_sss,

                    pds_tin,
                    pds_governmentid,
                    pds_govidnumber,

                    "",

                    pds_pobislocal,
                    pds_pobprovince,
                    pds_pobcity,
                    pds_pobcountry,

                ]
            elif pds_submit_summary == 1:

                return [
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    date.today(),

                    "",
                    "",
                    "",
                    "",

                    "",
                    "",
                    "",
                    "",
                    "",

                    "",
                    "",
                    "",
                    "",
                    "",

                    "",
                    "",
                    "",
                    "",
                    "",

                    "",
                    "",
                    "",
                    "",
                    "",

                    "",
                    "",
                    "",
                    "",
                    "",

                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",

                ]
            else:
                raise PreventUpdate

        elif eventid == "pds_load_bp" and pds_load_bp == 2 and pds_valid_status == 1:

            parsed = urlparse.urlparse(url)
            uid = str(parse_qs(parsed.query)['uid'][0])

            # sqlcommand = '''SELECT bp.bp_id, person_last_name, person_first_name, person_middle_name,person_name_extension,person_dob,person_pob,
            # person_sex_id,person_civil_status_id,person_blood_type_id,person_citizenship_id,person_citizenship_type_id,person_country_citizenship_id,
            # person_gsis_no, person_pagibig_no, person_philhealth_no, person_sss_no, person_tin,
            # bp_designation_id,bp_salary_grade_id,bp_psi_type_id,bp_effectivity_start_date,bp_effectivity_end_date,bp_unit_code,bp_designation_status_id,
            # bp_credit_units,bp_conditions_appt, bp_justification, p.person_id, p.person_gov_id_type_id, p.person_gov_id_no, bp_emp_class_id
            # FROM persons p INNER JOIN basic_papers bp on bp.person_id = p.person_id
            # INNER JOIN bp_status_changes bsc ON bsc.bp_id = bp.bp_id
            # INNER JOIN bp_statuses bs ON bsc.bp_status_id = bs.bp_status_id
            # INNER JOIN designations d ON d.designation_id = bp.bp_designation_id
            # WHERE bp.bp_id = %s'''

            sqlcommand = '''SELECT person_title_id, person_last_name, person_first_name, person_middle_name,person_name_extension,person_dob,person_pob,
            person_sex_id,person_civil_status_id,person_blood_type_id,person_citizenship_id,person_citizenship_type_id,person_country_citizenship_id,
            person_gsis_no, person_pagibig_no, person_philhealth_no, person_sss_no, person_tin,
            person_id, person_gov_id_type_id, person_gov_id_no,
            person_pob_is_local, person_pob_country_id, person_pob_city_id, person_pob_prov_id, person_temp_unit_id, person_is_active
            FROM persons
            WHERE person_id = %s'''

            values = (uid, )
        #    , designation_name,bp_effectivity_start_date, bp_effectivity_end_date ,bp_status_name
        #     columns = ['bp_id', 'person_last_name', 'person_first_name', 'person_middle_name', 'person_name_extension', 'person_dob', 'person_pob', 'person_sex_id',
        #                'person_civil_status_id', 'person_blood_type_id', 'person_citizenship_id', 'person_citizenship_type_id', 'person_country_citizenship_id',
        #                'person_gsis_no', 'person_pagibig_no', 'person_philhealth_no', 'person_sss_no', 'person_tin',
        #                'bp_designation_id', 'bp_salary_grade_id', 'bp_psi_type_id', 'bp_effectivity_start_date', 'bp_effectivity_end_date', 'bp_unit_code', 'bp_designation_status_id',
        #                'bp_credit_units', 'bp_conditions_appt', 'bp_justification', 'person_id', 'person_gov_id_type_id', 'person_gov_id_no', 'bp_emp_class_id']

            columns = ['person_title_id', 'person_last_name', 'person_first_name', 'person_middle_name', 'person_name_extension', 'person_dob', 'person_pob',
                       'person_sex_id', 'person_civil_status_id', 'person_blood_type_id', 'person_citizenship_id', 'person_citizenship_type_id', 'person_country_citizenship_id',
                       'person_gsis_no', 'person_pagibig_no', 'person_philhealth_no', 'person_sss_no', 'person_tin',
                       'person_id', 'person_gov_id_type_id', 'person_gov_id_no',
                       'person_pob_is_local', 'person_pob_country_id', 'person_pob_city', 'person_pob_prov_id', 'person_temp_unit_id', 'person_is_active']

            df = securequerydatafromdatabase(sqlcommand, values, columns)

            person_title_id = df['person_title_id'][0]
            person_is_active = df['person_is_active'][0]
            pds_lastname = df['person_last_name'][0]
            pds_firstname = df['person_first_name'][0]
            pds_middlename = df['person_middle_name'][0]
            pds_suffixname = df['person_name_extension'][0]
            pds_dob = df['person_dob'][0]
            pds_pob = df['person_pob'][0]
            pds_sexatbirth = df['person_sex_id'][0]
            pds_civilstatus = df['person_civil_status_id'][0]
            pds_bloodtype = df['person_blood_type_id'][0]
            pds_citizenship = df['person_citizenship_id'][0]
            pds_typeofcit = df['person_citizenship_type_id'][0]
            pds_countryofcit = df['person_country_citizenship_id'][0]
            pds_temp_unit = df['person_temp_unit_id'][0]

            pds_gsis = df['person_gsis_no'][0]
            pds_pagibig = df['person_pagibig_no'][0]
            pds_philhealth = df['person_philhealth_no'][0]
            pds_sss = df['person_sss_no'][0]
            pds_tin = df['person_tin'][0]
            pds_governmentid = df['person_gov_id_type_id'][0]
            pds_govidnumber = df['person_gov_id_no'][0]

            pds_pobislocal_proxy = df['person_pob_is_local'][0]

            if pds_pobislocal_proxy:
                pds_pobislocal = 1
            else:
                pds_pobislocal = 2

            pds_pobprovince = df['person_pob_prov_id'][0]
            pds_pobcity = df['person_pob_city'][0]
            pds_pobcountry = df['person_pob_country_id'][0]

            person_id = str(df['person_id'][0])

            sql = '''SELECT address_country_id, address_region_id, address_prov_id, address_city_id, address_street, address_brgy, address_subdivision_village, address_zip_code
                FROM addresses WHERE person_id = %s ORDER BY address_type_id'''
            values = (person_id, )
            columns = ['address_country_id', 'address_region_id', 'address_prov_id', 'address_city_id',
                       'address_street', 'address_brgy', 'address_subdivision_village', 'address_zip_code']
            dfadd = securequerydatafromdatabase(sql, values, columns)

            if not dfadd.empty:
                pds_addcountrycurr = dfadd['address_country_id'][0]
                pds_regioncurr = dfadd['address_region_id'][0]
                pds_aprovincecurr = dfadd['address_prov_id'][0]
                pds_citymuncurrent = dfadd['address_city_id'][0]
                pds_streetaddresscurr = dfadd['address_street'][0]
                pds_subdvillagecurr = dfadd['address_subdivision_village'][0]
                pds_brgyaddresscurr = dfadd['address_brgy'][0]
                pds_zipcodecurr = dfadd['address_zip_code'][0]
                pds_addcountryperm = dfadd['address_country_id'][1]
                pds_regionperm = dfadd['address_region_id'][1]
                pds_aprovinceperm = dfadd['address_prov_id'][1]
                pds_citymunperm = dfadd['address_city_id'][1]
                pds_streetaddressperm = dfadd['address_street'][1]
                pds_subdvillageperm = dfadd['address_subdivision_village'][1]
                pds_brgyaddressperm = dfadd['address_brgy'][1]
                pds_zipcodeperm = dfadd['address_zip_code'][1]
            else:
                pds_addcountrycurr = ""
                pds_regioncurr = ""
                pds_aprovincecurr = ""
                pds_citymuncurrent = ""
                pds_streetaddresscurr = ""
                pds_subdvillagecurr = ""
                pds_brgyaddresscurr = ""
                pds_zipcodecurr = ""
                pds_addcountryperm = ""
                pds_regionperm = ""
                pds_aprovinceperm = ""
                pds_citymunperm = ""
                pds_streetaddressperm = ""
                pds_subdvillageperm = ""
                pds_brgyaddressperm = ""
                pds_zipcodeperm = ""

            sql = '''SELECT person_email_address FROM person_email_addresses WHERE person_id = %s'''
            values = (person_id, )
            columns = ['person_email_address']
            dfemail = securequerydatafromdatabase(sql, values, columns)

            if len(dfemail['person_email_address']) == 0:

                pds_email = ""
            else:
                pds_email = dfemail['person_email_address'][0]

            sql = '''SELECT person_contact_number FROM person_contact_numbers WHERE person_id = %s ORDER BY person_contact_type_id'''
            values = (person_id, )
            columns = ['person_contact_number']
            dfcontactdetails = securequerydatafromdatabase(sql, values, columns)
            if len(dfcontactdetails['person_contact_number']) == 0:
                pds_lanecontactnumber = ""
                pds_mobilecontactnumber = ""

            else:

                pds_lanecontactnumber = dfcontactdetails['person_contact_number'][0]
                pds_mobilecontactnumber = dfcontactdetails['person_contact_number'][1]


            return [
                pds_temp_unit,
                person_title_id,
                person_is_active,
                pds_lastname,
                pds_firstname,
                pds_middlename,
                pds_suffixname,
                name_disabled,
                name_disabled,
                name_disabled,

                name_disabled,
                pds_dob,
                pds_pob,
                pds_sexatbirth,
                pds_civilstatus,
                pds_bloodtype,
                pds_mobilecontactnumber,
                pds_lanecontactnumber,
                pds_email,
                pds_citizenship,

                pds_typeofcit,
                pds_countryofcit,
                pds_addcountrycurr,
                pds_regioncurr,
                pds_aprovincecurr,
                pds_citymuncurrent,
                pds_streetaddresscurr,
                pds_subdvillagecurr,
                pds_brgyaddresscurr,
                pds_zipcodecurr,

                pds_addcountryperm,
                pds_regionperm,
                pds_aprovinceperm,
                pds_citymunperm,
                pds_streetaddressperm,
                pds_subdvillageperm,
                pds_brgyaddressperm,
                pds_zipcodeperm,
                pds_gsis,
                pds_pagibig,

                pds_philhealth,
                pds_sss,
                pds_tin,
                pds_governmentid,
                pds_govidnumber,
                person_id,
                pds_pobislocal,
                pds_pobprovince,
                pds_pobcity,
                pds_pobcountry

            ]
            # raise PreventUpdate
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback(
    [Output("pds_modal_bp_select_eligibility", "is_open"),
     Output("pds_currenteligibilitiesdiv", "children"),
     Output('sessioneligibilities', "data"),
     Output('sessioneligibilitiesprocessed', "data"),
     Output('sessionpersoneligibilitiescid', "data"),
     Output('pds_eligibilities_checkbox', "checked"),
     Output('pds_elig_summary', 'value')
     ],
    [Input("pds_btn_add_eligibilities", "n_clicks"),
     Input("pds_btn_delete_eligibilities", "n_clicks"),
     Input("pds_modal_bp_eligibility_close", "n_clicks"),
     Input("modal_bp_eligibility_cancel", "n_clicks"),
     Input("pds_load_bp", "value"),
     Input({'type': 'pds_dynamiceligedit', 'index': ALL}, 'n_clicks'),
     Input({'type': 'pds_dynamiceligdelete', 'index': ALL}, 'n_clicks'),
     ],
    [State("pds_modal_bp_select_eligibility", "is_open"),
        State("pds_eligibility", "value"),
        State("pds_eligibilityrating", "value"),
        State("pds_eligibility_date_of_exam", "date"),
        State("pds_placeofconferment", "value"),
        State("pds_licensenumber", "value"),
        State("pds_eligibilitystartdate", "date"),
        State("pds_eligibilityenddate", "date"),
        State("pds_eligibility", "options"),
        State('sessioneligibilities', "data"),
        State('sessioneligibilitiesprocessed', "data"),
        State("pds_currenteligibilitiesdiv", "children"),
        State("url", "search"),
        State('sessionpersoneligibilitiescid', "data"),
        State("sessionpersonid", 'data'),
        State('current_user_id', 'data'),
        State('pds_elig_id_store', 'value'),
        State('pds_elig_summary', 'value')
     ],
)
def toggle_modal_elig(pds_btn_add_eligibilities, pds_btn_delete_eligibilities, pds_modal_bp_eligibility_close, modal_bp_eligibility_cancel, pds_load_bp,
                        pds_dynamiceligedit, pds_dynamiceligdelete,
                         pds_modal_bp_select_eligibility_is_open,
                         pds_eligibility, pds_eligibilityrating, pds_eligibility_date_of_exam, pds_placeofconferment, pds_licensenumber, pds_eligibilitystartdate, pds_eligibilityenddate, pds_eligibilityoptions,
                         sessioneligibilities, sessioneligibilitiesprocessed, pds_currenteligibilitiesdiv, url, sessionpersoneligibilitiescid, person_id, current_user_id,
                         pds_elig_id_store, pds_elig_summary):

    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if eventid == 'pds_btn_add_eligibilities' or "pds_dynamiceligedit" in str(eventid):#Add Elig Button (Open modal)
            # df = pd.DataFrame.from_dict(sessiondegreesprocessed, orient='columns')
            # if len(sessiondegreesprocessed)>0:
            #     df = addcheckboxtocolumn(df)
            # table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

            df = pd.DataFrame.from_dict(sessioneligibilitiesprocessed, orient='columns')
            editbtncol = {}
            deletebtncol = {}

            for index, row in df.iterrows():
                editbtncol[index] = dbc.Button("Edit", id={'index': index, 'type': 'pds_dynamiceligedit'},
                                               color='primary')
                deletebtncol[index] = dbc.Button("Delete", id={'index': index, 'type': 'pds_dynamiceligdelete'},
                                                 color='primary')
            data_dict = df.to_dict()
            dictionarydata = {'Edit': editbtncol}
            dictionarydata2 = {'Delete': deletebtncol}
            data_dict.update(dictionarydata)
            data_dict.update(dictionarydata2)
            df = pd.DataFrame.from_dict(data_dict)
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

            if eventid == 'pds_btn_add_eligibilities':
                pds_elig_summary = -1
            else:
                index = json.loads(eventid)["index"]

                pds_elig_summary = index

            return [True, table, sessioneligibilities, sessioneligibilitiesprocessed, sessionpersoneligibilitiescid, False, pds_elig_summary]

        elif "pds_dynamiceligdelete" in str(eventid):

            index = json.loads(eventid)["index"]


            del sessioneligibilitiesprocessed[index]
            del sessioneligibilities[index]

            df = pd.DataFrame.from_dict(sessioneligibilitiesprocessed, orient='columns')

            editbtncol = {}
            deletebtncol = {}

            for index, row in df.iterrows():

                editbtncol[index] = dbc.Button("Edit", id={'index': index, 'type': 'pds_dynamiceligedit'},
                                               color='primary')
                deletebtncol[index] = dbc.Button("Delete", id={'index': index, 'type': 'pds_dynamiceligdelete'},
                                                 color='primary')
            data_dict = df.to_dict()
            dictionarydata = {'Edit': editbtncol}
            dictionarydata2 = {'Delete': deletebtncol}
            data_dict.update(dictionarydata)
            data_dict.update(dictionarydata2)
            df = pd.DataFrame.from_dict(data_dict)

            # df = pd.DataFrame.from_dict(sessiondegreesprocessed, orient='columns')

            # if len(sessiondegreesprocessed) > 0:
            #     df = addcheckboxtocolumn(df)
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

            return [False, table, sessioneligibilities, sessioneligibilitiesprocessed, sessionpersoneligibilitiescid, False, pds_elig_summary]

        elif eventid == 'pds_modal_bp_eligibility_close':


            if pds_eligibility:

                pds_eligibilityname = [(i, d) for i, d in enumerate(
                    pds_eligibilityoptions) if pds_eligibility in d.values()]
                if pds_eligibilityname:
                    pds_eligibilityname = pds_eligibilityname[0][1]['label']

                pds_placeofconferment = safeupper(pds_placeofconferment)

                if pds_elig_id_store == -1:

                    degree = [(i, d) for i, d in enumerate(pds_eligibilityoptions) if pds_eligibility in d.values()]
                    if degree:
                        degree = degree[0][1]['label']
                    new_row = {'Eligibility': pds_eligibilityname, 'Rating': pds_eligibilityrating,
                               'Date of Exam': pds_eligibility_date_of_exam,
                               'Place of Conferment': pds_placeofconferment, 'License Number': pds_licensenumber,
                               'Eligibility Effective Start Date': pds_eligibilitystartdate,
                               "Eligibility Effective End Date": pds_eligibilityenddate}
                    sessioneligibilitiesprocessed.append(new_row)
                    new_row_raw = {'Eligibility': pds_eligibility, 'Rating': pds_eligibilityrating,
                                   'Date of Exam': pds_eligibility_date_of_exam,
                                   'Place of Conferment': pds_placeofconferment, 'License Number': pds_licensenumber,
                                   'Eligibility Effective Start Date': pds_eligibilitystartdate,
                                   "Eligibility Effective End Date": pds_eligibilityenddate}
                    sessioneligibilities.append(new_row_raw)

                elif pds_elig_id_store >= -1:


                    degree = [(i, d) for i, d in enumerate(pds_eligibilityoptions) if pds_eligibility in d.values()]
                    if degree:
                        degree = degree[0][1]['label']


                    if sessioneligibilities[pds_elig_id_store].get("Eligibility ID") is not None:

                        new_row = {'Eligibility ID': sessioneligibilities[pds_elig_id_store].get("Eligibility ID"), 'Eligibility': pds_eligibilityname, 'Rating': pds_eligibilityrating,
                                   'Date of Exam': pds_eligibility_date_of_exam,
                                   'Place of Conferment': pds_placeofconferment, 'License Number': pds_licensenumber,
                                   'Eligibility Effective Start Date': pds_eligibilitystartdate,
                                   "Eligibility Effective End Date": pds_eligibilityenddate}


                        new_row_raw = {'Eligibility ID': sessioneligibilities[pds_elig_id_store].get("Eligibility ID"),
                                       'Eligibility': pds_eligibility, 'Rating': pds_eligibilityrating,
                                       'Date of Exam': pds_eligibility_date_of_exam,
                                       'Place of Conferment': pds_placeofconferment,
                                       'License Number': pds_licensenumber,
                                       'Eligibility Effective Start Date': pds_eligibilitystartdate,
                                       "Eligibility Effective End Date": pds_eligibilityenddate}
                    else:
                        new_row = {'Eligibility': pds_eligibilityname, 'Rating': pds_eligibilityrating,
                                   'Date of Exam': pds_eligibility_date_of_exam,
                                   'Place of Conferment': pds_placeofconferment, 'License Number': pds_licensenumber,
                                   'Eligibility Effective Start Date': pds_eligibilitystartdate,
                                   "Eligibility Effective End Date": pds_eligibilityenddate}

                        new_row_raw = {'Eligibility': pds_eligibility, 'Rating': pds_eligibilityrating,
                                       'Date of Exam': pds_eligibility_date_of_exam,
                                       'Place of Conferment': pds_placeofconferment,
                                       'License Number': pds_licensenumber,
                                       'Eligibility Effective Start Date': pds_eligibilitystartdate,
                                       "Eligibility Effective End Date": pds_eligibilityenddate}

                    sessioneligibilitiesprocessed.append(new_row)
                    sessioneligibilities.append(new_row_raw)

                    del sessioneligibilitiesprocessed[pds_elig_summary]
                    del sessioneligibilities[pds_elig_summary]

                df = pd.DataFrame.from_dict(sessioneligibilitiesprocessed, orient='columns')
                editbtncol = {}
                deletebtncol = {}

                for index, row in df.iterrows():
                    editbtncol[index] = dbc.Button("Edit", id={'index': index, 'type': 'pds_dynamiceligedit'},
                                                   color='primary')
                    deletebtncol[index] = dbc.Button("Delete", id={'index': index, 'type': 'pds_dynamiceligdelete'},
                                                     color='primary')
                data_dict = df.to_dict()
                dictionarydata = {'Edit': editbtncol}
                dictionarydata2 = {'Delete': deletebtncol}
                data_dict.update(dictionarydata)
                data_dict.update(dictionarydata2)
                df = pd.DataFrame.from_dict(data_dict)

                df = pd.DataFrame.from_dict(sessioneligibilitiesprocessed, orient='columns')

                editbtncol = {}
                deletebtncol = {}

                for index, row in df.iterrows():
                    editbtncol[index] = dbc.Button("Edit", id={'index': index, 'type': 'pds_dynamiceligedit'},
                                                   color='primary')
                    deletebtncol[index] = dbc.Button("Delete", id={'index': index, 'type': 'pds_dynamiceligdelete'},
                                                     color='primary')
                data_dict = df.to_dict()
                dictionarydata = {'Edit': editbtncol}
                dictionarydata2 = {'Delete': deletebtncol}
                data_dict.update(dictionarydata)
                data_dict.update(dictionarydata2)
                df = pd.DataFrame.from_dict(data_dict)

                # if len(sessioneligibilitiesprocessed) > 0:
                #     df = addcheckboxtocolumn(df)
                table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)



                return [False, table, sessioneligibilities, sessioneligibilitiesprocessed, sessionpersoneligibilitiescid, False, pds_elig_summary]
            else:
                df = pd.DataFrame.from_dict(sessioneligibilitiesprocessed, orient='columns')
                editbtncol = {}
                deletebtncol = {}

                for index, row in df.iterrows():
                    editbtncol[index] = dbc.Button("Edit", id={'index': index, 'type': 'pds_dynamiceligedit'},
                                                   color='primary')
                    deletebtncol[index] = dbc.Button("Delete", id={'index': index, 'type': 'pds_dynamiceligdelete'},
                                                     color='primary')
                data_dict = df.to_dict()
                dictionarydata = {'Edit': editbtncol}
                dictionarydata2 = {'Delete': deletebtncol}
                data_dict.update(dictionarydata)
                data_dict.update(dictionarydata2)
                df = pd.DataFrame.from_dict(data_dict)
                # if len(sessioneligibilitiesprocessed) > 0:
                #     df = addcheckboxtocolumn(df)
                table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

                return [True, table, sessioneligibilities, sessioneligibilitiesprocessed, sessionpersoneligibilitiescid, False, pds_elig_summary]
        elif eventid == 'modal_bp_eligibility_cancel':

            df = pd.DataFrame.from_dict(sessioneligibilitiesprocessed, orient='columns')
            editbtncol = {}
            deletebtncol = {}

            for index, row in df.iterrows():
                editbtncol[index] = dbc.Button("Edit", id={'index': index, 'type': 'pds_dynamiceligedit'},
                                               color='primary')
                deletebtncol[index] = dbc.Button("Delete", id={'index': index, 'type': 'pds_dynamiceligdelete'},
                                                 color='primary')
            data_dict = df.to_dict()
            dictionarydata = {'Edit': editbtncol}
            dictionarydata2 = {'Delete': deletebtncol}
            data_dict.update(dictionarydata)
            data_dict.update(dictionarydata2)
            df = pd.DataFrame.from_dict(data_dict)
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

            return [False, table, sessioneligibilities, sessioneligibilitiesprocessed, sessionpersoneligibilitiescid, False, pds_elig_summary]

        elif eventid in ['pds_btn_delete_eligibilities']:
            rowstodelete = returnselectedrows(pds_currenteligibilitiesdiv, 8)
            parsed = urlparse.urlparse(url)
            mode = str(parse_qs(parsed.query)['mode'][0])

            #
            if mode == "edit":
                uid = str(parse_qs(parsed.query)['uid'][0])

            #
                eligibilitieslist = []
                for index in range(len(sessioneligibilitiesprocessed)):
                    if index in rowstodelete:
                        eligibilitieslist.append(sessioneligibilities[index])

                for item in eligibilitieslist:

                    sql1 = '''
                                SELECT eligibility_id
                                FROM eligibilities
                                WHERE eligibility_code = %s
                                AND eligibility_delete_ind = %s

                            '''

                    values1 = (item["Eligibility"], False)
                    columns1 = ['eligibility_id']
                    df1 = securequerydatafromdatabase(sql1, values1, columns1)

                    eligibility_id = int(df1["eligibility_id"][0])

                    sqlbpfields = """
                        UPDATE person_eligibilities SET person_eligibility_delete_ind=%s
                        WHERE person_id=%s and eligibility_id=%s
                    """
                    bpfields = [True, person_id, eligibility_id]
                    modifydatabase(sqlbpfields, bpfields)

            processedlist = []
            for index in range(len(sessioneligibilitiesprocessed)):
                if index not in rowstodelete:
                    processedlist.append(sessioneligibilitiesprocessed[index])
            sessioneligibilitiesprocessed = processedlist
            processedlist2 = []
            for index in range(len(sessioneligibilities)):
                if index not in rowstodelete:
                    processedlist2.append(sessioneligibilities[index])
            sessioneligibilities = processedlist2

            df = pd.DataFrame.from_dict(sessioneligibilitiesprocessed, orient='columns')
            editbtncol = {}
            deletebtncol = {}

            for index, row in df.iterrows():
                editbtncol[index] = dbc.Button("Edit", id={'index': index, 'type': 'pds_dynamiceligedit'},
                                               color='primary')
                deletebtncol[index] = dbc.Button("Delete", id={'index': index, 'type': 'pds_dynamiceligdelete'},
                                                 color='primary')
            data_dict = df.to_dict()
            dictionarydata = {'Edit': editbtncol}
            dictionarydata2 = {'Delete': deletebtncol}
            data_dict.update(dictionarydata)
            data_dict.update(dictionarydata2)
            df = pd.DataFrame.from_dict(data_dict)
            # if len(sessioneligibilitiesprocessed) > 0:
            #     df = addcheckboxtocolumn(df)
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)
            return [False, table, sessioneligibilities, sessioneligibilitiesprocessed, sessionpersoneligibilitiescid, False, pds_elig_summary]

        elif eventid == "pds_load_bp" and pds_load_bp == 2:#pageload

            parsed = urlparse.urlparse(url)
            uid = str(parse_qs(parsed.query)['uid'][0])
            person_id = uid
            sql = '''
            SELECT pe.person_eligibility_id, e.eligibility_id, e.eligibility_code, pe.person_eligibility_rating, pe.person_eligibility_taken, pe.person_eligibility_poe, pe.person_eligibility_license_no, pe.person_eligibility_valid_start_date,
            pe.person_eligibility_valid_end_date
            FROM person_eligibilities pe
            INNER JOIN eligibilities e ON e.eligibility_id = pe.eligibility_id
            WHERE pe.person_id = %s and pe.person_eligibility_delete_ind = %s
            '''

            values = (int(person_id), False)

            columns = ['person_eligibility_id', 'eligilibity_id', 'eligibility_code', 'person_eligibility_rating', 'person_eligibility_taken', 'person_eligibility_poe', 'person_eligibility_license_no', 'person_eligibility_valid_start_date',
                       'person_eligibility_valid_end_date']

            df = securequerydatafromdatabase(sql, values, columns)

            dfsessioneligibilities = df[['person_eligibility_id', 'eligilibity_id', 'person_eligibility_rating', 'person_eligibility_taken', 'person_eligibility_poe',
                                         'person_eligibility_license_no', 'person_eligibility_valid_start_date', 'person_eligibility_valid_end_date']].copy()
            dfsessioneligibilities.columns = ["Eligibility ID", "Eligibility", "Rating", "Date of Exam", "Place of Conferment",
                                              "License Number", "Eligibility Effective Start Date", "Eligibility Effective End Date"]
            sessioneligibilities = dfsessioneligibilities.to_dict('records')

            sessioneligibilitiesprocesseddf = df[['person_eligibility_id','eligibility_code', 'person_eligibility_rating', 'person_eligibility_taken', 'person_eligibility_poe',
                                                  'person_eligibility_license_no', 'person_eligibility_valid_start_date', 'person_eligibility_valid_end_date']].copy()
            sessioneligibilitiesprocesseddf.columns = ['Eligibility ID', "Eligibility", "Rating", "Date of Exam", "Place of Conferment",
                                                       "License Number", "Eligibility Effective Start Date", "Eligibility Effective End Date"]
            #table = sessioneligibilitiesprocesseddf
            sessioneligibilitiesprocessed = sessioneligibilitiesprocesseddf.to_dict('records')
            sessioneligibilitiesprocesseddf = pd.DataFrame.from_dict(sessioneligibilitiesprocessed, orient='columns')

            if len(sessioneligibilitiesprocessed) > 0:
                pds_eligibilities_checkbox_checked = False
                # sessioneligibilitiesprocesseddf = addcheckboxtocolumn(
                #     sessioneligibilitiesprocesseddf)
            elif len(sessioneligibilitiesprocessed) == 0:
                pds_eligibilities_checkbox_checked = True

            tabledf = sessioneligibilitiesprocesseddf.copy()
            editbtncol = {}
            deletebtncol = {}

            for index, row in tabledf.iterrows():
                editbtncol[index] = dbc.Button("Edit", id={'index': index, 'type': 'pds_dynamiceligedit'}, color = 'primary')
                deletebtncol[index] = dbc.Button("Delete", id={'index': index, 'type': 'pds_dynamiceligdelete'}, color = 'primary')
            data_dict = tabledf.to_dict()
            dictionarydata = {'Edit': editbtncol}
            dictionarydata2 = {'Delete': deletebtncol}
            data_dict.update(dictionarydata)
            data_dict.update(dictionarydata2)
            tabledf = pd.DataFrame.from_dict(data_dict)

            table = dbc.Table.from_dataframe(
                tabledf, striped=True, bordered=True, hover=True)
            sessionpersoneligibilitiescid = df['person_eligibility_id'].to_list()

            return [False, table, sessioneligibilities, sessioneligibilitiesprocessed, sessionpersoneligibilitiescid, pds_eligibilities_checkbox_checked, pds_elig_summary]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback([
    Output('pds_eligibilitystartdate', 'max_date_allowed'),
],
    [
    Input('pds_eligibilityenddate', 'date'),
],
)
def elig_mindate_pds_eligibilitystartdate(pds_eligibilityenddate):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'pds_eligibilityenddate':
            return [pds_eligibilityenddate]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback([
    Output('pds_eligibilityenddate', 'min_date_allowed'),
],
    [
    Input('pds_eligibilitystartdate', 'date'),
],
)
def elig_mindate_pds_eligibilityenddate(pds_eligibilitystartdate):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'pds_eligibilitystartdate':
            return [pds_eligibilitystartdate]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


def insert_eligibilities(eligibilitieslist, person_id, current_user_id):

    # pds_lastname = pds_lastname.upper()

    entryidlist = []
    for i in eligibilitieslist:
        if i.get('Eligibility ID') is not None:
            entryidlist.append(i['Eligibility ID'])


    sql8 = '''
            SELECT person_eligibility_id
            FROM person_eligibilities
            WHERE person_id = %s
            AND person_eligibility_delete_ind = %s

        '''

    values8 = (person_id, False)
    columns8 = ['person_eligibility_id']
    dfexistingeligids = securequerydatafromdatabase(sql8, values8, columns8)
    dfexistingeligids_list = dfexistingeligids['person_eligibility_id'].tolist()

    for i in dfexistingeligids_list:
        if i not in entryidlist:
            sqldeleteelig = '''
                UPDATE person_eligibilities
                SET person_eligibility_delete_ind = %s
                WHERE person_eligibility_id = %s
            '''
            valuesdelete = (True, i)

            modifydatabase(sqldeleteelig, valuesdelete)


    for i in range(0, len(eligibilitieslist)):
        dict_temp = eligibilitieslist[i]
        if dict_temp.get('Eligibility ID') is None:

            sqleligibilitiesnew = """
                INSERT INTO person_eligibilities(eligibility_id,  person_eligibility_rating, person_eligibility_taken,
                    person_eligibility_poe, person_eligibility_license_no, person_eligibility_valid_start_date, person_eligibility_valid_end_date,
                    person_id, person_eligibility_inserted_by,
                     person_eligibility_inserted_on, person_eligibility_delete_ind)
                VALUES (%s, %s, %s,
                %s, %s, %s, %s,
                %s,%s,
                %s, %s)

            """

            if len(str(dict_temp.get('Rating'))) == 0:
                dict_temp['Rating'] = None


            valuesnew = (dict_temp['Eligibility'], dict_temp['Rating'], dict_temp['Date of Exam'] ,
                         dict_temp['Place of Conferment'], dict_temp['License Number'], dict_temp['Eligibility Effective Start Date'], dict_temp['Eligibility Effective End Date'],
                         person_id, current_user_id, datetime.now(), False)
            modifydatabase(sqleligibilitiesnew, valuesnew)

        else:

            sqleligibilities2 = """
                UPDATE person_eligibilities

                SET eligibility_id = %s, person_eligibility_rating = %s, person_eligibility_taken = %s,
                    person_eligibility_poe = %s, person_eligibility_license_no = %s, person_eligibility_valid_start_date = %s, person_eligibility_valid_end_date = %s
                WHERE person_eligibility_id = %s

            """

            values2 = (dict_temp['Eligibility'], dict_temp['Rating'], dict_temp['Date of Exam'],
                       dict_temp['Place of Conferment'], dict_temp['License Number'], dict_temp['Eligibility Effective Start Date'], dict_temp['Eligibility Effective End Date'],
                        dict_temp['Eligibility ID'])

            modifydatabase(sqleligibilities2, values2)




    # eligibilitiesdf = pd.DataFrame(eligibilitiesdict)
    # eligibilitiesdf = eligibilitiesdf.values.tolist()
    # finaleligibilities = []
    # for item in eligibilitiesdf:
    #     item.append(person_id)
    #     item.append(current_user_id)
    #     item.append(datetime.now())
    #     item.append(False)
    #     finaleligibilities.append(item)
    # bulkmodifydatabase(sqleligibilities, finaleligibilities)

#
#
# @app.callback([Output('pds_maindiv', 'style'),
#                Output('pds_valid_status', 'value')
#                ],
#               [
#     Input('url', 'pathname'),
# ], [
#                   State('sessioncurrentunit', 'data'),
#                   State('sessionlistofunits', 'data'),
#                   State("url", "search"),
#                 State('pds_valid_status', 'value')
# ])
# def pds_unit_security(url, sessioncurrentunit, sessionlistofunits, search, pds_valid_status):
#
#     parsed = urlparse.urlparse(search)
#     if url == "/settings/settings_personal_data_profile":
#         mode = str(parse_qs(parsed.query)['mode'][0])
#         if mode == "edit":
#             person_id = str(parse_qs(parsed.query)['uid'][0])
#
#
#             sqlcommand = '''SELECT e.emp_primary_home_unit_id
#                             FROM persons p
#                             INNER JOIN employees e ON p.person_id = e.person_id
#                             WHERE p.person_id = %s
#             '''
#
#             values = (person_id,)
#             columns = ['emp_primary_home_unit_id']
#             df = securequerydatafromdatabase(sqlcommand, values, columns)
#
#             if not df.empty:
#                 if df["emp_primary_home_unit_id"][0] in sessionlistofunits[str(sessioncurrentunit)]:
#
#                     pds_valid_status = 1
#                     style = {'display': 'inline'}
#
#                 else:
#
#                     pds_valid_status = 0
#                     style = {'display': 'none'}
#
#             else:
#                 sqlcommand2 = '''SELECT person_temp_unit_id
#                                 FROM persons p
#                                 WHERE p.person_id = %s
#                             '''
#
#                 values2 = (person_id,)
#                 columns2 = ['person_temp_unit_id']
#                 df2 = securequerydatafromdatabase(sqlcommand2, values2, columns2)
#
#                 if df2["person_temp_unit_id"][0] in sessionlistofunits[str(sessioncurrentunit)]:
#
#                     pds_valid_status = 1
#                     style = {'display': 'inline'}
#
#                 else:
#
#                     pds_valid_status = 0
#                     style = {'display': 'none'}
#
#
#
#             return [style, pds_valid_status]
#         else:
#             raise PreventUpdate
#     else:
#         raise PreventUpdate


@app.callback(
    [
        Output("pds_oldcollapse", "is_open"),

        Output("pds_oldtitle", "children"),
        Output("pds_oldsex", "children"),
        Output("pds_olddob", "children"),
        Output("pds_oldcstat", "children"),
        Output("pds_oldcitizenship", "children"),
        Output("pds_oldbltype", "children"),

        Output("pds_oldtin", "children"),
        Output("pds_oldotherq", "children"),
        Output("pds_oldencode", "children"),
        Output("pds_oldhrmo", "children"),
        Output("pds_oldrem", "children"),
        Output("pds_oldcreatedat", "children"),

        Output("pds_oldupdatedat", "children"),
        Output("pds_oldapptclean", "children"),
        Output("pds_oldapptremarks", "children"),
        Output("pds_oldapptname", "children"),
        Output("pds_oldtimestamp", "children"),
        Output("pds_oldleaveclean", "children"),

        Output("pds_oldleaveremarks", "children"),
        Output("pds_oldleavename", "children"),
        Output("pds_oldleavetimestamp", "children"),
        Output("pds_oldsysclean", "children"),
        Output("pds_oldsysremarks", "children"),
        Output("pds_oldsystimestamp", "children"),

        Output("pds_oldleaveremarks2", "children"),
        Output("pds_oldleaveremarks3", "children"),
        Output("pds_oldaddress", "children"),

        Output("pds_oldwhr", "children"),
        Output("pds_oldeduc", "children"),
        Output("pds_oldmajor", "children"),
        Output("pds_oldwhn", "children"),

        Output("pds_oldcse", "children"),
        Output("pds_oldcseyear", "children"),
        Output("pds_oldrating", "children"),

    ],
    [
        Input("pds_oldvaluesbtn", "n_clicks")
    ],
    [
        State("pds_oldcollapse", "is_open"),
        State("url", "search")

    ]
)
def load_old_emp_values(pds_oldvaluesbtn, pds_oldcollapse, url):
    ctx = dash.callback_context

    parsed = urlparse.urlparse(url)
    mode = str(parse_qs(parsed.query)['mode'][0])

    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'pds_oldvaluesbtn':
            if mode == "edit":
                person_id = str(parse_qs(parsed.query)['uid'][0])

                sql1 = '''
                    SELECT person_old_title, person_old_sex, person_old_bday, person_old_cstat, person_old_citizenship, person_old_bl_type,
                                person_old_tin, person_old_other_q, person_old_encode, person_old_hrmo, person_old_rem, person_old_created_at,
                                person_old_updated_at, person_old_appt_clean, person_old_appt_remarks, person_old_appt_name, person_old_appt_timestamp, person_old_leave_clean,
                                person_old_leave_remarks, person_old_leave_name, person_old_leave_timestamp, person_old_sys_clean, person_old_sys_remarks, person_old_sys_timestamp,
                                person_old_leave_remarks2, person_old_leave_remarks3

                    FROM persons
                    WHERE person_id = %s
                '''

                values1 = (person_id, )
                columns1 = ['person_old_title', 'person_old_sex', 'person_old_bday', 'person_old_cstat', 'person_old_citizenship', 'person_old_bl_type',
                            'person_old_tin', 'person_old_other_q', 'person_old_encode', 'person_old_hrmo', 'person_old_rem', 'person_old_created_at',
                            'person_old_updated_at', 'person_old_appt_clean', 'person_old_appt_remarks', 'person_old_appt_name', 'person_old_appt_timestamp', 'person_old_leave_clean',
                            'person_old_leave_remarks', 'person_old_leave_name', 'person_old_leave_timestamp', 'person_old_sys_clean', 'person_old_sys_remarks', 'person_old_sys_timestamp',
                            'person_old_leave_remarks2', 'person_old_leave_remarks3']
                df1 = securequerydatafromdatabase(sql1, values1, columns1)

                person_old_title = df1["person_old_title"][0]
                person_old_sex = df1["person_old_sex"][0]
                person_old_bday = df1["person_old_bday"][0]
                person_old_cstat = df1["person_old_cstat"][0]
                person_old_citizenship = df1["person_old_citizenship"][0]
                person_old_bl_type = df1["person_old_bl_type"][0]

                person_old_tin = df1["person_old_tin"][0]
                person_old_other_q = df1["person_old_other_q"][0]
                person_old_encode = df1["person_old_encode"][0]
                person_old_hrmo = df1["person_old_hrmo"][0]
                person_old_rem = df1["person_old_rem"][0]
                person_old_created_at = df1["person_old_created_at"][0]

                person_old_updated_at = df1["person_old_updated_at"][0]
                person_old_appt_clean = df1["person_old_appt_clean"][0]
                person_old_appt_remarks = df1["person_old_appt_remarks"][0]
                person_old_appt_name = df1["person_old_appt_name"][0]
                person_old_appt_timestamp = df1["person_old_appt_timestamp"][0]
                person_old_leave_clean = df1["person_old_leave_clean"][0]

                person_old_leave_remarks = df1["person_old_leave_remarks"][0]
                person_old_leave_name = df1["person_old_leave_name"][0]
                person_old_leave_timestamp = df1["person_old_leave_timestamp"][0]
                person_old_sys_clean = df1["person_old_sys_clean"][0]
                person_old_sys_remarks = df1["person_old_sys_remarks"][0]
                person_old_sys_timestamp = df1["person_old_sys_timestamp"][0]

                person_old_leave_remarks2 = df1["person_old_leave_remarks2"][0]
                person_old_leave_remarks3 = df1["person_old_leave_remarks3"][0]

                sql2 = '''
                                    SELECT person_old_address
                                    FROM addresses
                                    WHERE person_id = %s
                                '''

                values2 = (person_id,)
                columns2 = ['person_old_address']
                df2 = securequerydatafromdatabase(sql2, values2, columns2)

                person_old_address = df2["person_old_address"][0]

                sql3 = '''
                    SELECT person_old_whr, person_old_educ, person_old_major, person_old_whn
                    FROM person_educational_backgrounds
                    WHERE person_id = %s
                '''

                values3 = (person_id,)
                columns3 = ['person_old_whr', 'person_old_educ',
                            'person_old_major', 'person_old_whn']
                df3 = securequerydatafromdatabase(sql3, values3, columns3)

                person_old_whr = df3["person_old_whr"][0]
                person_old_educ = df3["person_old_educ"][0]
                person_old_major = df3["person_old_major"][0]
                person_old_whn = df3["person_old_whn"][0]

                sql4 = '''
                            SELECT person_old_cse, person_old_cse_year, person_eligibility_old_rating
                            FROM person_eligibilities
                            WHERE person_id = %s
                        '''

                values4 = (person_id,)
                columns4 = ['person_old_cse', 'person_old_cse_year',
                            'person_eligibility_old_rating']
                df4 = securequerydatafromdatabase(sql4, values4, columns4)

                person_old_cse = df4["person_old_cse"][0]
                person_old_cse_year = df4["person_old_cse_year"][0]
                person_eligibility_old_rating = df4["person_eligibility_old_rating"][0]

                return [not pds_oldcollapse,
                        person_old_title, person_old_sex, person_old_bday, person_old_cstat, person_old_citizenship, person_old_bl_type,
                        person_old_tin, person_old_other_q, person_old_encode, person_old_hrmo, person_old_rem, person_old_created_at,
                        person_old_updated_at, person_old_appt_clean, person_old_appt_remarks, person_old_appt_name, person_old_appt_timestamp, person_old_leave_clean,
                        person_old_leave_remarks, person_old_leave_name, person_old_leave_timestamp, person_old_sys_clean, person_old_sys_remarks, person_old_sys_timestamp,
                        person_old_leave_remarks2, person_old_leave_remarks3, person_old_address,
                        person_old_whr, person_old_educ, person_old_major, person_old_whn,
                        person_old_cse, person_old_cse_year, person_eligibility_old_rating]

            else:
                raise PreventUpdate
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback(
    [
        Output('pds_pobproxy1', 'style'),
        Output('pds_pobproxy2', 'style'),
        Output('pds_pobproxy3', 'style'),
        Output('pds_pobproxy4', 'style'),
        Output('pds_pobproxy5', 'style'),
        Output('pds_pobproxy6', 'style'),


    ],
    [
        Input('pds_pobislocal', 'value')
    ]
)
def formatpob(pds_pobislocal):
    if pds_pobislocal == 1:
        return [{'display': 'none'}, {'display': 'none'}, {'display': 'inline'},
                {'display': 'inline'}, {'display': 'none'}, {'display': 'none'}]
    elif pds_pobislocal == 2:
        return [{'display': 'none'}, {'display': 'none'}, {'display': 'none'},
                {'display': 'none'}, {'display': 'inline'}, {'display': 'inline'}]

    else:
        raise PreventUpdate

# @app.callback(
#     [
#         Output('pds_editresultmodal', 'is_open')
#
#     ],
#     [
#         Input('pds_confirmsubmitgo', 'n_clicks')
#     ],
#     [
#         State('pds_confirmsubmitgo', 'n_clicks')
#     ]
# )
#
# def pdsconfirmmodal(pds_confirmsubmitgo, is_open):
#     ctx = dash.callback_context
#     if ctx.triggered:
#         eventid = ctx.triggered[0]['prop_id'].split('.')[0]
#         if eventid == 'pds_confirmsubmitgo':
#
#             return [True]
#
#         else:
#             raise PreventUpdate
#
#     else:
#         raise PreventUpdate


@app.callback(
    [
        Output('pds_confirmsubmitmodal', 'is_open'),
        Output('pds_tempunitlabel', 'style'),
        Output('pds_titlelabel', 'style'),
        Output('pds_isactivelabel', 'style'),
        Output('pds_lastname', 'valid'), Output('pds_lastname', 'invalid'),
        Output('pds_firstname', 'valid'), Output('pds_firstname', 'invalid'),

        Output('pds_doblabel', 'style'),
        Output('pds_pobislocallabel', 'style'),
        Output('pds_pobprovincelabel', 'style'),
        Output('pds_pobcitylabel', 'style'),
        Output('pds_pobcountrylabel', 'style'),
        Output('pds_pob', 'valid'), Output('pds_pob', 'invalid'),

        Output('pds_sexatbirthlabel', 'style'),
        Output('pds_civilstatuslabel', 'style'),
        Output('pds_bloodtypelabel', 'style'),
        Output('pds_email', 'valid'), Output('pds_email', 'invalid'),

        Output('pds_citizenshiplabel', 'style'),
        Output('pds_addcountrycurrlabel', 'style'),
        Output('pds_regioncurrlabel', 'style'),
        Output('pds_aprovincecurrlabel', 'style'),
        Output('pds_citymuncurrentlabel', 'style'),
        Output('pds_streetaddresscurr', 'valid'), Output('pds_streetaddresscurr', 'invalid'),
        Output('pds_brgyaddresscurr', 'valid'), Output('pds_brgyaddresscurr', 'invalid'),
        Output('pds_zipcodecurr', 'valid'), Output('pds_zipcodecurr', 'invalid'),

        Output('pds_addcountrypermlabel', 'style'),
        Output('pds_regionpermlabel', 'style'),
        Output('pds_aprovincepermlabel', 'style'),
        Output('pds_citymunpermlabel', 'style'),
        Output('pds_streetaddressperm', 'valid'), Output('pds_streetaddressperm', 'invalid'),
        Output('pds_brgyaddressperm', 'valid'), Output('pds_brgyaddressperm', 'invalid'),
        Output('pds_zipcodeperm', 'valid'), Output('pds_zipcodeperm', 'invalid'),
        Output('pds_tin', 'valid'), Output('pds_tin', 'invalid'),

        Output('pds_degreeslabel', 'style'),
        Output('pds_eligibilitieslabel', 'style'),
        Output('pds_duplimodal', 'is_open'),
        Output('pds_duplimodalwarning', 'style'),
        Output('pds_duplimodaldiv', 'children'),
        Output('pds_empnum', 'valid'), Output('pds_empnum', 'invalid'),
        Output('pds_gsis', 'valid'), Output('pds_gsis', 'invalid')

    ],
    [
        Input('pds_confirmsubmitback', 'n_clicks'),
        Input('pds_confirmsubmitgo', 'n_clicks'),
        Input('pds_submitbtn', 'n_clicks'),
        Input('pds_duplimodalclose', 'n_clicks')
    ],
    [
        State('pds_temp_unit', 'value'),
        State('pds_title', 'value'),
        State('pds_isactive', 'value'),
        State('pds_lastname', 'value'),
        State('pds_firstname', 'value'),
        State('pds_middlename', 'value'),
        State('pds_suffixname', 'value'),

        State('pds_dob', 'date'),
        State('pds_pob', 'value'),
        State('pds_sexatbirth', 'value'),
        State('pds_civilstatus', 'value'),
        State('pds_bloodtype', 'value'),
        State('pds_mobilecontactnumber', 'value'),


        State('pds_email', 'value'),
        State('pds_citizenship', 'value'),

        State('pds_addcountrycurr', 'value'),
        State('pds_regioncurr', 'value'),
        State('pds_aprovincecurr', 'value'),
        State('pds_citymuncurrent', 'value'),
        State('pds_streetaddresscurr', 'value'),

        State('pds_subdvillagecurr', 'value'),
        State('pds_brgyaddresscurr', 'value'),
        State('pds_zipcodecurr', 'value'),
        State('pds_addcountryperm', 'value'),
        State('pds_regionperm', 'value'),
        State('pds_aprovinceperm', 'value'),
        State('pds_citymunperm', 'value'),
        State('pds_streetaddressperm', 'value'),
        State('pds_subdvillageperm', 'value'),
        State('pds_brgyaddressperm', 'value'),

        State('pds_zipcodeperm', 'value'),
        State('pds_gsis', 'value'),
        State('pds_pagibig', 'value'),
        State('pds_philhealth', 'value'),
        State('pds_sss', 'value'),
        State('pds_tin', 'value'),
        State('pds_governmentid', 'value'),
        State('pds_govidnumber', 'value'),

        State('pds_permsameascurrent', 'checked'),
        State('sessiondegrees', 'data'),
        State('current_user_id', 'data'),
        State('sessioncurrentunit', 'data'),
        State("url", "search"),
        # State('bp_emp_type', 'value'),
        State("sessionpersonid", 'data'),
        State("sessionpersoneducid", 'data'),

        State('pds_doblabel', 'style'),
        State('pds_sexatbirthlabel', 'style'),
        State('pds_civilstatuslabel', 'style'),
        State('pds_citizenshiplabel', 'style'),
        State('pds_regioncurrlabel', 'style'),
        State('pds_aprovincecurrlabel', 'style'),
        State('pds_citymuncurrentlabel', 'style'),
        State('pds_regionpermlabel', 'style'),
        State('pds_aprovincepermlabel', 'style'),
        State('pds_citymunpermlabel', 'style'),

        State('sessioneligibilities', 'data'),
        State('pds_eligibilities_checkbox', 'checked'),

        State('pds_pobislocal', 'value'),
        State('pds_pobprovince', 'value'),
        State('pds_pobcity', 'value'),
        State('pds_pobcountry', 'value'),

        State('pds_pobislocallabel', 'style'),
        State('pds_pobprovincelabel', 'style'),
        State('pds_pobcitylabel', 'style'),
        State('pds_pobcountrylabel', 'style'),
        State('pds_degreeslabel', 'style'),
        State('pds_eligibilitieslabel', 'style'),
        State('sessioncurrentrole', 'data'),
        State('pds_addempnum', 'value'),
        State('pds_empnum', 'value'),

    ]
)
def modalopenpds(pds_confirmsubmitback, pds_confirmsubmitgo, pds_submitbtn, pds_duplimodalclose,
                 pds_temp_unit,
                 pds_title,
                 pds_isactive,
                 pds_lastname,
                 pds_firstname,
                 pds_middlename,
                 pds_suffixname,

                 pds_dob,
                 pds_pob,
                 pds_sexatbirth,
                 pds_civilstatus,
                 pds_bloodtype,
                 pds_mobilecontactnumber,

                 pds_email,
                 pds_citizenship,

                 pds_addcountrycurr,
                 pds_regioncurr,
                 pds_aprovincecurr,
                 pds_citymuncurrent,
                 pds_streetaddresscurr,
                 pds_subdvillagecurr,
                 pds_brgyaddresscurr,
                 pds_zipcodecurr,
                 pds_addcountryperm,
                 pds_regionperm,
                 pds_aprovinceperm,
                 pds_citymunperm,
                 pds_streetaddressperm,
                 pds_subdvillageperm,
                 pds_brgyaddressperm,
                 pds_zipcodeperm,
                 pds_gsis,
                 pds_pagibig,
                 pds_philhealth,
                 pds_sss,
                 pds_tin,
                 pds_governmentid,
                 pds_govidnumber,

                 pds_permsameascurrent,
                 sessiondegrees,
                 current_user_id,
                 sessioncurrentunit,
                 url,
                 # bp_emp_type,
                 person_id,
                 sessionpersoneducid,
                 pds_doblabel,
                 pds_sexatbirthlabel,
                 pds_civilstatuslabel,
                 pds_citizenshiplabel,
                 pds_regioncurrlabel,
                 pds_aprovincecurrlabel,
                 pds_citymuncurrentlabel,
                 pds_regionpermlabel,
                 pds_aprovincepermlabel,
                 pds_citymunpermlabel,

                 sessioneligibilities,
                 pds_eligibilities_checkbox,


                 pds_pobislocal,
                 pds_pobprovince,
                 pds_pobcity,
                 pds_pobcountry,

                 pds_pobislocallabel,
                 pds_pobprovincelabel,
                 pds_pobcitylabel,
                 pds_pobcountrylabel,
                 pds_degreeslabel,
                 pds_eligibilitieslabel,
                 sessioncurrentrole,
                pds_addempnum,
                pds_empnum

                 ):
    table = ""
    pds_duplimodalwarning = {'display':'none'}
    parsed = urlparse.urlparse(url)
    if parse_qs(parsed.query):

        mode = str(parse_qs(parsed.query)['mode'][0])

    pds_confirmsubmitmodal = False
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]

        if str(pds_isactive).upper() in ['NONE']:
            ppds_isactive_str = ""
        else:
            ppds_isactive_str = str(pds_isactive)

        pds_temp_unitvalid = checkiflengthzero2(pds_temp_unit)
        pds_titlevalid = checkiflengthzero2(pds_title)
        pds_isactivevalid = checkiflengthzero2(ppds_isactive_str)
        pds_lastnamevalid = checkiflengthzero2(pds_lastname)
        pds_firstnamevalid = checkiflengthzero2(pds_firstname)
        pds_dobvalid = checkiflengthzero2(pds_dob)

        pds_pobislocalvalid = checkiflengthzero2(pds_pobislocal)
        pds_pobprovincevalid = checkiflengthzero2(pds_pobprovince)
        pds_pobcityvalid = checkiflengthzero2(pds_pobcity)
        pds_pobcountryvalid = checkiflengthzero2(pds_pobcountry)
        pds_pobvalid = checkiflengthzero2(pds_pob)
        pds_gsisvalid = checkiflengthzero2(pds_gsis)

        if (pds_pobislocal and pds_pobprovince and pds_pobcity) or (pds_pobislocal and pds_pobcountry and pds_pob):

            pds_pobfinalvalid = True

        else:
            pds_pobfinalvalid = False

        pds_sexatbirthvalid = checkiflengthzero2(pds_sexatbirth)
        pds_civilstatusvalid = checkiflengthzero2(pds_civilstatus)
        pds_bloodtypevalid = checkiflengthzero2(pds_bloodtype)
        pds_emailvalid = checkiflengthzero2(pds_email)
        pds_citizenshipvalid = checkiflengthzero2(pds_citizenship)

        pds_addcountrycurrvalid = checkiflengthzero2(pds_addcountrycurr)
        if pds_addcountrycurr == 168:
            pds_regioncurrvalid = checkiflengthzero2(pds_regioncurr)
            pds_aprovincecurrvalid = checkiflengthzero2(pds_aprovincecurr)
            pds_citymuncurrentvalid = checkiflengthzero2(pds_citymuncurrent)
        else:
            pds_regioncurrvalid = True
            pds_aprovincecurrvalid = True
            pds_citymuncurrentvalid = True
        pds_streetaddresscurrvalid = checkiflengthzero2(pds_streetaddresscurr)
        pds_brgyaddresscurrvalid = checkiflengthzero2(pds_brgyaddresscurr)
        pds_zipcodecurrvalid = checkiflengthzero2(pds_zipcodecurr)

        if pds_permsameascurrent:
            pds_addcountrypermvalid = pds_addcountrycurrvalid
            pds_regionpermvalid = pds_regioncurrvalid
            pds_aprovincepermvalid = pds_aprovincecurrvalid
            pds_citymunpermvalid = pds_citymuncurrentvalid
            pds_streetaddresspermvalid = pds_streetaddresscurrvalid
            pds_brgyaddresspermvalid = pds_brgyaddresscurrvalid
            pds_zipcodepermvalid = pds_zipcodecurrvalid

        else:
            pds_addcountrypermvalid = checkiflengthzero2(pds_addcountryperm)
            if pds_addcountryperm == 168:
                pds_regionpermvalid = checkiflengthzero2(pds_regionperm)
                pds_aprovincepermvalid = checkiflengthzero2(pds_aprovinceperm)
                pds_citymunpermvalid = checkiflengthzero2(pds_citymunperm)
            else:
                pds_regionpermvalid = True
                pds_aprovincepermvalid = True
                pds_citymunpermvalid = True
            pds_streetaddresspermvalid = checkiflengthzero2(pds_streetaddressperm)
            pds_brgyaddresspermvalid = checkiflengthzero2(pds_brgyaddressperm)
            pds_zipcodepermvalid = checkiflengthzero2(pds_zipcodeperm)


        print('HERE4577', pds_tin, checkiflengthx2(pds_tin, 12), checkiflengthzero2(pds_tin))



        pds_tin_str = str(pds_tin)
        if checkiflengthx2(pds_tin, 12) or checkiflengthzero2(pds_tin) or pds_tin_str.upper() in ['NONE', 'NAN']:
            pds_tinvalid = True
        else:
            pds_tinvalid = False

        pds_empnumvalid = True
        if int(sessioncurrentrole) in [1, 27] and 1 in pds_addempnum:#hrdo analyist, superadmin
            pds_empnumvalid = checkiflengthx2(pds_empnum, 9)
        else:
            pds_empnumvalid = True




        if len(sessiondegrees) == 0:
            sessiondegreesvalid = False
        else:
            sessiondegreesvalid = True

        if len(sessioneligibilities) == 0 and not pds_eligibilities_checkbox:
            sessioneligibilitiesvalid = False
        else:
            sessioneligibilitiesvalid = True

        if mode == 'edit':
            pds_temp_unitvalid = True
            uid = str(parse_qs(parsed.query)['uid'][0])

            sql1 = '''
                SELECT person_old_emp03s_id
                FROM persons
                WHERE person_id = %s

            '''

            values1 = (uid,)
            columns1 = ['person_old_emp03s_id']
            df1 = securequerydatafromdatabase(sql1, values1, columns1)
            person_old_emp03s_id = df1["person_old_emp03s_id"][0]

            if not person_old_emp03s_id is None:

                pds_temp_unitvalid = True
                pds_titlevalid = True
                pds_isactivevalid = True
                pds_lastnamevalid = True
                pds_firstnamevalid = True
                pds_dobvalid = True
                pds_pobfinalvalid = True
                pds_sexatbirthvalid = True
                pds_civilstatusvalid = True
                pds_bloodtypevalid = True
                pds_emailvalid = True
                pds_citizenshipvalid = True
                pds_addcountrycurrvalid = True
                pds_regioncurrvalid = True
                pds_aprovincecurrvalid = True
                pds_citymuncurrentvalid = True
                pds_streetaddresscurrvalid = True
                pds_brgyaddresscurrvalid = True
                pds_zipcodecurrvalid = True
                pds_addcountrypermvalid = True
                pds_regionpermvalid = True
                pds_aprovincepermvalid = True
                pds_citymunpermvalid = True
                pds_streetaddresspermvalid = True
                pds_brgyaddresspermvalid = True
                pds_zipcodepermvalid = True
                pds_tinvalid = True
                sessiondegreesvalid = True
                sessioneligibilitiesvalid = True
                pds_gsisvalid = True

        pds_tempunitlabel = checkstyle2(pds_temp_unitvalid)
        pds_titlelabel = checkstyle2(pds_titlevalid)
        pds_isactivelabel = checkstyle2(pds_isactivevalid)
        pds_doblabel = checkstyle2(pds_dobvalid)
        pds_pobislocallabel = checkstyle2(pds_pobislocalvalid)
        pds_pobprovincelabel = checkstyle2(pds_pobprovincevalid)
        pds_pobcitylabel = checkstyle2(pds_pobprovincevalid)
        pds_pobcountrylabel = checkstyle2(pds_pobcountryvalid)

        pds_sexatbirthlabel = checkstyle2(pds_sexatbirthvalid)
        pds_civilstatuslabel = checkstyle2(pds_civilstatusvalid)
        pds_bloodtypelabel = checkstyle2(pds_bloodtypevalid)
        pds_citizenshiplabel = checkstyle2(pds_citizenshipvalid)

        pds_addcountrycurrlabel = checkstyle2(pds_addcountrycurrvalid)
        pds_regioncurrlabel = checkstyle2(pds_regioncurrvalid)
        pds_aprovincecurrlabel = checkstyle2(pds_aprovincecurrvalid)
        pds_citymuncurrentlabel = checkstyle2(pds_citymuncurrentvalid)

        pds_addcountrypermlabel = checkstyle2(pds_addcountrypermvalid)
        pds_regionpermlabel = checkstyle2(pds_regionpermvalid)
        pds_aprovincepermlabel = checkstyle2(pds_aprovincepermvalid)
        pds_citymunpermlabel = checkstyle2(pds_citymunpermvalid)

        pds_degreeslabel = checkstyle2(sessiondegreesvalid)

        pds_eligibilitieslabel = checkstyle2(sessioneligibilitiesvalid)

        allvalid = [pds_temp_unitvalid, pds_titlevalid, pds_isactivevalid, pds_lastnamevalid, pds_firstnamevalid, pds_dobvalid,
                    pds_pobfinalvalid,
                    pds_sexatbirthvalid, pds_civilstatusvalid, pds_bloodtypevalid, pds_emailvalid, pds_citizenshipvalid,
                    pds_addcountrycurrvalid, pds_regioncurrvalid, pds_aprovincecurrvalid, pds_citymuncurrentvalid, pds_streetaddresscurrvalid, pds_brgyaddresscurrvalid, pds_zipcodecurrvalid,
                    pds_addcountrypermvalid, pds_regionpermvalid, pds_aprovincepermvalid, pds_citymunpermvalid, pds_streetaddresspermvalid, pds_brgyaddresspermvalid, pds_zipcodepermvalid,
                    pds_tinvalid, pds_empnumvalid,sessiondegreesvalid, sessioneligibilitiesvalid, pds_gsisvalid]

        # pds_lastname
        # pds_firstname
        # pds_dob
        # pds_middlename
        # pds_suffixname


        if all(allvalid):

            pds_confirmsubmitmodal = True

        else:
            pds_confirmsubmitmodal = False
        has_dupli = False
        pds_duplimodal = False

        if mode == 'add':
            # duplisql = '''
            #             SELECT person_last_name, person_first_name, person_middle_name, person_name_extension, person_dob, person_id
            #             FROM persons
            #             WHERE person_last_name = UPPER(%s)
            #             AND person_delete_ind = %s
            #         '''
            #
            # duplivalues = (pds_lastname, False)
            # duplicolumns = ['person_last_name', 'person_first_name', 'person_middle_name', 'person_name_extension',
            #                 'person_dob', 'person_id']
            #
            # duplidf = securequerydatafromdatabase(duplisql, duplivalues, duplicolumns)
            #
            # if duplidf.shape[0] > 0:
            #     duplidf['person_dob'] = duplidf['person_dob'].astype(str)
            #     # lastname_list = duplidf['person_last_name'].tolist()
            #     firstname_list = duplidf['person_first_name'].tolist()
            #     middlename_list = duplidf['person_middle_name'].tolist()
            #     suffix_list = duplidf['person_name_extension'].tolist()
            #     dob_list = duplidf['person_dob'].tolist()
            #     personid_list = duplidf['person_id'].tolist()
            #
            #     for i in range(len(firstname_list)):
            #         if (str(firstname_list[i]).upper() == str(pds_firstname).upper() and
            #                 str(middlename_list[i]).upper() == str(pds_middlename).upper() and
            #                 str(suffix_list[i]).upper() == str(pds_suffixname).upper() and
            #                 dob_list[i] == pds_dob):
            #
            #             dupli_personid = personid_list[i]
            #
            #             has_dupli = True
            #             break
            has_dupli = False 
            has_dupli, dupli_personid = ispersonexisting(pds_firstname, pds_middlename, pds_lastname, pds_suffixname, pds_dob)

            pds_duplimodal = has_dupli

            if has_dupli == True:

                duplisql2 = '''
                            SELECT p.person_id, u.unit_name, e.emp_is_active,
                            CASE WHEN e.emp_is_active = True THEN 'Active'
                            WHEN e.emp_is_active = False THEN 'Inactive'
                            ELSE 'No Info'
                            END AS emp_is_active_text
                            FROM persons p
                            LEFT JOIN employees e ON p.person_id = e.person_id
                            LEFT JOIN units u ON u.unit_id = e.emp_primary_home_unit_id
                            WHERE p.person_id = %s
                            AND p.person_delete_ind = %s

                        '''

                duplivalues2 = (dupli_personid, False)
                duplicolumns2 = ['Person ID', 'Unit', 'emp_is_active', 'Is Active?']

                duplidf2 = securequerydatafromdatabase(duplisql2, duplivalues2, duplicolumns2)
                duplidf2 = duplidf2[['Person ID', 'Unit','Is Active?']]

                table = dbc.Table.from_dataframe(duplidf2, striped=True, bordered=True, hover=True)

                pds_confirmsubmitmodal = False

            if has_dupli == True and sessioncurrentrole in [1]:
                pds_duplimodal = False
                pds_duplimodalwarning = {'display':'inline'}
                pds_confirmsubmitmodal = True

        if eventid in ['pds_duplimodalclose']:
            pds_duplimodal = False
        if eventid in ['pds_submitbtn', 'pds_confirmsubmitback', 'pds_confirmsubmitgo', 'pds_duplimodalclose']:
            if eventid in ['pds_confirmsubmitback', 'pds_confirmsubmitgo']:
                pds_confirmsubmitmodal = False
                pds_duplimodal = False

            return [
                pds_confirmsubmitmodal,
                pds_tempunitlabel,
                pds_titlelabel,
                pds_isactivelabel,
                pds_lastname, not pds_lastname,
                pds_firstname, not pds_firstname,

                pds_doblabel,
                pds_pobislocallabel,
                pds_pobprovincelabel,
                pds_pobcitylabel,
                pds_pobcountrylabel,
                pds_pob, not pds_pob,

                pds_sexatbirthlabel,
                pds_civilstatuslabel,
                pds_bloodtypelabel,
                pds_emailvalid, not pds_emailvalid,


                pds_citizenshiplabel,
                pds_addcountrycurrlabel,
                pds_regioncurrlabel,
                pds_aprovincecurrlabel,
                pds_citymuncurrentlabel,
                pds_streetaddresscurrvalid, not pds_streetaddresscurrvalid,
                pds_brgyaddresscurr, not pds_brgyaddresscurrvalid,
                pds_zipcodecurr, not pds_zipcodecurr,

                pds_addcountrypermlabel,
                pds_regionpermlabel,
                pds_aprovincepermlabel,
                pds_citymunpermlabel,
                pds_streetaddresspermvalid, not pds_streetaddresspermvalid,
                pds_brgyaddresspermvalid, not pds_brgyaddresspermvalid,
                pds_zipcodepermvalid, not pds_zipcodepermvalid,
                pds_tinvalid, not pds_tinvalid,

                pds_degreeslabel,
                pds_eligibilitieslabel,
                pds_duplimodal,
                pds_duplimodalwarning,
                table,
                pds_empnumvalid, not pds_empnumvalid,
                pds_gsisvalid, not pds_gsisvalid

            ]

        # elif eventid == 'pds_confirmsubmitback':
        #
        #     return [
        #         False,
        #         pds_tempunitlabel,

        #         pds_titlelabel,
        #

        # elif eventid == 'pds_submitbtn':
        #     return [True]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback(
    [
        Output("pds_eligibility", "value"),
        Output("pds_eligibilityrating", "value"),
        Output("pds_eligibility_date_of_exam", "date"),
        Output("pds_placeofconferment", "value"),
        Output("pds_licensenumber", "value"),
        Output("pds_eligibilitystartdate", "date"),
        Output("pds_eligibilityenddate", "date"),
    ],
    [
        # Input("pds_elig_id_store", "value")
        Input("pds_elig_summary", "value"),
        # Input({'type': 'pds_dynamiceligedit', 'index': ALL}, 'n_clicks')
    ],
    [
        State('sessioneligibilities', 'data'),
        State('sessioneligibilitiesprocessed', 'data'),
        # State("pds_elig_summary", "value"),

    ]
)

def toggle_modal_elig_values(
                                pds_elig_summary,
                                # pds_elig_id_store,
                                # pds_dynamiceligedit,
                                sessioneligibilities, sessioneligibilitiesprocessed,
                                # pds_elig_summary
                                ):

    pds_elig_summary = int(pds_elig_summary)
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if pds_elig_summary == -1 or len(sessioneligibilities)==0:
            pds_eligibility = ""
            pds_eligibilityrating = ""
            pds_eligibility_date_of_exam = date.today()
            pds_placeofconferment = ""
            pds_licensenumber = ""
            pds_eligibilitystartdate = date.today()
            pds_eligibilityenddate = date.today()

        elif pds_elig_summary >= 0:

            # index = json.loads(eventid)["index"]
            index = pds_elig_summary

            pds_eligibility = sessioneligibilities[index]['Eligibility']
            pds_eligibilityrating = sessioneligibilities[index]['Rating']
            pds_eligibility_date_of_exam = sessioneligibilities[index]['Date of Exam']
            pds_placeofconferment = sessioneligibilities[index]['Place of Conferment']
            pds_licensenumber = sessioneligibilities[index]['License Number']
            pds_eligibilitystartdate = sessioneligibilities[index]['Eligibility Effective Start Date']
            pds_eligibilityenddate = sessioneligibilities[index]['Eligibility Effective End Date']

    return [pds_eligibility, pds_eligibilityrating, pds_eligibility_date_of_exam, pds_placeofconferment,
            pds_licensenumber, pds_eligibilitystartdate, pds_eligibilityenddate]

@app.callback(
    [
        Output('pds_deletemodal', 'is_open')
    ],
    [
        Input('pds_deletebutton', 'n_clicks'),
        Input('pds_deletemodalcancel', 'n_clicks'),
        Input('pds_deletemodalconfirm', 'n_clicks')

    ]

)
def deletemodal1(pds_deletebutton, pds_deletemodalcancel, pds_deletemodalconfirm):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'pds_deletebutton':

            return [True]
        elif eventid == 'pds_deletemodalcancel' or eventid == 'pds_deletemodalconfirm':

            return [False]

        else:
            raise PreventUpdate

    else:
        raise PreventUpdate


@app.callback(
    [
        Output('pds_deletemodal2', 'is_open')
    ],
    [
        Input('pds_deletemodalconfirm', 'n_clicks')
    ],
    [
        State('url', 'search')

    ]
)
def deletemodal2(pds_deletemodalconfirm, url):

    parsed = urlparse.urlparse(url)
    if parse_qs(parsed.query):
        ctx = dash.callback_context
        if ctx.triggered:
            eventid = ctx.triggered[0]['prop_id'].split('.')[0]
            person_id = str(parse_qs(parsed.query)['uid'][0])
            if eventid == 'pds_deletemodalconfirm':
                sql6 = """
                        UPDATE persons
                        SET person_delete_ind = %s
                        WHERE person_id = %s
                    """

                values6 = [True, person_id]

                modifydatabase(sql6, values6)

                return [True]
            else:
                raise PreventUpdate
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback(
    [
        Output('div_region', 'style'),
        Output('div_prov', 'style'),
        Output('div_city', 'style'),
        Output('pds_pobproxy1curr', 'style'),




    ],
    [
        Input('pds_addcountrycurr', 'value')
    ]
)
def temp_address_style_country(pds_addcountrycurr):
    if pds_addcountrycurr == 168:
        return [{'display': 'inline'}, {'display': 'inline'}, {'display': 'inline'}, {'display': 'none'}]
    else:
        return [{'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'inline'}]


@app.callback(
    [
        Output('div_regionperm', 'style'),
        Output('div_provperm', 'style'),
        Output('div_cityperm', 'style'),
        Output('pds_pobproxy1perm', 'style'),




    ],
    [
        Input('pds_addcountryperm', 'value')
    ]
)
def perm_address_style_country(pds_addcountryperm):
    if pds_addcountryperm == 168:
        return [{'display': 'inline'}, {'display': 'inline'}, {'display': 'inline'}, {'display': 'none'}]
    else:
        return [{'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'inline'}]


def update_persons_history(person_id,
                           current_user_id,
                           title_id,
                           last_name,
                           first_name,
                           middle_name,
                           name_extension,
                           civil_status_id,
                           pob_country_id,
                           pob_city_id,
                           pob_prov_id,
                           temp_unit_id,
                           savemode):
    if savemode == "add":
        mode_id = 1
    elif savemode == "edit":
        mode_id = 2
    else:
        mode_id = 3
    sqlpersonschange = """
        INSERT INTO person_change_history(person_id, person_change_history_modified_by, person_change_history_modified_on, person_change_history_delete_ind,
            person_change_history_title_id, person_change_history_last_name, person_change_history_first_name, person_change_history_middle_name, person_change_history_person_name_extension,
            person_change_history_civil_status_id, person_change_history_pob_country_id, person_change_history_pob_city_id, person_change_history_pob_prov_id,person_change_history_temp_unit_id,
            person_change_mode_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)

    """

    values = [person_id, current_user_id, datetime.now(), False,
              title_id, last_name, first_name, middle_name, name_extension,
              civil_status_id, pob_country_id, pob_city_id, pob_prov_id, temp_unit_id,
              mode_id]

    modifydatabase(sqlpersonschange, values)
    pass

@app.callback(
    [
        Output('pds_empnum_input_collapse', 'is_open')

    ],
    [
        Input('pds_addempnum', 'value')

    ]
)

def pds_open_empnum_collapse(pds_addempnum):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'pds_addempnum':

            if 1 in pds_addempnum:
                return_value = True
            else:
                return_value = False

            return [return_value]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback([
    Output('pds_confirmsubmitgo', 'disabled'),

],
    [
    Input('pds_confirmsubmitgo', 'n_clicks'),

],
    [

], prevent_initial_call=True)
def disable_submits(pds_confirmsubmitgo):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid in ['pds_confirmsubmitgo']:
            return [True]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
