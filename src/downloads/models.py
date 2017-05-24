import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices
from model_utils.models import StatusModel, TimeStampedModel

from .fields import ContentTypeRestrictedFileField
from .utils import FileSize

logger = logging.getLogger(__name__)


class Download(StatusModel, TimeStampedModel):

    STATUS = Choices(
        ('draft', _('draft')),
        ('published', _('published')),
        ('hidden', _('hidden')),
    )

    title = models.CharField(_('title'), max_length=250)
    slug = models.SlugField(_('slug'), unique=True)
    summary = models.TextField(_('summary'), blank=True)
    description = models.TextField(_('description'), blank=True)
    file = ContentTypeRestrictedFileField(
        _('file'),
        upload_to='downloads',
        content_types=['application/pdf', 'application/zip'],
        max_upload_size=FileSize('5MB').get_bytes(),
        help_text=_('Only PDF and ZIP files.')
    )
    thumbnail = models.ImageField(_('thumbnail'), upload_to='downloads')
    downloads = models.IntegerField(_('download counter'), default=0)
    registered_only = models.BooleanField(
        _('only for registered users'), default=True)

    class Meta:
        verbose_name = _('download')
        verbose_name_plural = _('downloads')
        ordering = ('title',)

    def __str__(self):
        return self.title
