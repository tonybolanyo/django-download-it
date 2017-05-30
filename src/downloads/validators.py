import logging

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _


import magic

logger = logging.getLogger(__name__)


MAGIC_FILE = None if not hasattr(
    settings, 'MAGIC_FILE') else settings.MAGIC_FILE

ALLOWED_TYPES = ['application/pdf'] if not hasattr(
    settings, 'DOWNLOADS_ALLOWED_CONTENT_TYPES'
) else settings.DOWNLOADS_ALLOWED_CONTENT_TYPES


@deconstructible
class FileMimeValidator(object):

    """
    Uses magic to validate file mime type in any FileField model field.
    """

    mime_lookup_length = 4096   # 4Kb by default

    def __init__(self, allowed_types=ALLOWED_TYPES):
        self.allowed_types = allowed_types

    def __call__(self, value):

        if value.file.__class__ == InMemoryUploadedFile:
            buffer = value.file.file.getvalue()
            # as the file is already in memory, buffer length
            # should not exhaust the system
        else:
            buffer = value.file.file.read(self.mime_lookup_length)
            # but here this may become an issue

        logger.debug('Magic file: %s' % MAGIC_FILE)

        file_magic = magic.Magic(mime=True, magic_file=MAGIC_FILE)
        mime = file_magic.from_buffer(buffer)
        logger.debug('Detected MIME: %s' % mime)

        content_type = value.file.content_type

        # Prefere mime-type instead mime-type from http header
        if content_type != mime:
            content_type = mime

        if content_type not in self.allowed_types:
            raise ValidationError(
                _('Files of type %(type)s are not supported.') % {
                    'type': content_type}
            )

    def __eq__(self, other):

        return self.allowed_types == other.allowed_types
