"""
See https://github.com/kaleidos/django-validated-file for original file
"""

import sys

from django.conf import settings
from django.db import models
from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext as _

import magic


class ValidatedFileField(models.FileField):

    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types", [])
        self.max_upload_size = kwargs.pop("max_upload_size", 0)
        self.mime_lookup_length = kwargs.pop("mime_lookup_length", 4096)
        super(ValidatedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ValidatedFileField, self).clean(*args, **kwargs)
        file = data.file

        if self.content_types:
            uploaded_content_type = getattr(file, 'content_type', '')

            if sys.platform in ('win32', 'cygwin'):
                mg = magic.Magic(
                    mime=True, magic_file=settings.MAGIC_FILE)
            else:
                mg = magic.Magic(mime=True)
            content_type_magic = mg.from_buffer(
                file.read(self.mime_lookup_length)
            )
            file.seek(0)

            # Prefere mime-type instead mime-type from http header
            if uploaded_content_type != content_type_magic:
                uploaded_content_type = content_type_magic

            if not uploaded_content_type in self.content_types:
                raise forms.ValidationError(
                    _('Files of type %(type)s are not supported.') % {
                        'type': content_type_magic}
                )

        if self.max_upload_size and hasattr(file, '_size'):
            if file._size > self.max_upload_size:
                raise forms.ValidationError(
                    _('Files of size greater than %(max_size)s are not allowed. Your file is %(current_size)s') %
                    {'max_size': filesizeformat(
                        self.max_upload_size),
                     'current_size': filesizeformat(file._size)}
                )

        return data
