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
from apps.dbconnect import securequerydatafromdatabase, modifydatabase, modifydatabasereturnid, bulkmodifydatabase
import hashlib
from datetime import datetime
import dash_table
import pandas as pd
import numpy as np
from datetime import date as date
import urllib.parse as urlparse
from urllib.parse import parse_qs
from apps.commonmodules import safeupper


#### MAIN ####


layout = html.Div([
    commonmodules.get_header(),
    commonmodules.get_menu(),
    commonmodules.get_common_variables(),
    dcc.Store(id='pdsv_sessiondegrees', storage_type='memory', data=[]),
    dcc.Store(id='pdsv_sessiondegreesprocessed', storage_type='memory', data=[]),
    dcc.Store(id='pdsv_sessioneligibilities', storage_type='memory', data=[]),
    dcc.Store(id='pdsv_sessioneligibilitiesprocessed', storage_type='memory', data=[]),
    dcc.Store(id='pdsv_sessionpersonid', storage_type='memory', data=[]),
    dcc.Store(id='pdsv_sessionpersoneducid', storage_type='memory', data=[]),
    dcc.Store(id='pdsv_sessionpersoneligibilitiescid', storage_type='memory', data=[]),
    html.Div([
        html.H1("View Personal Data Entry", style={
                "display": "block"}, id="pdsv_createheader"),
        html.H1("View Personal Data Entries", style={"display": "none"}, id="pdsv_editheader"),
        dcc.Link('← Back to List of Personal Data Entries',
                 href='/settings/settings_personal_data_viewing'),

        html.Hr(),

        dbc.Form([

            dbc.Card([

                dbc.CardHeader(
                    html.H4("Personal Data"),
                    style={"background-color": "rgb(123,20,24)", 'color': 'white'}
                ),

                html.Br(),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Div([

                                dbc.FormGroup([
                                    dbc.Label(
                                        "Select Temporary Unit", width=4, style={"text-align": "left", 'color': 'black'}),
                                    dbc.Col([
                                        dcc.Dropdown(
                                            id='pdsv_temp_unit',

                                            placeholder="Please select temporary unit",
                                        ),
                                        dbc.FormFeedback(
                                            "Please select temporary unit", valid=False)
                                    ], width=8)
                                ], row=True, ),

                            ], id = 'pdsv_tempunitdiv', style = {'display':'none'})
                        ]),
                        dbc.Col([

                        ]),
                    ]),

                    dbc.Row([
                        dbc.Col([
                            html.H4("Personal Information")
                        ]),
                        dbc.Col([

                        ]),

                    ]),

                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                dbc.FormGroup([
                                    dbc.Label(
                                        "Title", width=4,
                                        style={"text-align": "left", 'color': 'black'}
                                    ),
                                    dbc.Col([
                                        dbc.Label(
                                            children = '<value>', id='pdsv_title',
                                        ),

                                    #     dbc.FormFeedback(
                                    #          "Please select temporary unit", valid=False
                                    #         )
                                    ], width=8),
                                ], row=True,),

                            ], id='titlediv')
                            ]),

                        dbc.Col([

                        ]),
                        dbc.Col([

                        ]),
                    ]),


                    dbc.Row([
                        dbc.Col([
                            dbc.FormGroup([
                                dbc.Label("Last Name", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([

                                    dbc.Label(
                                        children='<value>', id='pdsv_lastname',
                                    ),

                                ], width=8)
                            ], row=True),
                        ]),
                        dbc.Col([
                            dbc.FormGroup([
                                dbc.Label("First Name", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([

                                    dbc.Label(
                                        children='<value>', id='pdsv_firstname',
                                    ),

                                ], width=8)
                            ], row=True),
                        ]),
                        dbc.Col([
                            dbc.FormGroup([
                                dbc.Label("Middle Name", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Label(
                                        children='<value>', id='pdsv_middlename',
                                    ),
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
                                    dbc.Label(
                                        children='<value>', id='pdsv_suffixname',
                                    ),
                                ], width=8)
                            ], row=True),
                        ]),
                        dbc.Col([
                            dbc.FormGroup([
                                dbc.Label(
                                    "Date of Birth", width=4, style={"text-align": "left", 'color': 'black'}, id='pdsv_doblabel'),
                                dbc.Col([
                                    dbc.Label(
                                        children='<value>', id='pdsv_dob',
                                    ),
                                ], width=8)
                            ], row=True),
                        ]),
                        dbc.Col([
                            # dbc.FormGroup([
                            #     dbc.Label("Place of Birth", width=4,
                            #               style={"text-align": "left"}),
                            #     dbc.Col([
                            #         dbc.Label(
                            #             children='<value>', id='pdsv_pob',
                            #         ),
                            #     ], width=8)
                            # ], row=True),
                        ]),


                    ]),

                    dbc.Row([
                        dbc.Col([
                            dbc.FormGroup([
                                dbc.Label("Place of Birth Local?", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Label(
                                        children='<value>', id='pdsv_pobislocal',
                                    ),
                                ], width=8)
                            ], row=True),
                        ]),
                        dbc.Col([
                            dbc.FormGroup([
                                dbc.Label(
                                    "Local POB - Province", width=4, style={"text-align": "left", 'color': 'black'}, id='pdsv_pobprovince'),
                                dbc.Col([
                                    dbc.Label(
                                        children='<value>', id='pdsv_pobprovince',
                                    ),
                                ], width=8)
                            ], row=True),
                        ], id = 'pdsv_proxydiv1'),
                        dbc.Col([
                            dbc.FormGroup([
                                dbc.Label("Local POB - City", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Label(
                                        children='<value>', id='pdsv_pobcity',
                                    ),
                                ], width=8)
                            ], row=True),
                        ], id = 'pdsv_proxydiv2'),

                        dbc.Col([
                            dbc.FormGroup([
                                dbc.Label("Country of Birth", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Label(
                                        children='<value>', id='pdsv_pobcountry',
                                    ),
                                ], width=8)
                            ], row=True),
                        ], id = 'pdsv_proxydiv3'),
                        dbc.Col([
                            dbc.FormGroup([
                                dbc.Label(
                                    "Outside PH POB - City", width=4, style={"text-align": "left", 'color': 'black'},
                                    id='pdsv_doblabel'),
                                dbc.Col([
                                    dbc.Label(
                                        children='<value>', id='pdsv_pob',
                                    ),
                                ], width=8)
                            ], row=True),
                        ], id = 'pdsv_proxydiv4'),

                    ]),



                    dbc.Row([
                        dbc.Col([
                            dbc.FormGroup([
                                dbc.Label(
                                    "Sex at Birth", width=4, style={"text-align": "left", 'color': 'black'}, id='pdsv_sexatbirthlabel'),
                                dbc.Col([
                                    dbc.Label(
                                        children='<value>', id='pdsv_sexatbirth',
                                    ),
                                ], width=8)
                            ], row=True),
                        ]),
                        dbc.Col([
                            dbc.FormGroup([
                                dbc.Label(
                                    "Civil Status", width=4, style={"text-align": "left", 'color': 'black'}, id='pdsv_civilstatuslabel'),
                                dbc.Label(
                                    children='<value>', id='pdsv_civilstatus',
                                ),
                            ], row=True),
                        ]),
                        dbc.Col([
                            dbc.FormGroup([
                                dbc.Label("Blood Type", width=4,
                                          style={"text-align": "left"}),
                                dbc.Label(
                                    children='<value>', id='pdsv_bloodtype',
                                ),
                            ], row=True),
                        ]),
                    ]),
                    dbc.Row([

                        dbc.Col([
                            dbc.FormGroup([
                                dbc.Label("Mobile Number", width=4,
                                          style={"text-align": "left"}),
                                dbc.Label(
                                    children='<value>', id='pdsv_mobilecontactnumber',
                                ),
                            ], row=True),
                        ]),
                        dbc.Col([
                            dbc.FormGroup([
                                dbc.Label("Landline Number", width=4,
                                          style={"text-align": "left"}),
                                dbc.Label(
                                    children='<value>', id='pdsv_lanecontactnumber',
                                ),
                            ], row=True),
                        ]),
                        dbc.Col([
                            dbc.FormGroup([
                                dbc.Label("Email Address", width=4,
                                          style={"text-align": "left"}),
                                dbc.Label(
                                    children='<value>', id='pdsv_email',
                                ),
                            ], row=True),
                        ]),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.FormGroup([
                                dbc.Label(
                                    "Citizenship", width=4, style={"text-align": "left", 'color': 'black'}, id='pdsv_citizenshiplabel'),
                                dbc.Col([
                                    dbc.Label(
                                        children='<value>', id='pdsv_citizenship',
                                    ),
                                ], width=8)
                            ], row=True),
                        ]),
                        dbc.Col([
                            dbc.FormGroup([
                                dbc.Label("Type of Citizenship", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([
                                    dbc.Label(
                                        children='<value>', id='pdsv_typeofcit',
                                    ),
                                ], width=8)
                            ], row=True),
                        ]),
                        dbc.Col([

                                dbc.FormGroup([
                                    dbc.Label("Country of Foreign Citizenship",
                                              width=4, style={"text-align": "left"}),
                                    dbc.Col([
                                        dbc.Label(
                                            children='<value>', id='pdsv_countryofcit',
                                        ),
                                    ], width=8)
                                ], row=True),
                        ]),
                    ]),

                    html.Hr(),
                    dbc.Spinner([
                                dbc.Row([
                                    dbc.Col([
                                        html.H4("Current Address")
                                    ]),
                                    dbc.Col([

                                    ]),

                                ]),
                                html.Br(),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.FormGroup([

                                            dbc.Label("Country", width=4,
                                                      style={"text-align": "left"}),
                                            dbc.Col([

                                                dbc.Label(
                                                    children='<value>', id='pdsv_addcurrentcountry',
                                                ),

                                            ], width=8)

                                        ], row=True),
                                    ]),
                                    dbc.Col([
                                        dbc.FormGroup([
                                            dbc.Label(
                                                "Region", width=4, style={"text-align": "left", 'color': 'black'}, id='pdsv_regioncurrlabel'),
                                            dbc.Col([

                                                dbc.Label(
                                                    children='<value>', id='pdsv_regioncurr',
                                                ),

                                            ], width=8)
                                        ], row=True),
                                    ]),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.FormGroup([
                                            dbc.Label(
                                                "Province", width=4, style={"text-align": "left", 'color': 'black'}, id='pdsv_aprovincecurrlabel'),

                                            dbc.Col([
                                                dbc.Label(
                                                    children='<value>', id='pdsv_aprovincecurr',
                                                ),
                                            ], width=8)
                                        ], row=True),
                                    ]),
                                    dbc.Col([
                                        dbc.FormGroup([
                                            dbc.Label(
                                                "City/Municipality", width=4, style={"text-align": "left", 'color': 'black'}, id='pdsv_citymuncurrentlabel'),
                                            dbc.Col([

                                                dbc.Label(
                                                    children='<value>', id='pdsv_citymuncurrent',
                                                ),
                                            ], width=8)
                                        ], row=True),
                                    ]),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.FormGroup([
                                            dbc.Label("House Number, Street Address",
                                                      width=4, style={"text-align": "left"}),
                                            dbc.Col([

                                                dbc.Label(
                                                    children='<value>', id='pdsv_streetaddresscurr',
                                                ),
                                            ], width=8)
                                        ], row=True),
                                    ]),
                                    dbc.Col([
                                        dbc.FormGroup([
                                            dbc.Label("Subdivision/Village", width=4,
                                                      style={"text-align": "left"}),
                                            dbc.Col([


                                                dbc.Label(
                                                    children='<value>', id='pdsv_subdvillagecurr',
                                                ),
                                            ], width=8)
                                        ], row=True),
                                    ]),

                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.FormGroup([
                                            dbc.Label("Barangay", width=4,
                                                      style={"text-align": "left"}),
                                            dbc.Col([
                                                dbc.Label(
                                                    children='<value>', id='pdsv_brgyaddresscurr',
                                                ),
                                            ], width=8)
                                        ], row=True),
                                    ]),
                                    dbc.Col([
                                        dbc.FormGroup([
                                            dbc.Label("Zip Code", width=4,
                                                      style={"text-align": "left"}),
                                            dbc.Col([

                                                dbc.Label(
                                                    children='<value>', id='pdsv_zipcodecurr',
                                                ),

                                            ], width=8)
                                        ], row=True),
                                    ]),
                                ]),
                                html.Hr(),

                                dbc.Row([
                                    dbc.Col([
                                        html.H4("Permanent Address"),
                                    ]),
                                    dbc.Col([

                                    ]),
                                ]),
                                html.Br(),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.FormGroup([
                                            dbc.Label("Country", width=4,
                                                      style={"text-align": "left"}),
                                            dbc.Col([


                                                dbc.Label(
                                                    children='<value>', id='pdsv_addcountryperm',
                                                ),
                                            ], width=8)
                                        ], row=True),
                                    ]),
                                    dbc.Col([
                                        dbc.FormGroup([
                                            dbc.Label(
                                                "Region", width=4, style={"text-align": "left", 'color': 'black'}, id='pdsv_regionpermlabel'),
                                            dbc.Col([

                                                dbc.Label(
                                                    children='<value>', id='pdsv_regionperm',
                                                ),
                                            ], width=8)
                                        ], row=True),
                                    ]),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.FormGroup([
                                            dbc.Label(
                                                "Province", width=4, style={"text-align": "left", 'color': 'black'}, id='pdsv_aprovincepermlabel'),
                                            dbc.Col([



                                                dbc.Label(
                                                    children='<value>', id='pdsv_aprovinceperm',
                                                ),
                                            ], width=8)
                                        ], row=True),
                                    ]),
                                    dbc.Col([
                                        dbc.FormGroup([
                                            dbc.Label(
                                                "City/Municipality", width=4, style={"text-align": "left", 'color': 'black'}, id='pdsv_citymunpermlabel'),
                                            dbc.Col([
                                                dbc.Label(
                                                    children='<value>', id='pdsv_citymunperm',
                                                ),


                                            ], width=8)
                                        ], row=True),
                                    ]),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.FormGroup([
                                            dbc.Label("House Number, Street Address",
                                                      width=4, style={"text-align": "left"}),
                                            dbc.Col([


                                                dbc.Label(
                                                    children='<value>', id='pdsv_streetaddressperm',
                                                ),
                                            ], width=8)
                                        ], row=True),
                                    ]),
                                    dbc.Col([
                                        dbc.FormGroup([
                                            dbc.Label("Subdivision/Village", width=4,
                                                      style={"text-align": "left"}),
                                            dbc.Col([

                                                dbc.Label(
                                                    children='<value>', id='pdsv_subdvillageperm',
                                                ),
                                            ], width=8)
                                        ], row=True),
                                    ]),

                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.FormGroup([
                                            dbc.Label("Barangay", width=4,
                                                      style={"text-align": "left"}),
                                            dbc.Col([

                                                dbc.Label(
                                                    children='<value>', id='pdsv_brgyaddressperm',
                                                ),
                                            ], width=8)

                                        ], row=True),
                                    ]),
                                    dbc.Col([
                                        dbc.FormGroup([
                                            dbc.Label("Zip Code", width=4,
                                                      style={"text-align": "left"}),
                                            dbc.Col([

                                                dbc.Label(
                                                    children='<value>', id='pdsv_zipcodeperm',
                                                ),

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
                                dbc.Label("GSIS BP No.", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([


                                    dbc.Label(
                                        children='<value>', id='pdsv_gsis',
                                    ),
                                ], width=8)
                            ], row=True),
                        ]),
                        dbc.Col([
                            dbc.FormGroup([
                                dbc.Label("PAG-IBIG ID No.", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([


                                    dbc.Label(
                                        children='<value>', id='pdsv_pagibig',
                                    ),
                                ], width=8)
                            ], row=True),
                        ]),
                        dbc.Col([
                            dbc.FormGroup([
                                dbc.Label("Philhealth No.", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([



                                    dbc.Label(
                                        children='<value>', id='pdsv_philhealth',
                                    ),
                                ], width=8)
                            ], row=True),
                        ]),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.FormGroup([
                                dbc.Label("SSS No.", width=4, style={"text-align": "left"}),
                                dbc.Col([


                                    dbc.Label(
                                        children='<value>', id='pdsv_sss',
                                    ),
                                ], width=8)
                            ], row=True),
                        ]),
                        dbc.Col([
                            dbc.FormGroup([
                                dbc.Label("TIN", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([

                                    dbc.Label(
                                        children='<value>', id='pdsv_tin',
                                    ),

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

                                    dbc.Label(
                                        children='<value>', id='pdsv_governmentid',
                                    ),
                                ], width=8)
                            ], row=True),
                        ]),
                        dbc.Col([
                            dbc.FormGroup([
                                dbc.Label("Government ID #", width=4,
                                          style={"text-align": "left"}),
                                dbc.Col([

                                    dbc.Label(
                                        children='<value>', id='pdsv_govidnumber',
                                    ),
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
                                html.H4("Degrees Earned", id='pdsv_degreeslabel')
                            ]),
                            dbc.Col([

                            ]),

                        ]),
                        html.Br(),
                    ]),

                    html.Div([

                    ], id="pdsv_currentdegreediv"),


                    html.Hr(),
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.H4("Eligibilities", id='pdsv_eligibilitieslabel')
                            ]),
                            dbc.Col([

                            ]),
                        ]),


                    ]),

                    html.Div([

                    ], id="pdsv_currenteligibilitiesdiv"),
                    html.Hr(),

                    html.Br(),

                ])
            ], className='border-dark'),

            ###

            html.Br(),
            html.Br(),

            dbc.Button("Show Old Values", color = "info", className = "mr-1", id = "pdsv_oldvaluesbtn"),

            html.Br(),
            html.Br(),

            dbc.Collapse([
                dbc.Card([

                    dbc.CardHeader(
                        html.H4("Old SQL Values"),
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
                                            children="<null>", id="pdsv_oldtitle",
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
                                            children="<null>", id="pdsv_oldsex",
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
                                            children="<null>", id="pdsv_olddob",
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
                                            children="<null>", id="pdsv_oldcstat",
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
                                            children="<null>", id="pdsv_oldcitizenship",
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
                                            children="<null>", id="pdsv_oldbltype",
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
                                            children="<null>", id="pdsv_oldtin",
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
                                            children="<null>", id="pdsv_oldotherq",
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
                                            children="<null>", id="pdsv_oldencode",
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
                                            children="<null>", id="pdsv_oldhrmo",
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
                                            children="<null>", id="pdsv_oldrem",
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
                                            children="<null>", id="pdsv_oldcreatedat",
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
                                            children="<null>", id="pdsv_oldupdatedat",
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
                                            children="<null>", id="pdsv_oldapptclean",
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
                                            children="<null>", id="pdsv_oldapptremarks",
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
                                            children="<null>", id="pdsv_oldapptname",
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
                                            children="<null>", id="pdsv_oldtimestamp",
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
                                            children="<null>", id="pdsv_oldleaveclean",
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
                                            children="<null>", id="pdsv_oldleaveremarks",
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
                                            children="<null>", id="pdsv_oldleavename",
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
                                            children="<null>", id="pdsv_oldleavetimestamp",
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
                                            children="<null>", id="pdsv_oldsysclean",
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
                                            children="<null>", id="pdsv_oldsysremarks",
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
                                            children="<null>", id="pdsv_oldsystimestamp",
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
                                            children="<null>", id="pdsv_oldleaveremarks2",
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
                                            children="<null>", id="pdsv_oldleaveremarks3",
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
                                            children="<null>", id="pdsv_oldaddress",
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
                                            children="<null>", id="pdsv_oldwhr",
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
                                            children="<null>", id="pdsv_oldeduc",
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
                                            children="<null>", id="pdsv_oldmajor",
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
                                            children="<null>", id="pdsv_oldwhn",
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
                                #             children="<null>", id="pdsv_oldeduc",
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
                                #             children="<null>", id="pdsv_oldmajor",
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
                                            children="<null>", id="pdsv_oldcse",
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
                                            children="<null>", id="pdsv_oldcseyear",
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
                                            children="<null>", id="pdsv_oldrating",
                                        ),

                                    ], width=8)
                                ], row=True),
                            ]),
                        ]),


                    ]),

                ], className='border-dark',)
            ], id = 'pdsv_oldcollapse'),
            ####

            html.Br(),
            html.Div([
                dcc.Input(id='pdsv_submit_summary', type='text', value="0")
            ], style={'display': 'none'}),
            html.Div([
                dcc.Input(id='pdsv_load_bp', type='text', value="0")
            ], style={'display': 'none'}),
            html.Div([
                dcc.Input(id='pdsv_degrees_summary', type='text', value="0")
            ], style={'display': 'none'}),


            html.Div(html.Div(
                [
                    dbc.Spinner(
                        [
                            dbc.Button("Back", color="danger", className="mr-1",
                                       id="pdsv_backbutton", href = '/settings/settings_personal_data_viewing'),
                        ],
                        color='secondary'
                    )
                ]
            ), style={"width": "auto", "display": "inline-block", "margin-right": "2%"}, id='pdsv_deletebuttondiv'),
        ]),





    ], id="pdsv_maindiv", style={'display': 'inline'}),
])

