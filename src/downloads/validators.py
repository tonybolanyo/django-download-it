import logging

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.translation import ugettext as _

import magic

logger = logging.getLogger(__name__)

try:
    MAGIC_FILE = settings.MAGIC_FILE
except:
    MAGIC_FILE = None


def validate_file_extension(value):

    content_types = settings.DOWNLOADS_ALLOWED_CONTENT_TYPES

    mime_lookup_length = 4096   # 4Kb by default

    if value.file.__class__ == InMemoryUploadedFile:
        buffer = value.file.file.getvalue()
        # as the file is already in memory, buffer length
        # should not exhaust the system
    else:
        buffer = value.file.file.read(mime_lookup_length)
        # but here this may become an issue

    logger.debug('Magic file: %s' % MAGIC_FILE)

    file_magic = magic.Magic(mime=True, magic_file=MAGIC_FILE)
    mime = file_magic.from_buffer(buffer)
    logger.debug('Detected MIME: %s' % mime)

    content_type = value.file.content_type

    # Prefere mime-type instead mime-type from http header
    if content_type != mime:
        content_type = mime

    if content_type not in content_types:
        raise ValidationError(
            _('Files of type %(type)s are not supported.') % {
                'type': content_type}
        )
