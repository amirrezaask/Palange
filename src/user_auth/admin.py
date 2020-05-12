from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from user_auth.models import Profile

admin.site.unregister(User)


class ProfileAdmin(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = _('Profile')


@admin.register(User)
class UserAdmin(UserAdmin):
    inlines = [ProfileAdmin, ]
