import logging
from typing import Dict, List

import dash_bootstrap_components as dbc
import dash_daq as daq
import plotly.express as px
# import plotly.graph_objects as go
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django_plotly_dash import DjangoDash
from dash import dcc, html, Input, Output, State, callback, exceptions
from plotly.offline import plot
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from skimage import io


from worldbuilder.models.map import Map, PointOfInterest, PoiOnMap
from worldbuilder.request_form import RequestForm

logger = logging.getLogger('__name__')
app = DjangoDash(
    "WorldBuilder",
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
app.layout = html.Div()
# app.layout = html.Div([
#     dcc.Graph(
#         id='map-graph',
#         figure=px.bar(),
#         # config=config,
#         style={'height': '95vh'}  # Set the height to 95% of the viewport height
#     ),
#     daq.ColorPicker(
#         id="annotation-color-picker",
#         label='Color Picker',
#         value=dict(rgb=dict(r=255, g=0, b=0, a=1)),
#         size=164,
#     )]
# )

@app.callback(
    Output("map-graph", "figure"),
    Input("annotation-color-picker", "value"),
    # State("map-graph", "figure"),
    State("session_store", "data"),
    prevent_initial_call=True,
)
def on_style_change(color_value, data):
    print('Style change')
    updated_fig = dash_map_fig(data['map_id'], data['image_url'])
    if updated_fig is None:
        # Handle the case when the figure is None
        raise exceptions.PreventUpdate
    c=color_value["rgb"]
    colour = f'rgb({c["r"]},{c["g"]},{c["b"]},{c["a"]})'
    
    updated_fig.update_layout(
        newshape=dict(
            # opacity=slider_value,
            fillcolor=colour
        ),
    )
    
    return updated_fig


@api_view(['GET'])
@permission_classes([])
def about(request: HttpRequest):
    return render(request, 'about.html')


@api_view(['GET'])
@permission_classes([])
def profile(request: HttpRequest):
    return redirect('request')


@api_view(['GET', 'POST'])
@permission_classes([])
def request(request: HttpRequest):
    uid = request.session.get('_auth_user_id', None)
    user = User.objects.get(id=uid) if uid else None
    if not user:
        return redirect('login')
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            params = RequestParams(request)
            params.use_vectorstore = {VECTORSTORE: form.cleaned_data['use_timeout_content']}
            context_items = []
            try:
                client = Client(streaming=False, **params.init_kwargs)
                data = client.run(**params.run_kwargs)
                context = client._curr_context
                if params.use_vectorstore:
                    get_context_items(context_items, context)
            except Exception as e:
                data = [{'Error': f'Exception in Client: {e}'}]

            return render(request, "results.html", {"data": data, "knn_results": context_items})
    else:
        form = RequestForm()

    return render(request, "request.html", {"form": form})


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

def map(request: HttpRequest):
    id = request.GET.get('id', default=None)
    try:
        map = Map.objects.get(pk=id)
    except Exception:
        map = Map.objects.last()
    
    url = request.build_absolute_uri(map.image.url)
    img = io.imread(
        url,
    )
    fig = px.imshow(img)
    fig.update_layout(
        autosize=True,
        sliders = map_sliders(map.image.width, map.image.height),
        newshape=dict(fillcolor="cyan", opacity=0.3, line=dict(color="darkblue", width=8)),
    )
    img_plot = plot(fig, output_type="div")
    context = {'plot_div': img_plot}
    return render(request, 'map.html', context)

def dash_map(request: HttpRequest):
    map_id = request.GET.get('id', default=None)
    width = request.session.get('width')
    height = request.session.get('height')
    ratio = height / width if width and height else 0.5
    map, fig, image_url = request_dash_map_fig(request, map_id)
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
        figure=fig,
        config=config,
        style={'height': '95vh'}  # Set the height to 95% of the viewport height
    )
    colour_picker = daq.ColorPicker(
        id="annotation-color-picker",
        label='Color Picker',
        value=dict(rgb=dict(r=255, g=0, b=0, a=1)),
        size=164,
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
    session_store = dcc.Store(
        id='session_store',
        storage_type='session',
        data=dict(
           map_id=map_id,
           image_url=image_url
        )
    )
    # Update the app layout outside the view function
    app.layout.children = [container, session_store]
    # app.layout = html.Div(
    #     # dcc.Store(id='session_store', storage_type='session', data=),
    #     container
    # )
    image_ratio = map.image.height / map.image.width
    context = {
        'height_ratio': min(image_ratio, ratio)
    }
    return render(request, 'dash_map.html', context)

def request_dash_map_fig(request, id):
    try:
        map = Map.objects.get(pk=id)
    except Exception:
        map = Map.objects.last()

    image_url = request.build_absolute_uri(map.image.url)
    img = io.imread(image_url)

    fig = px.imshow(img)
    for poi in map.points_of_interest.all():
        poi: PointOfInterest = poi
        coords = PoiOnMap.objects.get(map=map, point_of_interest=poi)
        fig.add_shape(type="circle",
            xref="x", yref="y",
            x0=coords.x-50, y0=coords.y-50, x1=coords.x+50, y1=coords.y+50,
            line_color="LightSeaGreen",
            fillcolor="PaleTurquoise",
        )
    
    return map,fig,image_url

def dash_map_fig(map_id, image_url):
    try:
        map = Map.objects.get(pk=map_id)
    except Exception:
        map = Map.objects.last()

    img = io.imread(image_url)

    fig = px.imshow(img)
    for poi in map.points_of_interest.all():
        poi: PointOfInterest = poi
        coords = PoiOnMap.objects.get(map=map, point_of_interest=poi)
        fig.add_shape(type="circle",
            xref="x", yref="y",
            x0=coords.x-50, y0=coords.y-50, x1=coords.x+50, y1=coords.y+50,
            line_color="LightSeaGreen",
            fillcolor="PaleTurquoise",
        )
    return fig

@api_view(['GET'])
@permission_classes([])
def session_screen_size(request: HttpRequest):
    width = request.GET.get('width', default=None)
    height = request.GET.get('height', default=None)
    print(f'Setting session screen size {width}x{height}')
    if not width or not height:
        return
    try:
        width, height = int(width), int(height)
    except Exception:
        return
    request.session['width'] = width
    request.session['height'] = height
    return Response(b'', status=status.HTTP_200_OK)

def maps(request):
    maps = Map.objects.all()
    context = {'maps': maps}
    return render(request, 'maps.html', context)
