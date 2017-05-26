import os

from django.test import TestCase

from mixer.backend.django import mixer

from .models import TestModel, ModelTestCase
from .utils import get_fake_pdf_file
from ..fields import ValidatedFileField


class ModelWithFile(TestModel):

    """
    Temporary model to test `ValidatedFileField`.
    """

    file = ValidatedFileField(
        upload_to='downloads',
        content_types=['application/pdf'],
        max_upload_size=1048576,    # 1 Mb: 1024 * 1024
        blank=True,
        null=True,
    )

    small_file = ValidatedFileField(
        upload_to='downloads',
        content_types=['application/pdf'],
        max_upload_size=100,    # 100 bytes
        blank=True,
        null=True,
    )

    text_file = ValidatedFileField(
        upload_to='downloads',
        content_types=['text/plain'],
        max_upload_size=100,    # 100 bytes
        )


class TestValidatedFileField(ModelTestCase):

    temporary_models = (ModelWithFile,)

    def setUp(self):
        self.file = get_fake_pdf_file()

    def test_model_has_file(self):
        obj = mixer.blend(ModelWithFile, file=self.file)
        os.remove(obj.file.path)
        assert obj.file is not None, 'Should save the file'
        assert obj.file.name.endswith(self.file.name), 'Should have the filename'

    def test_max_size(self):
        obj = mixer.blend(ModelWithFile, small_file=self.file)
        os.remove(obj.small_file.path)
