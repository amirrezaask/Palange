from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from user_auth.models import Profile, OrganizerProfile

admin.site.unregister(User)
admin.site.register(Profile)

admin.site.register(OrganizerProfile)

class ProfileAdmin(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = _('Profile')


@admin.register(User)
class UserAdmin(UserAdmin):
    inlines = [ProfileAdmin, ]
