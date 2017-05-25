import os

from django.test import TestCase

from mixer.backend.django import mixer
import pytest

from ..models import Download


class TestDownload(TestCase):

    def test_model(self):
        obj = mixer.blend(Download)
        assert obj.pk == 1, 'Should create a Download instance'
        assert obj.title in str(obj), 'Should have title on string representation'
        os.remove(obj.file.path)
        os.remove(obj.thumbnail.path)
