import logging
from typing import Dict, List

import plotly.express as px
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django_plotly_dash import DjangoDash
from dash import dcc
from dash import html
from plotly.offline import plot
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from skimage import io


from worldbuilder.models import Map
from worldbuilder.request_form import RequestForm

logger = logging.getLogger('__name__')
app = DjangoDash("WorldBuilder")


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
        sliders = map_sliders(map.image.width, map.image.height)
    )
    img_plot = plot(fig, output_type="div")
    context = {'plot_div': img_plot}
    return render(request, 'map.html', context)

def dash_map(request: HttpRequest):
    id = request.GET.get('id', default=None)
    width = request.session.get('width')
    height = request.session.get('height')
    ratio = height / width if width and height else 0.5
    try:
        map = Map.objects.get(pk=id)
    except Exception:
        map = Map.objects.last()

    url = request.build_absolute_uri(map.image.url)
    img = io.imread(url)

    fig = px.imshow(img)
    fig.update_layout(
        # height=1000
        # autosize=True,
        # sliders = map_sliders(map.image.width, map.image.height)
    )
    app.layout = html.Div([
        dcc.Graph(
            id='map-graph',
            figure=fig,
            config={
                'displayModeBar': True, 
                'responsive': True
            },
            style={'height': '100vh'}  # Set the height to 100% of the viewport height
        ),
    ])
    image_ratio = map.image.height / map.image.width
    context = {
        'height_ratio': min(image_ratio, ratio)
    }
    return render(request, 'dash_map.html', context)

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
