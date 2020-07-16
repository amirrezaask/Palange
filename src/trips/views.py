from datetime import datetime, timezone

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View, CreateView, UpdateView, ListView, DetailView
import time

from pytz import utc
from trips.mixins import OrganizerRequiredMixin, IsTripOrganizerMixin
from trips.models import Trip, PreRegister, TripPayment, TripRate, TripFeedback, Comment

from user_auth.models import Profile

class NewTripView(LoginRequiredMixin, OrganizerRequiredMixin, CreateView):
    model = Trip
    fields = ['title', 'description', 'start_date', 'tags_raw',
              'end_date', 'capacity', 'price','image']
    template_name = 'new_trip.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.organizer = self.request.user.profile
        return super(NewTripView, self).form_valid(form)


class EditTripView(LoginRequiredMixin, IsTripOrganizerMixin, UpdateView):
    model = Trip
    fields = ['title', 'description', 'start_date', 'tags_raw',
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
    def get_context_data(self, **kwargs):
        context_data = super(TripListView, self).get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            return context_data
        profile = Profile.objects.get(user=self.request.user)
        if len(profile.tags()) < 1:
            return context_data
        fav_trips = []
        for t in profile.tags():
            fav_trips += list(Trip.objects.filter(tags_raw__icontains=t))
        context_data['fav_trips'] = fav_trips
        print(context_data)
        return context_data


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
        trip = Trip.objects.filter(pk=trip_id).get()
        trip_rates = TripRate.objects.filter(trip=trip).order_by("pk").all()
        trip_feeds = TripFeedback.objects.filter(trip=trip).order_by("pk").all()
        context_data['rates'] = trip_rates
        context_data['feedbacks'] = trip_feeds
        context_data['comments'] = self.object.comments()
        context_data['is_done'] = trip.end_date < utc.localize(datetime.now())
        return context_data

def add_comment(req, trip_id):
    profile = get_object_or_404(Profile, user=req.user.pk)
    trip = get_object_or_404(Trip, pk=trip_id)
    if trip.end_date < utc.localize(datetime.now()):
        TripFeedback.objects.create(trip=trip, user=profile, comment=req.POST['text'])
    else:
        Comment.objects.create(trip=trip, profile=profile, text=req.POST['text'])
    return redirect('trips:detail', pk=trip_id)

def add_rate(req, trip_id):
    rate = req.POST['rate']
    profile = get_object_or_404(Profile, user=req.user.pk)
    trip = get_object_or_404(Trip, pk=trip_id)
    if trip.end_date >  utc.localize(datetime.now()):
        raise Exception()
    TripRate.objects.create(trip=trip, user=req.user.profile, rate=rate)
    return redirect('trips:detail', pk=trip_id)

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

def pay_preregister(req, pk):
    pre_register = get_object_or_404(PreRegister, pk=pk)
    pre_register.is_paid = True
    pre_register.save()
    return redirect('trips:management')

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

class SearchView(ListView):
    model = Trip
    template_name = 'search.html'

    def get(self, req):
       query = req.GET.get('query')
       if not query:
           return render(req, 'search.html', {})
       result1 = Trip.objects.filter(title__icontains=query) | Trip.objects.filter(tags_raw__icontains=query)
       return render(req, 'search.html', {'all_search_result': result1})

def get_notifications(req):
    if not req.user.is_authenticated:
        raise PermissionDenied()
    my_tags = Profile.objects.filter(user=req.user.pk).all()[0].tags()
    selected_trips = []
    for t in my_tags:
        trips = Trip.objects.all()
        for trip in trips:
            if t in trip.tags():
                selected_trips.append(trip)
    return render(req, "notification.html", {"trips": selected_trips})