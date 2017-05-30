from django.conf import settings
from django.db import models
from django.test import TestCase

from mixer.backend.django import mixer

from .models import TestModelFile, ModelTestCase
from .utils import get_fake_pdf_file
from ..validators import FileMimeValidator


class TestMimeValidator(ModelTestCase):

    temporary_models = (TestModelFile,)

    # def test_file_mime_accepted(self):
    #     with self.settings(
    #             DOWNLOADS_ALLOWED_CONTENT_TYPES=['application/pdf']):
    #         from ..validators import FileMimeValidator
    #         file = get_fake_pdf_file()
    #         validator = FileMimeValidator()
    #         self.assertTrue(validate_file_extension(file))

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

    def test_allowed_extension(self):
        validator = FileMimeValidator(['application/pdf'])
        file = get_fake_pdf_file()
        model = mixer.blend(TestModelFile, file=file)
        self.assertEqual(validator(model.file), 'application/pdf')
