import os

from django.db import models
from django.test import TestCase

from mixer.backend.django import mixer

from ..validators import FileMimeValidator

from .models import ModelTest, ModelTestCase
from .utils import get_fake_pdf_file


class ModelFile(ModelTest):

    """
    Temporary model to test `ValidatedFileField`.
    """

    file = models.FileField(
        upload_to='testfile',
        blank=True,
        null=True,
        validators=[FileMimeValidator()],
    )


class TestFileMimeValidator(ModelTestCase):

    temporary_models = (ModelFile,)

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

    # def test_valid_file(self):
    #     obj = mixer.blend(ModelFile, file=self.file)
    #     validator = FileMimeValidator(['application/pdf'])
    #     self.assertEqual(validator(obj.file), 'application/pdf')
    #     os.remove(obj.file.path)
