import os
from io import StringIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.test import TestCase

from mixer.backend.django import mixer

from ..validators import FileMimeValidator

from .forms import ModelFormTest
from .models import ModelTest, ModelTestFile, ModelTestCase
from .utils import get_fake_pdf_file


def get_fake_file(filename='foo.pdf', mime_type='application/pdf'):
    """
    Creafe a fake file for tests.
    """

    io = StringIO()
    io.write(' lajsdfh lasjdfh alsjdfh alsjdfh ')
    file = InMemoryUploadedFile(
        file=io, field_name=None, name=filename,
        content_type=mime_type, size=2300, charset=None)
    file.seek(0)
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

    def test_invalid_file(self):
        form = ModelFormTest(data={}, files={'file':get_fake_file()})
        self.assertFalse(form.is_valid())
