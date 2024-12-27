import re
from typing import Dict, List

import dash
from dash import Input, Output, State, dcc, exceptions, html, no_update
import dash_bootstrap_components as dbc
import dash_daq as daq
from django.http import HttpRequest
from django_plotly_dash import DjangoDash

from worldbuilder.dash import poi_cards
from worldbuilder.dash.map_figure import get_map_and_figure, init_map_and_figure
from worldbuilder.dash.utils import daq_rgb_to_dash
from worldbuilder.dash.constants import DEFAULT_RGB
from worldbuilder.dash.utils import try_write_thumbnail_from_form
from worldbuilder.models import Map, PointOfInterest


app = DjangoDash(
    "WorldBuilder",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)
config = {
    "displayModeBar": True,
    "responsive": True,
    "modeBarButtonsToAdd": [
        "drawline",
        "drawopenpath",
        "drawclosedpath",
        "drawcircle",
        "drawrect",
        "eraseshape",
    ],
}
styles = {"pre": {"border": "thin lightgrey solid", "overflowX": "scroll"}}
image_graph = dcc.Graph(
    id="map-graph",
    figure=None,
    config=config,
    style={"height": "95vh"},  # Set the height to 95% of the viewport height
)
colour_picker = daq.ColorPicker(
    id="annotation-color-picker",
    label="Fill Color Picker",
    value=dict(rgb=DEFAULT_RGB),
    size=120,
)
outline_colour_picker = daq.ColorPicker(
    id="annotation-color-picker-outline",
    label="Line Color Picker",
    value=dict(rgb=DEFAULT_RGB),
    size=120,
)
container = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [colour_picker, outline_colour_picker],
                    md=1,
                    align="left",
                ),
                dbc.Col(
                    image_graph,
                    md=8,
                    align="right",
                ),
                dbc.Col(
                    [poi_cards.hidden_card()], md=3, align="right", id="click-data"
                ),
                dbc.Col(
                    [
                        dcc.Markdown(
                            """
                        **Debug**
                    """
                        ),
                        html.Pre(id="debug-data", style=styles["pre"]),
                    ],
                    md=3,
                    align="right",
                ),
            ],
        ),
    ],
    fluid=True,
)
memory_store = dcc.Store(
    id="memory_store",
    # storage_type='session',
    data=dict(),
)

app.layout = html.Div([container, memory_store])


def set_figure_map(request: HttpRequest, id: str) -> Map:
    map, fig, image_url = init_map_and_figure(request, id)
    memory_store.data = dict(map_id=id, image_url=image_url, dragmode="drawcircle")
    image_graph.figure = fig
    return map


# ------------------------------------------------------------------------------------------------
# Map Callbacks
# ------------------------------------------------------------------------------------------------


@app.callback(
    Output("memory_store", "data"),
    Input("map-graph", "relayoutData"),
    State("memory_store", "data"),
    prevent_initial_call=True,
)
def on_toolbar_change(relayout_data, data):
    if not relayout_data:
        return no_update

    if "dragmode" in relayout_data:
        data["dragmode"] = relayout_data["dragmode"]
        return data

    if "shapes" in relayout_data:
        data["shapes"] = relayout_data["shapes"]
        return data

    shapes = data.get("shapes")
    if not shapes:
        return no_update

    pattern = r"shapes\[([0-9]+)].([xy][01])"
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
    Output("map-graph", "figure"),
    Input("button-create-poi", "n_clicks"),
    Input("annotation-color-picker", "value"),
    Input("annotation-color-picker-outline", "value"),
    State("store-poi-form", "data"),
    State("memory_store", "data"),
    prevent_initial_call=True,
)
def update_graph_figure(clicks, color_value, line_colour_value, poi_form, data):
    triggered_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    print(triggered_id)
    if triggered_id == "button-create-poi":
        return on_button_poi_create(clicks, poi_form, data)
    elif triggered_id in ("annotation-color-picker", "annotation-color-picker-outline"):
        return on_colour_picker_change(color_value, line_colour_value, data)


def on_colour_picker_change(color_value, line_colour_value, data):
    _, fig = get_map_and_figure(data["map_id"], data["image_url"])
    if fig is None:
        # Handle the case when the figure is None
        raise exceptions.PreventUpdate
    c = color_value["rgb"]
    colour = daq_rgb_to_dash(c)
    lc = line_colour_value["rgb"]
    line_colour = daq_rgb_to_dash(lc)

    update_kwargs = {
        "newshape": dict(fillcolor=colour, line_color=line_colour),
    }
    if shapes := data.get("shapes"):
        update_kwargs["shapes"] = shapes
    fig.update_layout(**update_kwargs)
    return fig


# ------------------------------------------------------------------------------------------------
# POI Callbacks
# ------------------------------------------------------------------------------------------------


