from typing import Dict
from worldbuilder.dash.constants import logger


from django.conf import settings


import base64
import os


def daq_rgb_to_dash(c: str):
    return f'rgb({c["r"]},{c["g"]},{c["b"]},{c["a"]})'


def try_write_thumbnail_from_form(poi_form: Dict):
    if not (thumbnail_data := poi_form["thumbnail_data"]):
        return None
    try:
        thumbnail_data = thumbnail_data.encode("utf8").split(b";base64,")[1]
        thumbnail_filename = poi_form["thumbnail_filename"]
        thumbnail_path = os.path.join("thumbnails", thumbnail_filename)
        thumbnail_fullpath = os.path.join(settings.MEDIA_ROOT, thumbnail_path)
        with open(thumbnail_fullpath, "wb") as fp:
            fp.write(base64.decodebytes(thumbnail_data))
    except Exception as e:
        logger.warning(e, exc_info=True)
        return None
    return thumbnail_path
