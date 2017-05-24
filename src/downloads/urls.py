from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from .views import *

app_name = 'downloads'


urlpatterns = [
    url(r'^$', DownloadListView.as_view(), name='index'),
    url(r'^download/(?P<pk>\d+)/$', FileDownloadView.as_view(), name='download'),
]
