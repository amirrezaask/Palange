from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Profile(models.Model):
    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_('User'))

    phone_number = models.CharField(max_length=11, verbose_name=_('Phone Number'))
    is_organizer = models.BooleanField(default=False, verbose_name=_('Is Organizer'))
    favorite_tags = models.CharField(max_length=2000, verbose_name=_("Favorite Tags"))

    def tags(self):
        return self.favorite_tags.split(",")
    def __str__(self):
        return f'{self.user}'

    def __repr__(self):
        return f'<Profile: {self}>'


class OrganizerProfile(models.Model):
    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
        
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    profile_picture = models.URLField(max_length=255)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.profile.user.first_name + " " + self.profile.user.last_name

