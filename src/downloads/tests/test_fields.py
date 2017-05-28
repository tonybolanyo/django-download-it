from io import StringIO
import os

from django.conf import settings
from django.test import TestCase

from django.core.files.uploadedfile import InMemoryUploadedFile

from mixer.backend.django import mixer

from .forms import TestModelForm
from .models import ModelTestCase, TestModelFile
from .utils import get_fake_pdf_file
from ..fields import ValidatedFileField


class ValidatedFileFieldTest(ModelTestCase):

    def test_create_empty_instance(self):
        """Can create model instance"""

        instance = TestModelFile.objects.create()

    def test_create_instance_with_file(self):
        """Can create model instance with file and access file URL"""

        instance = TestModelFile.objects.create(file=get_fake_pdf_file('foo'))

        self._check_file_url(instance.file, 'foo')

        instance.file.delete()
        instance.delete()

    def test_form_ok(self):

        io = StringIO()
        io.write('%PDF-1.5')
        pdf_file = InMemoryUploadedFile(
            file=io, field_name=None, name='foo.pdf',
            content_type='application/pdf', size=2300, charset=None,
            content_type_extra='application/pdf')
        pdf_file.seek(0)
        form = TestModelForm(data={}, files={'file': pdf_file})

        self.assertTrue(form.is_valid())
        instance = form.save()

        self._check_file_url(instance.the_file, 'the_file.png')

        instance.the_file.delete()
        instance.delete()

    def _check_file_url(self, filefield, filename):
        """
        Helper function to check URL of a FileField file.
        """

        url = os.path.join(settings.MEDIA_URL,
                           filefield.field.upload_to, filename)
        self.assertEqual(filefield.url, url)
