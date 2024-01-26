import json
import logging

from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response

import worldbuilder.models as models
from worldbuilder.models.map import Map
from worldbuilder.dash.map import set_figure_map
from worldbuilder.request_form import RequestForm

logger = logging.getLogger('__name__')


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

def dash_map(request: HttpRequest):
    map_id = request.GET.get('id', default=None)
    width = request.session.get('width')
    height = request.session.get('height')
    ratio = height / width if width and height else 0.5
    map = set_figure_map(request, map_id)
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

@api_view(['GET'])
@permission_classes([])
def list_npcs(_: HttpRequest):
    data = serializers.serialize('json', models.Npc.objects.all().order_by('name'))
    return HttpResponse(data, content_type='application/json')

@api_view(['GET'])
@permission_classes([])
def list_factions(_: HttpRequest):
    data = serializers.serialize('json', models.Faction.objects.all().order_by('name'))
    return HttpResponse(data, content_type='application/json')

@api_view(['GET'])
@permission_classes([])
def list_maps(_: HttpRequest):
    data = serializers.serialize('json', models.Map.objects.all().order_by('name'))
    return HttpResponse(data, content_type='application/json')

@api_view(['GET'])
@permission_classes([])
def list_points_of_interest(_: HttpRequest):
    data = serializers.serialize('json', models.PointOfInterest.objects.all().order_by('name'))
    return HttpResponse(data, content_type='application/json')

@api_view(['GET'])
@permission_classes([])
def list_quests(_: HttpRequest):
    data = serializers.serialize('json', models.Quest.objects.all().order_by('name'))
    return HttpResponse(data, content_type='application/json')

@api_view(['GET'])
@permission_classes([])
def lists(_: HttpRequest):
    return HttpResponse(
        json.dumps(['npc', 'faction', 'map', 'point_of_interest', 'quest']),
        content_type='application/json'
    )

def maps(request):
    maps = Map.objects.all()
    context = {'maps': maps}
    return render(request, 'maps.html', context)
