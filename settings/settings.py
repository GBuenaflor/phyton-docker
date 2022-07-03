import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from apps import commonmodules
from dash.exceptions import PreventUpdate
from app import app
from apps import home

layout = html.Div([
    commonmodules.get_header(),
    commonmodules.get_menu(),
    commonmodules.get_common_variables(),
    html.H3('Settings'),
    commonmodules.get_settings_menu(),

#    dbc.Button("Magrehistro", id="btninput2", color="primary", block=True),

    # html.Div(id="outputdiv2"),
    # dcc.Graph(
    #     id='example-graph',
    #     figure={
    #         'data': [
    #             {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'SF'},
    #             {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'line', 'name': u'Montréal'},
    #         ],
    #         'layout': {
    #             'title': 'Dash Data Visualization'
    #         }
    #     }
    # ),
])
# commonmodules.toggle_menu_colors(app)


#
# @app.callback(
#     [Output('outputdiv2', 'children'),
#      ],
#     [
#         Input('store1', 'modified_timestamp'),
#         Input('btninput2', 'n_clicks'),
#     ],
#     [
#         State('store1', 'data'),
#     ]
#
# )
# def querysublinics2(store1,n_clicks, store1data):
#     print(store1data)
#     if store1data:
#         return [store1data ]
#     else:
#         raise PreventUpdate
