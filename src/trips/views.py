from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View, CreateView, UpdateView, ListView, DetailView

from trips.mixins import OrganizerRequiredMixin, IsTripOrganizerMixin
from trips.models import Trip, PreRegister, TripPayment, TripRate, TripFeedback, Comment

from user_auth.models import Profile

class NewTripView(LoginRequiredMixin, OrganizerRequiredMixin, CreateView):
    model = Trip
    fields = ['title', 'description', 'start_date',
              'end_date', 'capacity', 'price','image']
    template_name = 'new_trip.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.organizer = self.request.user.profile
        return super(NewTripView, self).form_valid(form)


class EditTripView(LoginRequiredMixin, IsTripOrganizerMixin, UpdateView):
    model = Trip
    fields = ['title', 'description', 'start_date',
              'end_date', 'capacity', 'image']
    template_name = 'edit_trip.html'
    success_url = reverse_lazy('home')


class TripsManagementView(LoginRequiredMixin, OrganizerRequiredMixin, ListView):
    model = Trip
    template_name = 'trips_management.html'

    def get_queryset(self):
        return self.request.user.profile.trip_set.all().reverse()


class TripListView(ListView):
    model = Trip
    template_name = 'trip_list.html'
    ordering = '-id'


class TripDetailView(DetailView):
    model = Trip
    template_name = 'trip_detail.html'

    def get_context_data(self, **kwargs):
        context_data = super(TripDetailView, self).get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            return context_data
        try:
            context_data['preregister'] = PreRegister.objects.get(
                trip=self.object, profile=self.request.user.profile)
        except PreRegister.DoesNotExist:
            pass
        trip_id = context_data["trip"].pk
        trip_rates = TripRate.objects.filter(trip=trip_id).order_by("pk")
        trip_feeds = TripFeedback.objects.filter(trip=trip_id).order_by("pk")
        context_data['trip_rates'] = trip_rates
        context_data['trip_feeds'] = trip_feeds
        context_data['comments'] = self.object.comments()
        return context_data

def add_comment(req, trip_id):
    print(req.POST)
    profile = get_object_or_404(Profile, user=req.user.pk)
    trip = get_object_or_404(Trip, pk=trip_id)
    Comment.objects.create(trip=trip, profile=profile, text=req.POST['text'])
    return redirect('trips:detail', pk=trip_id)

def get_ipg():
    return ("", "")
    
def trip_payment_inti(req):
    trip_id = req.GET["trip"]
    pre_register_id = req.GET["pre_register_id"]
    pre_register = get_object_or_404(PreRegister, pk=pre_register_id)
    if pre_register.is_paid:
        # error pre register is already paid
        pass
    tp = TripPayment(trip=trip_id, pre_register=pre_register_id, state=0)
    uuid, url = get_ipg()
    tp.ipg_uuid = uuid
    tp.save()
    return redirect(req, url)
    
def trip_payment_ipg_callback(req):
    payment_uuid = req.GET["uuid"]
    tp = get_object_or_404(TripPayment, pk=payment_uuid)
    tp.state = 2
    tp.save()
    # return payment successfull page
    return


class PreRegisterView(LoginRequiredMixin, View):
    def get(self, request, pk):
        return self.post(request, pk)

    def post(self, request, pk):
        trip = get_object_or_404(Trip, id=pk)
        PreRegister.objects.get_or_create(
            profile=request.user.profile, trip=trip)
        messages.success(request, _(
            'You preregistered successfully, approvement pending.'))
        return redirect('trips:detail', pk)


class CancelPreRegisterView(LoginRequiredMixin, View):
    def post(self, request, pk):
        PreRegister.objects.filter(
            profile=request.user.profile, trip_id=pk).delete()
        messages.warning(request, _('We will miss you :('))
        return redirect('trips:detail', pk)


class MyTripsView(LoginRequiredMixin, ListView):
    model = PreRegister
    template_name = 'my_trips.html'

    def get_queryset(self):
        return self.request.user.profile.preregister_set.all()


class ManageTripView(LoginRequiredMixin, OrganizerRequiredMixin, DetailView):
    model = Trip
    template_name = 'manage_trip.html'


class ApprovePreRegisterView(LoginRequiredMixin, OrganizerRequiredMixin, View):
    def post(self, request, pk):
        preregister = get_object_or_404(PreRegister, id=pk)
        if preregister.trip.organizer_id != self.request.user.profile.id:
            raise PermissionDenied()
        preregister.is_approved = True
        preregister.save()
        messages.success(request, _('Just approved.'))
        return redirect('trips:manage', preregister.trip_id)
