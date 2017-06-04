import logging

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.template.defaultfilters import filesizeformat
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _


import magic

from .utils import FileSize


logger = logging.getLogger(__name__)


MAGIC_FILE = None if not hasattr(
    settings, 'MAGIC_FILE') else settings.MAGIC_FILE

ALLOWED_TYPES = ['application/pdf'] if not hasattr(
    settings, 'DOWNLOADS_ALLOWED_CONTENT_TYPES'
) else settings.DOWNLOADS_ALLOWED_CONTENT_TYPES

MAX_FILE_SIZE = FileSize('5MB').get_bytes() if not hasattr(
    settings, 'DOWNLOADS_MAX_FILE_SIZE') else settings.DOWNLOADS_MAX_FILE_SIZE


@deconstructible
class FileMimeValidator(object):

    """
    Uses magic to validate file mime type in any FileField model field.
    """

    mime_lookup_length = 4096   # 4Kb by default

    def __init__(self, allowed_types=ALLOWED_TYPES):
        self.allowed_types = allowed_types

    def __call__(self, value):

        buffer = value.file.file.read(self.mime_lookup_length)

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


@deconstructible
class FileSizeValidator:
    """
    Allows validate size in a `FileField`.
    """

    def __init__(self, max_size=MAX_FILE_SIZE):
        self.max_size = max_size

    def __eq__(self, other):
        return self.max_size == other.max_size

    def __call__(self, value):
        if value.size > self.max_size:
            raise ValidationError(
                _('Files of size greater than %(max_size)s are not allowed. Your file is %(current_size)s') %
                {'max_size': filesizeformat(
                    self.max_size),
                 'current_size': filesizeformat(value.size)}
            )