@app.callback(
    [
        Output('pdsv_title', 'children'),

        Output('pdsv_lastname', 'children'),
        Output('pdsv_firstname', 'children'),
        Output('pdsv_middlename', 'children'),
        Output('pdsv_suffixname', 'children'),
        Output('pdsv_dob', 'children'),
        Output('pdsv_pob', 'children'),

        Output('pdsv_sexatbirth', 'children'),
        Output('pdsv_civilstatus', 'children'),
        Output('pdsv_bloodtype', 'children'),
        Output('pdsv_mobilecontactnumber', 'children'),
        Output('pdsv_lanecontactnumber', 'children'),
        Output('pdsv_email', 'children'),

        Output('pdsv_citizenship', 'children'),
        Output('pdsv_typeofcit', 'children'),
        Output('pdsv_countryofcit', 'children'),
        Output('pdsv_addcurrentcountry', 'children'),
        Output('pdsv_regioncurr', 'children'),
        Output('pdsv_aprovincecurr', 'children'),

        Output('pdsv_citymuncurrent', 'children'),
        Output('pdsv_streetaddresscurr', 'children'),
        Output('pdsv_subdvillagecurr', 'children'),
        Output('pdsv_brgyaddresscurr', 'children'),
        Output('pdsv_zipcodecurr', 'children'),
        Output('pdsv_addcountryperm', 'children'),

        Output('pdsv_regionperm', 'children'),
        Output('pdsv_aprovinceperm', 'children'),
        Output('pdsv_citymunperm', 'children'),
        Output('pdsv_streetaddressperm', 'children'),
        Output('pdsv_subdvillageperm', 'children'),
        Output('pdsv_brgyaddressperm', 'children'),

        Output('pdsv_zipcodeperm', 'children'),
        Output('pdsv_gsis', 'children'),
        Output('pdsv_pagibig', 'children'),
        Output('pdsv_philhealth', 'children'),
        Output('pdsv_sss', 'children'),
        Output('pdsv_tin', 'children'),

        Output('pdsv_governmentid', 'children'),
        Output('pdsv_govidnumber', 'children'),

        Output('pdsv_currentdegreediv', 'children'),
        Output('pdsv_currenteligibilitiesdiv', 'children'),

        Output('pdsv_pobislocal', 'children'),
        Output('pdsv_pobprovince', 'children'),
        Output('pdsv_pobcity', 'children'),
        Output('pdsv_pobcountry', 'children'),

    ],

    [
        Input('url', 'search')
    ]
)

