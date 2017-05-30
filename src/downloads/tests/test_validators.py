import os
from io import StringIO

from django.conf import settings
from django.core.files.uploadedfile import (
    InMemoryUploadedFile, SimpleUploadedFile)
from django.db import models
from django.test import TestCase

from mixer.backend.django import mixer

from ..validators import FileMimeValidator, FileSizeValidator

from .forms import ModelFormTest, MultipleMimeFormTest, ModelFormSizeTest
from .models import (
    ModelTest, ModelTestFile, ModelTestMultipleMime, ModelTestCase)
from .utils import get_fake_pdf_file


def get_file(filename='sample.pdf'):
    filename = os.path.join(settings.BASE_DIR, 'downloads',
                            'tests', 'sample_files', filename)
    with open(filename, 'rb') as file:
        file = SimpleUploadedFile(file.name, file.read())
    return file


class TestFileMimeValidator(ModelTestCase):

    temporary_models = (ModelTestFile,)

    def setUp(self):
        self.file = get_fake_pdf_file()

    def test_allowed_types_equality(self):
        self.assertEqual(
            FileMimeValidator(),
            FileMimeValidator()
        )

        self.assertEqual(
            FileMimeValidator(['application/pdf']),
            FileMimeValidator(['application/pdf'])
        )

        self.assertEqual(
            FileMimeValidator(['application/pdf', 'image/png']),
            FileMimeValidator(['application/pdf', 'image/png'])
        )

        self.assertNotEqual(
            FileMimeValidator(['application/pdf']),
            FileMimeValidator(['application/pdf', 'image/png'])
        )

    def test_valid_file(self):
        """Real upload file with right http-headers"""
        file = get_file('sample.pdf')
        form = ModelFormTest(data={}, files={'file': file})
        self.assertTrue(form.is_valid())

    def test_valid_multiple_mime(self):
        """Real upload file with right http-headers"""
        file = get_file('sample.pdf')
        form = MultipleMimeFormTest(data={}, files={'file': file})
        self.assertTrue(form.is_valid())

        file = get_file('sample.odt')
        form = MultipleMimeFormTest(data={}, files={'file': file})
        self.assertTrue(form.is_valid())

    def test_invalid_file(self):
        """Not accepted MIME type"""
        file = get_file('sample.odt')
        form = ModelFormTest(data={}, files={'file': file})
        self.assertFalse(form.is_valid())

    def test_valid_file_bad_extension(self):
        """Should accept real MIME, not http header MIME"""
        file = get_file('not_pdf.pdf')
        form = ModelFormTest(data={}, files={'file': file})
        self.assertFalse(form.is_valid())


class TestFileSizeValidator(ModelTestCase):

    def test_size_equality(self):

        self.assertEqual(
            FileSizeValidator(),
            FileSizeValidator()
        )

        self.assertEqual(
            FileSizeValidator(max_size=500),
            FileSizeValidator(max_size=500)
        )

        self.assertNotEqual(
            FileSizeValidator(max_size=500),
            FileSizeValidator(max_size=1000)
        )

    def test_valid_size(self):
        """Accept file size < max_size"""
        file = get_file('sample.pdf')
        form = ModelFormSizeTest(data={}, files={'file': file})
        self.assertTrue(form.is_valid())

    def test_invalid_size(self):
        """Reject file size > max_size"""
        file = get_file('big_file.pdf')
        form = ModelFormSizeTest(data={}, files={'file': file})
        self.assertFalse(form.is_valid())
