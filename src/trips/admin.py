from django.contrib import admin

from trips.models import Trip, PreRegister


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    pass


@admin.register(PreRegister)
class PreRegisterAdmin(admin.ModelAdmin):
    pass