def loadpdsvpage(url):

    ctx = dash.callback_context
    parsed = urlparse.urlparse(url)
    if parse_qs(parsed.query):
        mode = str(parse_qs(parsed.query)['mode'][0])
        person_id = str(parse_qs(parsed.query)['uid'][0])
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]


        sql1 = '''
            SELECT t.title, p.person_last_name, p.person_first_name, p.person_middle_name, p.person_name_extension, p.person_dob, p.person_pob,
            s.sex, cs.civil_status_code, bt.blood_type, c.citizenship_name, ct.citizenship_type_name, p.person_country_citizenship_id,
            p.person_gsis_no, p.person_pagibig_no, p.person_philhealth_no, p.person_sss_no, p.person_tin, git.gov_id_type,
            p.person_gov_id_no

            FROM persons p
            LEFT JOIN sexes s ON p.person_sex_id = s.sex_id
            LEFT JOIN civil_statuses cs ON cs.civil_status_id = p.person_civil_status_id
            LEFT JOIN blood_types bt ON bt.blood_type_id = p.person_blood_type_id
            LEFT JOIN citizenships c ON c.citizenship_id = p.person_citizenship_id
            LEFT JOIN citizenship_types ct ON ct.citizenship_type_id = p.person_citizenship_type_id
            LEFT JOIN countries count ON count.country_id = p.person_country_citizenship_id
            LEFT JOIN government_id_types git ON p.person_gov_id_type_id = git.gov_id_type_id
            LEFT JOIN titles t ON p.person_title_id = t.title_id
            WHERE p.person_id = %s

        '''

        values1 = (person_id,)
        columns1 = ['title',
                    'person_last_name', 'person_first_name', 'person_middle_name', 'person_name_extension', 'person_dob', 'person_pob',
                    'sex', 'civil_status_code', 'blood_type', 'citizenship_name', 'citizenship_type_name', 'person_country_citizenship_id',
                    'person_gsis_no', 'person_pagibig_no', 'person_philhealth_no', 'person_sss_no', 'person_tin', 'gov_id_type',
                    'person_gov_id_no']
        df1 = securequerydatafromdatabase(sql1, values1, columns1)

        if not df1.empty:
            title = df1["title"][0]

            person_last_name = df1["person_last_name"][0]
            person_first_name = df1["person_first_name"][0]
            person_middle_name = df1["person_middle_name"][0]
            person_name_extension = str(df1["person_name_extension"][0])
            person_dob = str(df1["person_dob"][0])
            person_pob = str(df1["person_pob"][0])

            sex = str(df1["sex"][0])
            civil_status_code = str(df1["civil_status_code"][0])
            blood_type = str(df1["blood_type"][0])
            citizenship_name = str(df1["citizenship_name"][0])
            citizenship_type_name = str(df1["citizenship_type_name"][0])
            person_country_citizenship_id = str(df1["person_country_citizenship_id"][0])

            person_gsis_no = str(df1["person_gsis_no"][0])
            person_pagibig_no = str(df1["person_pagibig_no"][0])
            person_philhealth_no = str(df1["person_philhealth_no"][0])
            person_sss_no = str(df1["person_sss_no"][0])
            person_tin = str(df1["person_tin"][0])
            gov_id_type = str(df1["gov_id_type"][0])

            person_gov_id_no = str(df1["person_gov_id_no"][0])

        else:

            title = ""

            person_last_name = ""
            person_first_name = ""
            person_middle_name = ""
            person_name_extension = ""
            person_dob = ""
            person_pob = ""

            sex = ""
            civil_status_code = ""
            blood_type = ""
            citizenship_name = ""
            citizenship_type_name = ""
            person_country_citizenship_id = ""

            person_gsis_no = ""
            person_pagibig_no = ""
            person_philhealth_no = ""
            person_sss_no = ""
            person_tin = ""
            gov_id_type = ""

            person_gov_id_no = ""


        sql2 = '''
                SELECT person_contact_number
                FROM person_contact_numbers
                WHERE person_id = %s
                ORDER BY person_contact_type_id ASC
            '''

        values2 = (person_id,)
        columns2 = ['person_contact_number']
        df2 = securequerydatafromdatabase(sql2, values2, columns2)
        if not df2["person_contact_number"].empty:
            pdsv_lanecontactnumber = str(df2["person_contact_number"][0])
            pdsv_mobilecontactnumber = str(df2["person_contact_number"][1])
        else:
            pdsv_lanecontactnumber = ""
            pdsv_mobilecontactnumber = ""



        sql3 = '''
                SELECT count.country_name, r.region_name, p.prov_name, c.city_name, a.address_street, a.address_subdivision_village,
                a.address_brgy, a.address_zip_code
                FROM addresses a
                LEFT JOIN countries count ON count.country_id = a.address_country_id
                LEFT JOIN regions r ON r.region_id = a.address_region_id
                LEFT JOIN provinces p ON p.prov_id = a.address_prov_id
                LEFT JOIN cities c ON c.city_id = a.address_city_id
                WHERE a.person_id = %s
                ORDER BY address_type_id ASC
            '''

        values3 = (person_id,)
        columns3 = ['country_name', 'region_name','prov_name', 'city_name', 'address_street', 'address_subdivision_village',
                    'address_brgy', 'address_zip_code']
        df3 = securequerydatafromdatabase(sql3, values3, columns3)


        if not df3.empty:

            pdsv_addcurrentcountry = str(df3["country_name"][0])
            pdsv_regioncurr = str(df3["region_name"][0])
            pdsv_aprovincecurr = str(df3["prov_name"][0])
            pdsv_citymuncurrent = str(df3["city_name"][0])
            pdsv_streetaddresscurr = str(df3["address_street"][0])
            pdsv_subdvillagecurr = str(df3["address_subdivision_village"][0])

            pdsv_brgyaddresscurr = str(df3["address_brgy"][0])
            pdsv_zipcodecurr = str(df3["address_zip_code"][0])

            pdsv_addcountryperm = str(df3["country_name"][1])
            pdsv_regionperm = str(df3["region_name"][1])
            pdsv_aprovinceperm = str(df3["prov_name"][1])
            pdsv_citymunperm = str(df3["city_name"][1])
            pdsv_streetaddressperm = str(df3["address_street"][1])
            pdsv_subdvillageperm = str(df3["address_subdivision_village"][1])

            pdsv_brgyaddressperm = str(df3["address_brgy"][1])
            pdsv_zipcodeperm = str(df3["address_zip_code"][1])

        else:

            pdsv_addcurrentcountry = ""
            pdsv_regioncurr = ""
            pdsv_aprovincecurr = ""
            pdsv_citymuncurrent = ""
            pdsv_streetaddresscurr = ""
            pdsv_subdvillagecurr = ""

            pdsv_brgyaddresscurr = ""
            pdsv_zipcodecurr = ""

            pdsv_addcountryperm = ""
            pdsv_regionperm = ""
            pdsv_aprovinceperm = ""
            pdsv_citymunperm = ""
            pdsv_streetaddressperm = ""
            pdsv_subdvillageperm = ""

            pdsv_brgyaddressperm = ""
            pdsv_zipcodeperm = ""


        sql4 = '''
                SELECT person_email_address
                FROM person_email_addresses
                WHERE person_id = %s

            '''

        values4 = (person_id,)
        columns4 = ['person_email_address']
        df4 = securequerydatafromdatabase(sql4, values4, columns4)
        if not df4["person_email_address"].empty:
            person_email_address = str(df4["person_email_address"][0])
        else:
            person_email_address = ""

        sql10 = ''' SELECT person_degree_id, degree_name, person_program_id, program_name, person_educ_grad_date, person_educ_start_date, person_educ_end_date,
                    person_educ_school_id,school_name, person_educ_gwa_completed, person_educ_wa_major, person_number_failing_marks, person_educ_id
                    FROM persons p
                    LEFT JOIN person_educational_backgrounds peb on peb.person_id = p.person_id
                    LEFT JOIN degrees d on d.degree_id = peb.person_degree_id
                    LEFT JOIN programs prg on prg.program_id = peb.person_program_id
                    LEFT JOIN schools s on s.school_id = peb.person_educ_school_id
                    WHERE p.person_id = %s AND person_educ_delete_ind=%s'''
        values10 = (person_id, False)
        columns10 = ['person_degree_id', 'degree_name', 'person_program_id', 'program_name', 'person_educ_grad_date',
                   'person_educ_start_date', 'person_educ_end_date',
                   'person_educ_school_id', 'school_name', 'person_educ_gwa_completed', 'person_educ_wa_major',
                   'person_number_failing_marks', 'person_educ_id']
        df10 = securequerydatafromdatabase(sql10, values10, columns10)

        sessiondegreesprocesseddf = df10[['degree_name', 'program_name', 'person_educ_grad_date', 'person_educ_start_date',
                                        'person_educ_end_date', 'school_name', 'person_educ_gwa_completed',
                                        'person_educ_wa_major', 'person_number_failing_marks']].copy()
        sessiondegreesprocesseddf.columns = ["Degree", "Program", "Graduation Date", "Start Date",
                                             "End Date", "Institution", "GWA", "Weighted Average",
                                             "Number of Failing Marks"]
        deg_table = dbc.Table.from_dataframe(
            sessiondegreesprocesseddf, striped=True, bordered=True, hover=True)

        sql11 = '''
                    SELECT e.eligibility_code, pe.person_eligibility_rating, pe.person_eligibility_taken, pe.person_eligibility_poe, pe.person_eligibility_license_no, pe.person_eligibility_valid_start_date,
                    pe.person_eligibility_valid_end_date
                    FROM person_eligibilities pe
                    LEFT JOIN eligibilities e ON e.eligibility_id = pe.eligibility_id
                    WHERE pe.person_id = %s and pe.person_eligibility_delete_ind = %s
                    '''

        values11 = (person_id, False)

        columns11 = ['eligibility_code', 'person_eligibility_rating', 'person_eligibility_taken', 'person_eligibility_poe',
                   'person_eligibility_license_no', 'person_eligibility_valid_start_date',
                   'person_eligibility_valid_end_date']
        df11 = securequerydatafromdatabase(sql11, values11, columns11)

        sessioneligibilitiesprocesseddf = df11[
            ['eligibility_code', 'person_eligibility_rating', 'person_eligibility_taken', 'person_eligibility_poe',
             'person_eligibility_license_no', 'person_eligibility_valid_start_date',
             'person_eligibility_valid_end_date']].copy()
        sessioneligibilitiesprocesseddf.columns = ["Eligibility", "Rating", "Date of Exam", "Place of Conferment",
                                                   "License Number", "Eligibility Effective Start Date",
                                                   "Eligibility Effective End Date"]

        elig_table = dbc.Table.from_dataframe(
            sessioneligibilitiesprocesseddf, striped=True, bordered=True, hover=True)


        sql15 = '''
                    SELECT cit.city_name, prov.prov_name, p.person_pob_is_local, count.country_name
                    FROM persons p
                    LEFT JOIN cities cit ON cit.city_id = p.person_pob_city_id
                    LEFT JOIN countries count ON count.country_id = p.person_pob_country_id
                    LEFT JOIN provinces prov ON prov.prov_id = p.person_pob_prov_id
                    WHERE person_id = %s

                '''

        values15 = (person_id,)
        columns15 = ['city_name', 'prov_name', 'person_pob_is_local', 'country_name']

        df15 = securequerydatafromdatabase(sql15, values15, columns15)


        if not df15.empty:
            city_name = df15["city_name"][0]
            prov_name = df15["prov_name"][0]
            person_pob_is_local = str(df15["person_pob_is_local"][0])
            country_name = df15["country_name"][0]



        else:

            city_name = ""
            prov_name = ""
            person_pob_is_local = ""
            country_name = ""


        return [title,
                person_last_name, person_first_name, person_middle_name, person_name_extension, person_dob, person_pob,
                sex, civil_status_code, blood_type, pdsv_mobilecontactnumber, pdsv_lanecontactnumber, person_email_address,
                citizenship_name, citizenship_type_name, person_country_citizenship_id, pdsv_addcurrentcountry, pdsv_regioncurr, pdsv_aprovincecurr,
                pdsv_citymuncurrent, pdsv_streetaddresscurr, pdsv_subdvillagecurr, pdsv_brgyaddresscurr, pdsv_zipcodecurr, pdsv_addcountryperm,
                pdsv_regionperm, pdsv_aprovinceperm, pdsv_citymunperm, pdsv_streetaddressperm, pdsv_subdvillageperm, pdsv_brgyaddressperm,
                pdsv_zipcodeperm, person_gsis_no, person_pagibig_no, person_philhealth_no, person_sss_no, person_tin,
                gov_id_type, person_gov_id_no,
                deg_table, elig_table,
                person_pob_is_local, prov_name, city_name, country_name
                ]
    else:
        raise PreventUpdate


