from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from .views import *

app_name = 'downloads'


urlpatterns = [
    url(r'^$', DownloadListView.as_view(), name='index'),
]
