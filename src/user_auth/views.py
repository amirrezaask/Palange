from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseForbidden
from user_auth.forms import SignupForm
from user_auth.models import Profile, OrganizerProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from trips.mixins import OrganizerRequiredMixin, IsTripOrganizerMixin
from django.views.generic import View, CreateView, UpdateView, ListView, DetailView



class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form_valid = super(SignupView, self).form_valid(form)
        p = Profile.objects.create(user=form.instance, phone_number=form.cleaned_data.get('phone_number'))
        OrganizerProfile.objects.create(profile=p)
        login(self.request, form.instance)
        return form_valid



class OrganizerProfileDetailView(DetailView):
    model = OrganizerProfile
    template_name = 'organizer_profile_detail.html'
    def get_context_data(self, **kwargs):
        context_data = super(OrganizerProfileDetailView, self).get_context_data(**kwargs)
        return context_data

class EditOrganizerProfile(LoginRequiredMixin, IsTripOrganizerMixin, UpdateView):
    model = OrganizerProfile
    fields = ['profile_picture']
    template_name = 'organizer_edit_profile.html'
    success_url = reverse_lazy('home')