@app.callback(
    [
        Output("pdsv_oldcollapse", "is_open"),

        Output("pdsv_oldtitle", "children"),
        Output("pdsv_oldsex", "children"),
        Output("pdsv_olddob", "children"),
        Output("pdsv_oldcstat", "children"),
        Output("pdsv_oldcitizenship", "children"),
        Output("pdsv_oldbltype", "children"),

        Output("pdsv_oldtin", "children"),
        Output("pdsv_oldotherq", "children"),
        Output("pdsv_oldencode", "children"),
        Output("pdsv_oldhrmo", "children"),
        Output("pdsv_oldrem", "children"),
        Output("pdsv_oldcreatedat", "children"),

        Output("pdsv_oldupdatedat", "children"),
        Output("pdsv_oldapptclean", "children"),
        Output("pdsv_oldapptremarks", "children"),
        Output("pdsv_oldapptname", "children"),
        Output("pdsv_oldtimestamp", "children"),
        Output("pdsv_oldleaveclean", "children"),

        Output("pdsv_oldleaveremarks", "children"),
        Output("pdsv_oldleavename", "children"),
        Output("pdsv_oldleavetimestamp", "children"),
        Output("pdsv_oldsysclean", "children"),
        Output("pdsv_oldsysremarks", "children"),
        Output("pdsv_oldsystimestamp", "children"),

        Output("pdsv_oldleaveremarks2", "children"),
        Output("pdsv_oldleaveremarks3", "children"),
        Output("pdsv_oldaddress", "children"),

        Output("pdsv_oldwhr", "children"),
        Output("pdsv_oldeduc", "children"),
        Output("pdsv_oldmajor", "children"),
        Output("pdsv_oldwhn", "children"),

        Output("pdsv_oldcse", "children"),
        Output("pdsv_oldcseyear", "children"),
        Output("pdsv_oldrating", "children"),

    ],
    [
        Input("pdsv_oldvaluesbtn", "n_clicks")
    ],
    [
        State("pdsv_oldcollapse", "is_open"),
        State("url", "search")

    ]
)

