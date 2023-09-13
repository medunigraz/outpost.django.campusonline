import logging
from pathlib import Path

from django.core.cache import cache
from django.http import (
    FileResponse,
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseForbidden,
)
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import View
from rest_framework import permissions
from rest_framework.views import APIView
from wand.exceptions import WandException
from wand.image import Image

from . import (
    models,
    tasks,
)
from .conf import settings

logger = logging.getLogger(__name__)


@method_decorator(cache_page(3600), name="dispatch")
class PrivateAvatarView(View):
    def get(self, request, hash):
        p = get_object_or_404(models.Person, hash=hash)
        try:
            with Image(blob=p.avatar_private.tobytes()) as img:
                response = HttpResponse()
                img.format = "jpeg"
                img.save(file=response)
                response["Content-Type"] = img.mimetype
                response["Cache-Control"] = "private,max-age=604800"
                return response
        except WandException as e:
            logger.warn(f"Failed to load image blob: {e}")
        return HttpResponseNotFound()


class XMLView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        if not request.user.has_perm("global_permissions.linz"):
            return HttpResponseForbidden()
        response = HttpResponse()
        response["Content-Type"] = "application/xml"
        xml = cache.get(settings.CAMPUSONLINE_XML_CACHE_KEY, None)
        if not xml:
            xml = tasks.XMLTasks().hydrate()
        response.write(xml)
        return response


class SchemaView(View):
    def get(self, request):
        schema = Path(__file__).parent.joinpath("schema", "linz.xsd")
        response = FileResponse(schema.open("rb"))
        response["Content-Type"] = "application/xml"
        response["Cache-Control"] = "public,max-age=604800"
        return response
