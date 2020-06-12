from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseForbidden
from user_auth.forms import SignupForm
from user_auth.models import Profile, OrganizerProfile



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



def organizer_profile(req):
    organizer_id = req.GET["id"]
    profile_info = get_object_or_404(OrganizerProfile, pk=organizer_id)
    print(profile_info)
    return render(req, 'organizer_profile.html', {"profile": profile_info})


def update_organizer_profile(req):
    if not req.user.is_authenticated:
        return HttpResponseForbidden()
    if req.method == "GET":
        organizer_id = req.GET["id"]
        profile_info = get_object_or_404(OrganizerProfile, pk=organizer_id)
        
        return render(req, 'organizer_edit_profile.html', {"profile": profile_info})
    if req.method == "POST":
        organizer_id = req.GET["id"]
        if organizer_id != req.user.user_id:
            return HttpResponseForbidden()
        OrganizerProfile.filter(pk=organizer_id).update(**req.POST)
        return
                
