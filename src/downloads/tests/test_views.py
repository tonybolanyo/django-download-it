import os
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from mixer.backend.django import mixer

from ..models import Download
from ..views import DownloadListView

APP_NAME = 'downloads'
User = get_user_model()


def get_fake_pdf_file(filename='foo.pdf'):
    """
    Creafe a fake PDF file for tests.
    Use StringIO writing `%PDF-1.5` at the begining of file,
    so `magic` get the mime as `application/pdf`.
    """

    io = StringIO()
    io.write('%PDF-1.5')
    pdf_file = InMemoryUploadedFile(
        file=io, field_name=None, name=filename,
        content_type='application/pdf', size=2300, charset=None,
        content_type_extra='application/pdf')
    pdf_file.seek(0)
    return pdf_file


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
        pub = mixer.blend(Download, status=Download.STATUS.published)
        hide = mixer.blend(Download, status=Download.STATUS.hidden)
        draft = mixer.blend(Download, status=Download.STATUS.draft)

        client = Client()
        response = client.get(reverse(self.url))
        items = response.context_data['downloads']
        self.assertEqual(items.count(), 1)
        os.remove(pub.thumbnail.path)
        os.remove(draft.thumbnail.path)
        os.remove(hide.thumbnail.path)
        os.remove(hide.file.path)
        os.remove(draft.file.path)
        os.remove(pub.file.path)


class TestFileDownloadView(TestCase):

    url = APP_NAME + ':download'

    def setUp(self):
        self.obj = mixer.blend(Download, status=Download.STATUS.published)

    def tearDown(self):
        os.remove(self.obj.file.path)
        os.remove(self.obj.thumbnail.path)

    def test_url(self):
        client = Client()
        response = client.get(reverse(self.url, kwargs={'pk': self.obj.pk}))
        self.assertEqual(response.status_code, 200)

    def test_content_disposition(self):
        client = Client()
        response = client.get(reverse(self.url, kwargs={'pk': self.obj.pk}))
        self.assertIn('attachment', response['Content-Disposition'])

    def test_filename(self):
        client = Client()
        response = client.get(reverse(self.url, kwargs={'pk': self.obj.pk}))
        self.assertIn(self.obj.file.name, response['Content-Disposition'])

    def test_content_type(self):
        file = get_fake_pdf_file()
        os.remove(self.obj.file.path)
        self.obj.file = file
        self.obj.save()
        client = Client()
        response = client.get(reverse(self.url, kwargs={'pk': self.obj.pk}))
        self.assertIn('application/pdf', response['Content-Type'])


class TestDownloadDetailView(TestCase):

    url = APP_NAME + ':detail'

    def setUp(self):
        self.obj = mixer.blend(Download, status=Download.STATUS.published)

    def tearDown(self):
        os.remove(self.obj.file.path)
        os.remove(self.obj.thumbnail.path)

    def test_url(self):
        client = Client()
        response = client.get(reverse(self.url, kwargs={'pk': self.obj.pk}))
        self.assertEqual(response.status_code, 200)

    def test_use_template(self):
        client = Client()
        response = client.get(reverse(self.url, kwargs={'pk': self.obj.pk}))
        self.assertEqual(
            response.template_name[0], APP_NAME + '/download_detail.html')

    def test_not_show_draft_items_for_no_staff_user(self):
        self.obj.status = Download.STATUS.draft
        self.obj.save()
        user = mixer.blend(User, is_staff=False)

        # Anonymous user
        client = Client()
        response = client.get(reverse(self.url, kwargs={'pk': self.obj.pk}))
        self.assertEqual(response.status_code, 404)

        # Logged user, no staff
        client.force_login(user)
        response = client.get(reverse(self.url, kwargs={'pk': self.obj.pk}))
        self.assertEqual(response.status_code, 404)

    def test_not_show_hidden_items_for_no_staff_user(self):
        self.obj.status = Download.STATUS.hidden
        self.obj.save()
        user = mixer.blend(User, is_staff=False)

        # Anonymous user
        client = Client()
        response = client.get(reverse(self.url, kwargs={'pk': self.obj.pk}))
        self.assertEqual(response.status_code, 404)

        # Logged user, no staff
        client.force_login(user)
        response = client.get(reverse(self.url, kwargs={'pk': self.obj.pk}))
        self.assertEqual(response.status_code, 404)

    def test_show_hidden_items_to_staff(self):
        self.obj.status = Download.STATUS.hidden
        self.obj.save()
        user = mixer.blend(User, is_staff=True)
        client = Client()
        client.force_login(user)
        response = client.get(reverse(self.url, kwargs={'pk': self.obj.pk}))
        self.assertEqual(response.status_code, 200)

    def test_show_draft_items_to_staff(self):
        self.obj.status = Download.STATUS.draft
        self.obj.save()
        user = mixer.blend(User, is_staff=True)
        client = Client()
        client.force_login(user)
        response = client.get(reverse(self.url, kwargs={'pk': self.obj.pk}))
        self.assertEqual(response.status_code, 200)
