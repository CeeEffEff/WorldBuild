from typing import Tuple

import plotly.express as px
import plotly.graph_objects as go
from django.http import HttpRequest
from skimage import io

from worldbuilder.models import Map, PoiOnMap, PointOfInterest
from worldbuilder.dash.utils import daq_rgb_to_dash
from worldbuilder.dash.constants import (
    DEFAULT_RGB,
)

# ------------------------------------------------------------------------------------------------
# Helper
# ------------------------------------------------------------------------------------------------


def get_map_and_figure(map_id: str, image_url: str) -> Tuple[Map, go.Figure]:
    try:
        map = Map.objects.get(pk=map_id)
    except Exception:
        map = Map.objects.last()

    fig = build_map_fig(map, image_url)
    return map, fig


def init_map_and_figure(request: HttpRequest, id: str) -> Tuple[Map, go.Figure, str]:
    try:
        map = Map.objects.get(pk=id)
    except Exception:
        map = Map.objects.last()

    image_url = request.build_absolute_uri(map.image.url)
    return map, build_map_fig(map, image_url), image_url


def build_map_fig(map: Map, image_url: str) -> go.Figure:
    img = io.imread(image_url)
    fig = px.imshow(img)
    x, y, customdata, names = [], [], [], []
    for poi in map.points_of_interest.all():
        poi: PointOfInterest = poi
        print(f"Adding poi to map fig: {poi.name}")
        coords = PoiOnMap.objects.get(map=map, point_of_interest=poi)
        x.append(coords.x)
        y.append(coords.y)
        customdata.append({"pk": poi.pk})
        names.append(poi.name)
        # fig.add_shape(type="circle",
        #     xref="x", yref="y",
        #     x0=coords.x-50, y0=coords.y-50, x1=coords.x+50, y1=coords.y+50,
        #     line_color="LightSeaGreen",
        #     fillcolor="PaleTurquoise",
        # )
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            customdata=customdata,
            marker=dict(color="red", size=16),
            mode="markers",
            hovertext=names,
            name="POI",
        )
    )
    fig.update_layout(
        dragmode="drawcircle",
        newshape=dict(
            fillcolor=daq_rgb_to_dash(DEFAULT_RGB),
        ),
    )
    return fig


def map_sliders(img_width, img_height) -> list:
    # Create steps for width slider
    width_steps = [
        dict(
            method="relayout",
            args=[{"width": i}],
        )
        for i in range(img_width + 1)
    ]
    width_slider = dict(
        active=min(img_width, 800),
        currentvalue={"prefix": "Width: "},
        pad={"t": 150},
        steps=width_steps,
        yanchor="top",
    )
    height_steps = [
        dict(
            method="relayout",
            args=[{"height": i}],
        )
        for i in range(img_width + 1)
    ]
    height_slider = dict(
        active=min(img_height, 600),
        currentvalue={"prefix": "Height: "},
        pad={"t": 50},
        steps=height_steps,
        yanchor="top",
    )
    return [width_slider, height_slider]
