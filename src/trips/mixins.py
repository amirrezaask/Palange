from django.contrib.auth.mixins import AccessMixin
from django.utils.translation import ugettext_lazy as _


class OrganizerRequiredMixin(AccessMixin):
    """Verify that the current user is a organizer."""
    permission_denied_message = _('You are not an organizer')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.profile.is_organizer:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class IsTripOrganizerMixin(AccessMixin):
    """Verify that the current user is organizer of the trip"""
    permission_denied_message = _('You are not manager of this trip')

    def is_manager_of(self, trip_id):
        return self.request.user.profile.trip_set.filter(id=trip_id).exists()

    def dispatch(self, request, *args, **kwargs):
        if not self.is_manager_of(trip_id=kwargs.get('pk') or kwargs.get('trip_id')):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
