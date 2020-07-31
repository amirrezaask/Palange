from django.contrib import admin

from trips.models import Trip, PreRegister, Comment, TripFeedback, TripRate, Ads


admin.site.register(Comment)
admin.site.register(TripRate)
admin.site.register(TripFeedback)
admin.site.register(Ads)

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    pass


@admin.register(PreRegister)
class PreRegisterAdmin(admin.ModelAdmin):
    pass
