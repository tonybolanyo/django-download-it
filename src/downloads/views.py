import logging
import magic
import sys

from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView, View
from django.views.generic.detail import SingleObjectMixin

from .models import Download

logger = logging.getLogger(__name__)

MAGIC_FILE = None if not hasattr(
    settings, 'MAGIC_FILE') else settings.MAGIC_FILE


class DownloadListView(ListView):

    model = Download
    context_object_name = 'downloads'
    queryset = Download.published.all()


class FileDownloadView(SingleObjectMixin, View):

    model = Download

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        logger.debug('Downloading %s' % obj.file)
        obj.downloads = obj.downloads + 1
        obj.save()
        file_magic = magic.Magic(mime=True, magic_file=MAGIC_FILE)
        mime = file_magic.from_file(obj.file.path)
        response = HttpResponse(obj.file, content_type=mime)
        response['Content-Disposition'] = 'attachment; filename="%s"' % obj.file.name
        return response


class DownloadDetailView(DetailView):

    model = Download
    context_object_name = 'file'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        is_staff = self.request.user.is_staff
        if obj.status != Download.STATUS.published and not is_staff:
            raise Http404
        return obj

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        obj = self.get_object()
        file_magic = magic.Magic(mime=True, magic_file=MAGIC_FILE)
        context['mime'] = file_magic.from_file(obj.file.path)
        return context
