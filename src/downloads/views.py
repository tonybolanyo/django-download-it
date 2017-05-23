from django.shortcuts import render
from django.views.generic import ListView

from .models import Download


class DownloadListView(ListView):

    model = Download
    context_object_name = 'downloads'
    queryset = Download.published.all()