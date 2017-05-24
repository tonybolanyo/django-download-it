import logging
import magic

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, View
from django.views.generic.detail import SingleObjectMixin

from .models import Download

logger = logging.getLogger(__name__)


class DownloadListView(ListView):

    model = Download
    context_object_name = 'downloads'
    queryset = Download.published.all()


class FileDownloadView(SingleObjectMixin, View):

    model = Download

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        logger.debug(obj.file)
        mime = magic.from_file(obj.file.path, mime=True)
        print(mime)
        response = HttpResponse(obj.file, content_type=mime)
        response['Content-Disposition'] = 'attachment; filename="%s"' % obj.file.name
        return response