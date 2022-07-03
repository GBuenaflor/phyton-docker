import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from apps import commonmodules
import dash_bootstrap_components as dbc
import base64
from app import app
from dash.exceptions import PreventUpdate

image_filename = 'static/HRDO.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

layout = html.Div([
    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), height="85px", style={'textAlign':'center', 'marginLeft':'95px'}),
    html.P(" "),
    dbc.Card(
    [
        dbc.CardHeader("Site Information"),
        dbc.CardBody(
            [
                html.H4("About this software:", className="card-title", style={'textAlign':'left'}),
                html.Hr(),
                dcc.Markdown("""
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec sagittis urna ac semper consequat. Pellentesque iaculis tellus nec erat pretium, a fermentum diam luctus. Nunc metus justo, lobortis eu magna vel, laoreet volutpat tellus. Nunc in dolor vel massa vehicula tincidunt consequat accumsan lorem. Cras vitae leo a felis vestibulum tempor. Aenean pretium ullamcorper turpis, sed vehicula diam luctus et. Duis in condimentum ipsum, in accumsan neque. Phasellus diam augue, cursus non erat sed, pulvinar imperdiet ex. Nulla libero leo, vestibulum at semper sed, condimentum eget dui. Aliquam eu imperdiet libero. Vivamus in neque turpis. In a arcu vehicula, auctor erat at, porta sapien. Vestibulum ac convallis mi. Vivamus id libero convallis, fermentum ipsum eu, bibendum arcu.

Maecenas eu dolor in mi elementum scelerisque. Maecenas a risus non enim tempor consequat. Sed dapibus egestas sapien, eu consequat metus laoreet quis. Interdum et malesuada fames ac ante ipsum primis in faucibus. Sed sodales in mauris eget molestie. Duis vel velit vulputate, volutpat est eu, rutrum leo. Sed eu lorem lectus. Praesent felis ex, placerat vitae pulvinar non, mattis sit amet urna. Ut vel elit at felis aliquet placerat.                   

                """, style={'textAlign':'left'})
            ]
        ),
        dbc.CardFooter(html.A("Return to log-in page", href='/login', style={
                    "textDecoration": "underline", "cursor": "pointer"}),
            
            
            ),
    ],
    style={"width": "50rem"},
)
    
    
    ], style={"width": "30rem", 'marginLeft':'198'}, className='text-center')