def invitempunit(pdsv_oldvaluesbtn, pdsv_oldcollapse, url):
    ctx = dash.callback_context

    parsed = urlparse.urlparse(url)
    mode = str(parse_qs(parsed.query)['mode'][0])


    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'pdsv_oldvaluesbtn':
            if mode == "view":
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
                columns1 = ['person_old_title', 'person_old_sex','person_old_bday','person_old_cstat','person_old_citizenship','person_old_bl_type',
                            'person_old_tin', 'person_old_other_q','person_old_encode','person_old_hrmo','person_old_rem','person_old_created_at',
                            'person_old_updated_at', 'person_old_appt_clean','person_old_appt_remarks','person_old_appt_name','person_old_appt_timestamp','person_old_leave_clean',
                            'person_old_leave_remarks', 'person_old_leave_name','person_old_leave_timestamp','person_old_sys_clean','person_old_sys_remarks','person_old_sys_timestamp',
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
                columns3 = ['person_old_whr', 'person_old_educ', 'person_old_major', 'person_old_whn']
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
                columns4 = ['person_old_cse', 'person_old_cse_year', 'person_eligibility_old_rating']
                df4 = securequerydatafromdatabase(sql4, values4, columns4)

                person_old_cse = df4["person_old_cse"][0]
                person_old_cse_year = df4["person_old_cse_year"][0]
                person_eligibility_old_rating = df4["person_eligibility_old_rating"][0]

                oldvalues = [
                        person_old_title, person_old_sex, person_old_bday, person_old_cstat, person_old_citizenship, person_old_bl_type,
                        person_old_tin, person_old_other_q, person_old_encode, person_old_hrmo, person_old_rem, person_old_created_at,
                        person_old_updated_at, person_old_appt_clean, person_old_appt_remarks, person_old_appt_name, person_old_appt_timestamp, person_old_leave_clean,
                        person_old_leave_remarks, person_old_leave_name, person_old_leave_timestamp, person_old_sys_clean, person_old_sys_remarks, person_old_sys_timestamp,
                        person_old_leave_remarks2, person_old_leave_remarks3, person_old_address,
                        person_old_whr, person_old_educ, person_old_major, person_old_whn,
                        person_old_cse, person_old_cse_year, person_eligibility_old_rating]

                return [not pdsv_oldcollapse] + oldvalues

            else:
                raise PreventUpdate
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback(
    [
      Output('pdsv_proxydiv1', 'style'),
      Output('pdsv_proxydiv2', 'style'),
      Output('pdsv_proxydiv3', 'style'),
      Output('pdsv_proxydiv4', 'style'),
    ],
    [
        Input('pdsv_pobislocal', 'children')
    ]
)

def pdsv_pobformatting(pdsv_pobislocal):
    if pdsv_pobislocal == "True":
        return [{'display':'inline'}, {'display':'inline'}, {'display':'none'}, {'display':'none'}]
    else:
        return [{'display': 'none'}, {'display': 'none'}, {'display': 'inline'}, {'display': 'inline'}]
