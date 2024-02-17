import base64
import logging
import os
import re
from typing import Dict, List, Tuple

import dash_bootstrap_components as dbc
import dash_daq as daq
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html, Input, Output, State, exceptions, no_update
from django.conf import settings
from django.http import HttpRequest
from django_plotly_dash import DjangoDash
from multipledispatch import dispatch
from skimage import io

from worldbuilder.dash import map_cards
from worldbuilder.models import Map, PoiOnMap, PointOfInterest

logger = logging.getLogger('__name__')
app = DjangoDash(
    "WorldBuilder",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)
config = {
    'displayModeBar': True, 
    'responsive': True,
    "modeBarButtonsToAdd": [
        "drawline",
        "drawopenpath",
        "drawclosedpath",
        "drawcircle",
        "drawrect",
        "eraseshape",
    ]
}
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}
image_graph = dcc.Graph(
    id='map-graph',
    figure=None,
    config=config,
    style={'height': '95vh'}  # Set the height to 95% of the viewport height
)
default_rgb = dict(r=255, g=0, b=0, a=1)
colour_picker = daq.ColorPicker(
    id="annotation-color-picker",
    label='Fill Color Picker',
    value=dict(rgb=default_rgb),
    size=120,
)
outline_colour_picker = daq.ColorPicker(
    id="annotation-color-picker-outline",
    label='Line Color Picker',
    value=dict(rgb=default_rgb),
    size=120,
)
container = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col([colour_picker, outline_colour_picker], md=1, align="left", ),
                dbc.Col(image_graph, md=8, align="right",),
                dbc.Col([map_cards.hidden_card()], md = 3, align='right', id='click-data'),
                dbc.Col([
                    dcc.Markdown("""
                        **Debug**
                    """),
                    html.Pre(id='debug-data', style=styles['pre']),
                ], md = 3, align='right')
            ],
        ),
        
    ],
    fluid=True,
)
memory_store = dcc.Store(
    id='memory_store',
    # storage_type='session',
    data=dict()
)
app.layout = html.Div([
    container,
    memory_store
])

@app.callback(
    Output("map-graph", "figure"),
    Input("annotation-color-picker", "value"),
    Input("annotation-color-picker-outline", "value"),
    State("memory_store", "data"),
    prevent_initial_call=True,
)
def on_style_change(color_value, line_colour_value, data):
    _, fig = map_fig(data['map_id'], data['image_url'])
    if fig is None:
        # Handle the case when the figure is None
        raise exceptions.PreventUpdate
    c=color_value["rgb"]
    colour = daq_rgb_to_dash(c)
    lc=line_colour_value["rgb"]
    line_colour = daq_rgb_to_dash(lc)

    update_kwargs = {
        "newshape": dict(
            fillcolor=colour,
            line_color=line_colour
        ),
    }
    if shapes := data.get('shapes'):
        update_kwargs['shapes'] = shapes
    fig.update_layout(
        **update_kwargs
    )
    return fig

def daq_rgb_to_dash(c: str):
    return f'rgb({c["r"]},{c["g"]},{c["b"]},{c["a"]})'

@app.callback(
    Output("memory_store", "data"),
    Input("map-graph", "relayoutData"),
    State("memory_store", "data"),
    prevent_initial_call=True,
)
def on_new_annotation(relayout_data, data):
    if not relayout_data:
        return no_update

    if "dragmode" in relayout_data:
        data['dragmode'] = relayout_data["dragmode"]
        return data

    if "shapes" in relayout_data:
        data['shapes'] = relayout_data["shapes"]
        return data
    
    shapes = data.get('shapes')
    if not shapes:
        return no_update

    pattern = r'shapes\[([0-9]+)].([xy][01])'
    for key in relayout_data:
        result = re.search(pattern, key)
        if not result:
            continue
        index = int(result.group(1))
        attr = result.group(2)
        value = relayout_data[key]
        shapes[index][attr] = value
    return data

@app.callback(
    Output('click-data', 'children'),
    Input('map-graph', 'clickData'),
    Input('btn-close-poi-form', 'n_clicks'),
    State("memory_store", "data"),
    prevent_initial_call=True,)
def display_click_data(click_data: Dict, close_clicks, data: Dict):
    if close_clicks:
        prev_clicks = data.get('card_closes', 0)
        data['card_closes'] = close_clicks
        if close_clicks > prev_clicks:
            return map_cards.hidden_card()
    if not click_data:
        return map_cards.hidden_card()
    points: List[Dict] = click_data.get('points')
    if not points:
        return map_cards.hidden_card()
    point = points[0]
    point_data = point.get('customdata')
    if point_data:
        return map_cards.display_poi_card(point_data)
    if ("x" in point) and ("y" in point):
        return map_cards.new_poi_card(point["x"], point["y"], data['map_id'])
    return map_cards.hidden_card()

@app.callback(
    Output('upload-thumbnail-poi-form', 'children'),
    Input('upload-thumbnail-poi-form', 'contents'),
    State('upload-thumbnail-poi-form', 'filename'),
    prevent_initial_call=True,)
def update_poi_thumbnail_upload(contents, name):
    if contents is not None:
        return html.Div([
            html.A([
                dcc.Markdown(f"""
                        _Thumbnail:_ {name}
                    """),
                ])
        ])
    return no_update

