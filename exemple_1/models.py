from django.db import models
import uuid
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from easy_thumbnails.fields import ThumbnailerImageField

from .. import utils


class Token(models.Model):
    PLATFORM_CHOICE = (
        ('windows', "windows"),
        ('ios', "ios"),
        ('android', "android"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICE)
    user_agent = models.CharField(max_length=512)


class Account(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        related_name='account'
    )

    first_name = models.CharField(_("first name"), max_length=512, default='')

    last_name = models.CharField(_("last name"), max_length=512, default='')

    middle_name = models.CharField(
        _("middle name"),
        max_length=512,
        blank=True,
        default=''
    )

    notes = models.CharField(
        _("extra info"),
        max_length=1024,
        null=True,
        blank=True,
        default=''
    )

    birthday = models.DateField(_("birthday"), null=True, blank=True)

    legal_person = models.BooleanField(_("legal person"), default=False)

    logo = ThumbnailerImageField(
        _("picture"),
        default=None,
        upload_to=utils.upload_logo,
        blank=True,
        null=True
    )

    class Meta(object):
        verbose_name = _("account")
        verbose_name_plural = _("accounts")

    def __str__(self):
        return '{first_name} {last_name} {middle_name}'.format(
            first_name=self.first_name,
            last_name=self.last_name,
            middle_name=self.middle_name
        ).strip()

    def get_full_name(self):
        pattern = '{first_name} {last_name} {middle_name}'

        first_name = self.first_name
        last_name = ''
        middle_name = ''

        if self.last_name:
            last_name = '%s.' % self.last_name[0].upper()
        if self.middle_name:
            middle_name = '%s.' % self.middle_name[0].upper()
        return pattern.format(first_name=first_name, last_name=last_name,
                              middle_name=middle_name).strip()

    def get_email(self):
        return self.user.email
