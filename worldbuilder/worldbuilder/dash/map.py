import logging
import re
from typing import Tuple

import dash_bootstrap_components as dbc
import dash_daq as daq
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html, Input, Output, State, exceptions, no_update
from django.http import HttpRequest
from django_plotly_dash import DjangoDash
from multipledispatch import dispatch
from skimage import io

from worldbuilder.models.map import Map, PoiOnMap

logger = logging.getLogger('__name__')
app = DjangoDash(
    "WorldBuilder",
    external_stylesheets=[dbc.themes.BOOTSTRAP]
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
image_graph = dcc.Graph(
    id='map-graph',
    figure=None,
    config=config,
    style={'height': '95vh'}  # Set the height to 95% of the viewport height
)
default_rgb = dict(r=255, g=0, b=0, a=1)
colour_picker = daq.ColorPicker(
    id="annotation-color-picker",
    label='Color Picker',
    value=dict(rgb=default_rgb),
    size=120,
)
container = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(colour_picker, md=1, align="left",),
                dbc.Col(image_graph, md=10, align="right",),
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
    State("memory_store", "data"),
    prevent_initial_call=True,
)
def on_style_change(color_value, data):
    print('Style change')
    _, fig = map_fig(data['map_id'], data['image_url'])
    if fig is None:
        # Handle the case when the figure is None
        raise exceptions.PreventUpdate
    c=color_value["rgb"]
    colour = daq_rgb_to_dash(c)

    update_kwargs = {
        "newshape": dict(
            fillcolor=colour
        ),
        "dragmode": data.get('dragmode')
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
    for poi in map.points_of_interest.all():
        coords = PoiOnMap.objects.get(map=map, point_of_interest=poi)
        fig.add_shape(type="circle",
            xref="x", yref="y",
            x0=coords.x-50, y0=coords.y-50, x1=coords.x+50, y1=coords.y+50,
            line_color="LightSeaGreen",
            fillcolor="PaleTurquoise",
        )
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