@app.callback(
    Output('store-poi-form', 'data'),
    Input('point-poi-form', 'children'),
    Input('name-input-poi-form', 'value'),
    Input('description-markdown-poi-form', 'value'),
    Input('upload-thumbnail-poi-form', 'contents'),
    Input('map-dropdown-poi-form', 'value'),
    State('upload-thumbnail-poi-form', 'filename'),
    prevent_initial_call=True,)
def update_poi_form(point, name, description, thumbnail_data, poi_map, thumbnail_filename):
    pattern = r'\[(\d+),(\d+)]'
    result = re.search(pattern, point)
    x, y = int(result.group(1)), int(result.group(2))
    return {
        'x': x,
        'y': y,
        'name': name,
        'description': description,
        'poi_map': poi_map,
        'thumbnail_data': thumbnail_data,
        'thumbnail_filename': thumbnail_filename
    }

@app.callback(
    Output('debug-data', 'children'),
    Input('button-create-poi', 'n_clicks'),
    State('store-poi-form', 'data'),
    State('memory_store', 'data'),
    prevent_initial_call=True,)
def on_button_poi_create(clicks, poi_form, data):
    if not clicks:
        return no_update
    thumbnail_data = poi_form['thumbnail_data'].encode("utf8").split(b";base64,")[1]
    thumbnail_filename = poi_form['thumbnail_filename']
    thumbnail_path = os.path.join('thumbnails', thumbnail_filename)
    thumbnail_fullpath = os.path.join(settings.MEDIA_ROOT, thumbnail_path)
    with open(thumbnail_fullpath, "wb") as fp:
        fp.write(base64.decodebytes(thumbnail_data))
    curr_map = Map.objects.get(pk=data['map_id'])
    poi = PointOfInterest(
        name=poi_form['name'],
        description = description if (description := poi_form.get('name')) else None,
        thumbnail = thumbnail_path,
        poi_map = Map.objects.get(pk=poi_form['poi_map']) if poi_form['poi_map'] else None
    )
    poi.full_clean()
    poi.save()
    poi.parent_maps.add(curr_map, through_defaults={
        'x': poi_form['x'],
        'y': poi_form['y']
    })
    poi.full_clean()
    poi.save()
    return 'Return creating POI'

@app.callback(
    Output('add-poi-preview-div', 'children'),
    Input('add-poi-dropdown', 'value'),
)
def update_add_poi_preview(selected_value):
    poi = PointOfInterest.objects.get(pk=selected_value)
    return map_cards.add_poi_preview(poi) if poi else no_update

@dispatch(str, str)
def map_fig(map_id: str, image_url: str) -> Tuple[Map, go.Figure]:
    try:
        map = Map.objects.get(pk=map_id)
    except Exception:
        map = Map.objects.last()

    fig = build_map_fig(map, image_url)
    return map, fig

@dispatch(HttpRequest, str)
def map_fig(request: HttpRequest, id: str) -> Tuple[Map, go.Figure, str]:
    try:
        map = Map.objects.get(pk=id)
    except Exception:
        map = Map.objects.last()

    image_url = request.build_absolute_uri(map.image.url)
    return map, build_map_fig(map, image_url), image_url

def build_map_fig(map: Map, image_url: str) -> go.Figure:
    img = io.imread(image_url)
    fig = px.imshow(img)
    x, y, customdata = [], [], []
    for poi in map.points_of_interest.all():
        coords = PoiOnMap.objects.get(map=map, point_of_interest=poi)
        x.append(coords.x)
        y.append(coords.y)
        customdata.append({
            'pk': poi.pk
        })
        # fig.add_shape(type="circle",
        #     xref="x", yref="y",
        #     x0=coords.x-50, y0=coords.y-50, x1=coords.x+50, y1=coords.y+50,
        #     line_color="LightSeaGreen",
        #     fillcolor="PaleTurquoise",
        # )
    fig.add_trace(go.Scatter(x=x, y=y, customdata=customdata, marker=dict(color='red', size=16), mode='markers'))
    fig.update_layout(
        dragmode="drawcircle",
        newshape= dict(
            fillcolor= daq_rgb_to_dash(default_rgb),
        ),
    )
    return fig

def set_figure_map(request: HttpRequest, id: str) -> Map:
    map, fig, image_url = map_fig(request, id)
    memory_store.data=dict(
        map_id=id,
        image_url=image_url,
        dragmode="drawcircle"
    )
    image_graph.figure = fig
    return map

def map_sliders(img_width, img_height) -> list:
    # Create steps for width slider
    width_steps = [
        dict(
            method="relayout",
            args=[{"width": i}], 
        ) for i in range(img_width + 1)
    ]
    width_slider = dict(
        active=min(img_width, 800),
        currentvalue={"prefix": "Width: "},
        pad={"t": 150},
        steps=width_steps,
        yanchor='top'
    )
    height_steps = [
        dict(
            method="relayout",
            args=[{"height": i}], 
        ) for i in range(img_width + 1)
    ]
    height_slider = dict(
        active=min(img_height, 600),
        currentvalue={"prefix": "Height: "},
        pad={"t": 50},
        steps=height_steps,
        yanchor='top'
    )
    return [width_slider, height_slider]
