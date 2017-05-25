from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from mixer.backend.django import mixer

from ..models import Download
from ..views import DownloadListView

APP_NAME = 'downloads'
User = get_user_model()


class TestDownloadListView(TestCase):

    url = APP_NAME + ':index'

    def test_url(self):
        client = Client()
        response = client.get(reverse(self.url))
        self.assertEqual(response.status_code, 200)

    def test_use_template(self):
        client = Client()
        response = client.get(reverse(self.url))
        self.assertEqual(response.template_name[
                         0], APP_NAME + '/download_list.html')

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


class TestDownloadDetailView(TestCase):

    url = APP_NAME + ':detail'

    def test_url(self):
        obj = mixer.blend(Download, status=Download.STATUS.published)
        client = Client()
        response = client.get(reverse(self.url, kwargs={'pk': obj.pk}))
        self.assertEqual(response.status_code, 200)

    def test_use_template(self):
        obj = mixer.blend(Download, status=Download.STATUS.published)
        client = Client()
        response = client.get(reverse(self.url, kwargs={'pk': obj.pk}))
        self.assertEqual(
            response.template_name[0], APP_NAME + '/download_detail.html')

    def test_not_show_draft_items_for_no_staff_user(self):
        obj = mixer.blend(Download, status=Download.STATUS.draft)
        user = mixer.blend(User, is_staff=False)

        # Anonymous user
        client = Client()
        response = client.get(reverse(self.url, kwargs={'pk': obj.pk}))
        self.assertEqual(response.status_code, 404)

        # Logged user, no staff
        client.force_login(user)
        response = client.get(reverse(self.url, kwargs={'pk': obj.pk}))
        self.assertEqual(response.status_code, 404)

    def test_not_show_hidden_items_for_no_staff_user(self):
        obj = mixer.blend(Download, status=Download.STATUS.hidden)
        user = mixer.blend(User, is_staff=False)

        # Anonymous user
        client = Client()
        response = client.get(reverse(self.url, kwargs={'pk': obj.pk}))
        self.assertEqual(response.status_code, 404)

        # Logged user, no staff
        client.force_login(user)
        response = client.get(reverse(self.url, kwargs={'pk': obj.pk}))
        self.assertEqual(response.status_code, 404)

    def test_show_hidden_items_to_staff(self):
        obj = mixer.blend(Download, status=Download.STATUS.hidden)
        user = mixer.blend(User, is_staff=True)
        client = Client()
        client.force_login(user)
        response = client.get(reverse(self.url, kwargs={'pk': obj.pk}))
        self.assertEqual(response.status_code, 200)

    def test_show_draft_items_to_staff(self):
        obj = mixer.blend(Download, status=Download.STATUS.draft)
        user = mixer.blend(User, is_staff=True)
        client = Client()
        client.force_login(user)
        response = client.get(reverse(self.url, kwargs={'pk': obj.pk}))
        self.assertEqual(response.status_code, 200)
