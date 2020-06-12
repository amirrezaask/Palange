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

    organizer = models.ForeignKey(
        Profile, on_delete=models.CASCADE, verbose_name=_('Organizer'))

    tags_raw = models.TextField(max_length=4096)

    title = models.CharField(max_length=128, verbose_name=_('Title'))
    description = models.TextField(
        max_length=1024, verbose_name=_('Description'))
    start_date = models.DateTimeField(verbose_name=_('Start Date'))
    end_date = models.DateTimeField(verbose_name=_('End Date'))
    capacity = models.PositiveIntegerField(verbose_name=_('Capacity'))
    image = models.ImageField(
        upload_to=image_upload_name, verbose_name=_('Image'))
    price = models.IntegerField()

    def comments(self):
        return Comment.objects.filter(trip=self.pk).all()

    def tags(self):
        return self.tags.split("|")
    def feedbacks(self):
        return TripFeedback.objects.filter(trip=self.pk)
    def rates(self):
        return TripRate.objects.filter(trip=self.pk)
    def __str__(self):
        return f'{self.title}'

    def __repr__(self):
        return f'<Trip: {self}>'


class Comment(models.Model):
    class Meta:
        verbose_name = _('Comments')
        verbose_name_plural = _('Comments')
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)


class PreRegister(models.Model):
    class Meta:
        verbose_name = _('PreRegister')
        verbose_name_plural = _('PreRegisters')
        unique_together = ['trip', 'profile']

    profile = models.ForeignKey(
        Profile, on_delete=models.PROTECT, verbose_name=_('Profile'))
    trip = models.ForeignKey(
        Trip, on_delete=models.PROTECT, verbose_name=_('Trip'))
    is_approved = models.BooleanField(
        default=False, verbose_name=_('Is Approved'))
    is_paid = models.BooleanField()


class TripPayment(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.PROTECT)
    pre_register = models.ForeignKey(PreRegister, on_delete=models.PROTECT)
    state = models.IntegerField()
    ipg_uuid = models.CharField(max_length=255)


class TripRate(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.PROTECT)
    user = models.ForeignKey(user_auth.models.Profile, on_delete=models.PROTECT)
    rate = models.IntegerField()

class TripFeedback(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.PROTECT)
    user = models.ForeignKey(user_auth.models.Profile, on_delete=models.PROTECT)
    comment = models.TextField(max_length=4096)