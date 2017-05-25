from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from mixer.backend.django import mixer

from ..models import Download
from ..views import DownloadListView

APP_NAME = 'downloads'


class DownloadListViewTest(TestCase):

    url = APP_NAME + ':index'

    def test_url(self):
        client = Client()
        response = client.get(reverse(self.url))
        self.assertEqual(response.status_code, 200)

    def test_use_template(self):
        client = Client()
        response = client.get(reverse(self.url))
        self.assertEqual(response.template_name[0], APP_NAME + '/download_list.html')

    def test_list_empty(self):
        client = Client()
        response = client.get(reverse(self.url))
        items = response.context_data['downloads']
        self.assertEqual(items.count(), 0)

    def test_only_show_published_items(self):
        mixer.blend(Download, status=Download.STATUS.published)
        mixer.blend(Download, status=Download.STATUS.hidden)
        mixer.blend(Download, status=Download.STATUS.draft)

        client = Client()
        response = client.get(reverse(self.url))
        items = response.context_data['downloads']
        self.assertEqual(items.count(), 1)
