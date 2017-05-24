
from django.test import TestCase

from mixer.backend.django import mixer
import pytest

from ..models import Download
from ..fields import ContentTypeRestrictedFileField

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestDownload(TestCase):

    def test_model(self):
        obj = mixer.blend(Download)
        assert obj.pk == 1, 'Should create a Download instance'
        assert obj.title in str(obj), 'Should have title on string representation'
