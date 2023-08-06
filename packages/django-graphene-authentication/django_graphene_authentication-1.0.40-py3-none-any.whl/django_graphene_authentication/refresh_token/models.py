import binascii
import os
from calendar import timegm
from datetime import datetime

from django.conf import settings
from django.db import models
from django.http import HttpRequest
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from . import managers, signals
from django_graphene_authentication.conf import settings


class AbstractRefreshToken(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='refresh_tokens',
        verbose_name=_('user'),
    )
    token = models.CharField(_('token'), max_length=255, editable=False)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    revoked = models.DateTimeField(_('revoked'), null=True, blank=True)

    objects = managers.RefreshTokenQuerySet.as_manager()

    class Meta:
        abstract = True
        verbose_name = _('refresh token')
        verbose_name_plural = _('refresh tokens')
        unique_together = ('token', 'revoked')

    def __str__(self):
        return self.token

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self._cached_token = self.generate_token()

        super().save(*args, **kwargs)

    def generate_token(self):
        return binascii.hexlify(
            os.urandom(settings.GRAPHENE_AUITHENTICATION_JWT_REFRESH_TOKEN_N_BYTES),
        ).decode()

    def get_token(self):
        if hasattr(self, '_cached_token'):
            return self._cached_token
        return self.token

    def is_expired(self, request=None) -> bool:
        orig_iat = timegm(self.created.timetuple())
        return self.refresh_expired_handler(orig_iat, request)

    def refresh_expired_handler(self, orig_iat: datetime, request: HttpRequest):
        exp = orig_iat + settings.GRAPHENE_AUITHENTICATION_JWT_REFRESH_EXPIRATION_DELTA.total_seconds()
        return timegm(datetime.utcnow().utctimetuple()) > exp

    def revoke(self, request=None):
        self.revoked = timezone.now()
        self.save(update_fields=['revoked'])

        signals.refresh_token_revoked.send(
            sender=AbstractRefreshToken,
            request=request,
            refresh_token=self,
        )

    def reuse(self, request=None):
        self.token = ''
        self.created = timezone.now()
        self.save(update_fields=['token', 'created'])


class RefreshToken(AbstractRefreshToken):
    """RefreshToken default model"""