def on_button_poi_create(clicks, poi_form, data):
    if not clicks:
        return no_update
    curr_map = Map.objects.get(pk=data["map_id"])
    poi = PointOfInterest(
        name=poi_form["name"],
        description=poi_form.get("description", None),
        poi_map=(
            Map.objects.get(pk=poi_form["poi_map"]) if poi_form["poi_map"] else None
        ),
    )
    if thumbnail_path := try_write_thumbnail_from_form(poi_form):
        poi.thumbnail = thumbnail_path
    poi.full_clean()
    poi.save()
    poi.parent_maps.add(
        curr_map, through_defaults={"x": poi_form["x"], "y": poi_form["y"]}
    )
    poi.full_clean()
    poi.save()

    _, fig = get_map_and_figure(data["map_id"], data["image_url"])
    if fig is None:
        # Handle the case when the figure is None
        raise exceptions.PreventUpdate
    return fig


@app.callback(
    Output("click-data", "children"),
    Input("map-graph", "clickData"),
    Input("btn-close-poi-form", "n_clicks"),
    State("memory_store", "data"),
    prevent_initial_call=True,
)
def show_or_hide_poi_card(click_data: Dict, close_clicks, data: Dict):
    if close_clicks:
        prev_clicks = data.get("card_closes", 0)
        data["card_closes"] = close_clicks
        if close_clicks > prev_clicks:
            return poi_cards.hidden_card()
    if not click_data:
        return poi_cards.hidden_card()
    points: List[Dict] = click_data.get("points")
    if not points:
        return poi_cards.hidden_card()
    point = points[0]
    point_data = point.get("customdata")
    if point_data:
        return poi_cards.display_poi_card(point_data)
    if ("x" in point) and ("y" in point):
        return poi_cards.new_poi_card(point["x"], point["y"], data["map_id"])
    return poi_cards.hidden_card()


@app.callback(
    Output("upload-thumbnail-poi-form", "children"),
    Input("upload-thumbnail-poi-form", "contents"),
    State("upload-thumbnail-poi-form", "filename"),
    prevent_initial_call=True,
)
def update_poi_thumbnail_upload(contents, name):
    if contents is not None:
        return html.Div(
            [
                html.A(
                    [
                        dcc.Markdown(
                            f"""
                        _Thumbnail:_ {name}
                    """
                        ),
                    ]
                )
            ]
        )
    return no_update


@app.callback(
    Output("store-poi-form", "data"),
    Input("point-poi-form", "children"),
    Input("name-input-poi-form", "value"),
    Input("description-markdown-poi-form", "value"),
    Input("upload-thumbnail-poi-form", "contents"),
    Input("map-dropdown-poi-form", "value"),
    State("upload-thumbnail-poi-form", "filename"),
    prevent_initial_call=True,
)
def update_poi_form(
    point, name, description, thumbnail_data, poi_map, thumbnail_filename
):
    pattern = r"\[(\d+),(\d+)]"
    result = re.search(pattern, point)
    x, y = int(result.group(1)), int(result.group(2))
    return {
        "x": x,
        "y": y,
        "name": name,
        "description": description,
        "poi_map": poi_map,
        "thumbnail_data": thumbnail_data,
        "thumbnail_filename": thumbnail_filename,
    }


@app.callback(
    Output("store-add-poi-form", "data"),
    Input("dropdown-add-poi-form", "value"),
    Input("point-add-poi-form", "children"),
    State("memory_store", "data"),
    prevent_initial_call=False,
)
def update_add_poi_form(poi_pk, point, data):
    pattern = r"\[(\d+),(\d+)]"
    result = re.search(pattern, point)
    x, y = int(result.group(1)), int(result.group(2))
    return {"x": x, "y": y, "poi_id": poi_pk, "map_id": data["map_id"]}


@app.callback(
    Output("preview-div-add-poi-form", "children"),
    Input("store-add-poi-form", "data"),
    prevent_initial_call=False,
)
def update_add_poi_preview(data):
    if not (poi_id := data.get("poi_id", None)):
        return no_update
    poi = PointOfInterest.objects.get(pk=poi_id)
    return poi_cards.add_poi_preview(poi) if poi else no_update


@app.callback(
    Output("debug-data", "children"),
    Input("button-add-poi-form", "n_clicks"),
    State("store-add-poi-form", "data"),
    prevent_initial_call=True,
)
def on_button_poi_add(clicks, data):
    if not clicks:
        return no_update
    curr_map = Map.objects.get(pk=data["map_id"])
    poi = PointOfInterest.objects.get(pk=data["poi_id"])
    poi.parent_maps.add(curr_map, through_defaults={"x": data["x"], "y": data["y"]})
    poi.full_clean()
    poi.save()
    return "Return adding POI"
