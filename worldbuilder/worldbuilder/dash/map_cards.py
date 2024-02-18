import dash_bootstrap_components as dbc
from dash import dcc, html
from django.urls import reverse

from markdown_input_component import MarkdownInputComponent
from worldbuilder.models import Map, PointOfInterest


def card_header():
    return dbc.CardHeader(
        [
            html.Button(
                id='btn-close-poi-form',
                className='btn-close',
                **{
                    'data-dismiss':'alert',
                    'data-target':'#cardpoiform',
                    'aria-label':'Close',
                }
            ),
        ],
        style={"height": "40px"},
        class_name='card-header border-bottom-0'  # bg-transparent
    )

def new_poi_card(x, y, map_id):
    map_options = [
       { 'label':map.name, 'value': map.pk }  for map in Map.objects.exclude(pk=map_id)
    ]
    return dbc.Card(
        [
            card_header(),
            dbc.Tabs([new_poi_tab(x, y, map_options), add_poi_tab(x, y)], active_tab='create_poi')
        ],
        style={"height": "90vh"},
        id='cardright',
    )

def add_poi_tab(x, y):
    pois = PointOfInterest.objects.order_by('name').all()
    options = { poi.pk: poi.name for poi in pois }
    return dbc.Tab(
        [
            dbc.CardBody(
                [
                    html.H4(f"[{x},{y}]", className="card-title", id='point-add-poi-form'),
                    html.P(
                        "Add existing point of interest",
                        className="card-text",
                    ),
                    html.Hr(),
                    dcc.Dropdown(
                        options, list(options.keys())[0], id='dropdown-add-poi-form',
                    ),
                    html.Div([], id="preview-div-add-poi-form", style={'overflow-y': 'scroll', 'maxHeight': '50vh'}),
                    html.Br(),
                    dbc.Button("Add Point of Interest", color="primary", id="button-add-poi-form"),
                    dcc.Store(
                        id='store-add-poi-form',
                        data=dict()
                    ),
                ],
            )
        ],
        label='Add POI',
        tab_id='add_poi'
    )

def add_poi_preview(poi: PointOfInterest):
    return [
        dbc.CardImg(src=poi.thumbnail.url, top=False),
        html.H4(poi.name, className="card-title",),
        dcc.Markdown(
            poi.description,
            className="card-text",
        ),
    ]

def new_poi_tab(x, y, map_options):
    return dbc.Tab(
        [
            dbc.CardBody(
                [
                    html.H4(f"[{x},{y}]", className="card-title", id='point-poi-form'),
                    html.P(
                        "Create a new point of interest",
                        className="card-text",
                    ),
                    html.Hr(),
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Name"),
                            dbc.Input(placeholder="New Point of Interest", required=True, id='name-input-poi-form')
                        ],
                        className="sb-3",
                    ),
                    html.Br(),
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Description"), 
                            MarkdownInputComponent(id='description-markdown-poi-form', value='',),
                         ],
                        className="sb-3",
                    ),
                    html.Br(),
                    dcc.Upload(
                        id='upload-thumbnail-poi-form',
                        children=html.Div([
                            html.A('Select Thumbnail')
                        ]),
                        style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                        }
                    ),
                    html.Br(),
                    dbc.InputGroup(
                        [dbc.InputGroupText("Map for POI"), dcc.Dropdown(options=map_options, id='map-dropdown-poi-form')],
                        className="mb-3",
                    ),
                    html.Br(),
                    dbc.Button(
                        "Create Point of Interest", color="primary", id="button-create-poi"
                    ),
                    dcc.Store(
                        id='store-poi-form',
                        data=dict()
                    ),
                ],
                style={'overflow-y': 'scroll', 'maxHeight': '80vh'}
            ),
        ],
        label='Create POI',
        tab_id='create_poi'
    )

def display_poi_card(point_data):
    pk = point_data.get('pk')
    poi = PointOfInterest.objects.get(pk=pk)
    return dbc.Card(
        [
            card_header(),
            dbc.CardImg(src=poi.thumbnail.url, top=False),
            dbc.CardBody(
                [
                    html.H4(poi.name, className="card-title",),
                    dcc.Markdown(
                        poi.description,
                        className="card-text",
                    ),
                ] + ([dbc.Button(
                    "Go to map of POI", color="primary", href=f"{reverse('dash_map')}?id={poi.poi_map.pk}",
                    target="_blank",
                    external_link=True,
                )] if poi.poi_map else [])
                
            ),
        ],
        style={"height": "90vh"},
        id='cardright',
    )

def hidden_card():
    return dbc.Card(
        [card_header()],
        style={"height": "90vh", "visibility": "hidden", "width": "0px"},
        id='cardright',
    )
