from uuid import uuid4

from django.db import models
from django.utils.translation import ugettext_lazy as _

from user_auth.models import Profile


def image_upload_name(instance, filename):
    return f'trips/{str(uuid4())}.{filename.split(".")[-1]}'


class Trip(models.Model):
    class Meta:
        verbose_name = _('Trip')
        verbose_name_plural = _('Trips')

    organizer = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_('Organizer'))

    title = models.CharField(max_length=128, verbose_name=_('Title'))
    description = models.TextField(max_length=1024, verbose_name=_('Description'))
    start_date = models.DateTimeField(verbose_name=_('Start Date'))
    end_date = models.DateTimeField(verbose_name=_('End Date'))
    capacity = models.PositiveIntegerField(verbose_name=_('Capacity'))
    image = models.ImageField(upload_to=image_upload_name, verbose_name=_('Image'))

    def __str__(self):
        return f'{self.title}'

    def __repr__(self):
        return f'<Trip: {self}>'


class PreRegister(models.Model):
    class Meta:
        verbose_name = _('PreRegister')
        verbose_name_plural = _('PreRegisters')
        unique_together = ['trip', 'profile']

    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, verbose_name=_('Profile'))
    trip = models.ForeignKey(Trip, on_delete=models.PROTECT, verbose_name=_('Trip'))
    is_approved = models.BooleanField(default=False, verbose_name=_('Is Approved'))
