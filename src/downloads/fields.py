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


class FileQuota(object):

    def __init__(self, max_usage=-1):
        self.current_usage = 0
        self.max_usage = max_usage

    def update(self, items, attr_name):
        self.current_usage = 0
        for item in items:
            the_file = getattr(item, attr_name, None)
            if the_file:
                try:
                    self.current_usage += the_file.size
                except AttributeError:
                    pass  # Protect against the inconsistence of that the file
                    # has been deleted in storage but still is in the field

    def exceeds(self, size=0):
        if self.max_usage >= 0:
            return (self.current_usage + size > self.max_usage)
        else:
            return False

    def near_limit(self, limit_threshold=0.8):
        return (float(self.current_usage) / float(self.max_usage)) > limit_threshold


class QuotaValidator(object):

    def __init__(self, max_usage):
        self.quota = FileQuota(max_usage)

    def update_quota(self, items, attr_name):
        self.quota.update(items, attr_name)

    def __call__(self, file):
        file_size = file.size
        if self.quota.exceeds(file_size):
            raise forms.ValidationError(
                _('Please keep the total uploaded files under %(total_size)s. With this file, the total would be %(exceed_size)s.' %
                  {'total_size': filesizeformat(self.quota.max_usage), 'exceed_size': filesizeformat(self.quota.current_usage + file_size)})
            )
