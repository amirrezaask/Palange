from django.urls import path

from trips import views as trips_views

app_name = 'trips'

urlpatterns = [
    path('new', trips_views.NewTripView.as_view(), name='new'),
    path('<int:pk>/edit', trips_views.EditTripView.as_view(), name='edit'),
    path('my', trips_views.MyTripsView.as_view(), name='my'),
    path('<int:pk>/detail', trips_views.TripDetailView.as_view(), name='detail'),
    path('list', trips_views.TripListView.as_view(), name='list'),
    path('<int:pk>/preregister', trips_views.PreRegisterView.as_view(), name='preregister'),
    path('<int:pk>/cancel_preregister', trips_views.CancelPreRegisterView.as_view(), name='cancel_preregister'),
    path('management', trips_views.TripsManagementView.as_view(), name='management'),
    path('<int:pk>/manage', trips_views.ManageTripView.as_view(), name='manage'),
    path('preregister/<int:pk>/approve', trips_views.ApprovePreRegisterView.as_view(), name='approve'),
    path('preregister/<int:pk>/pay', trips_views.pay_preregister, name="pay"),
    path('trip/<int:trip_id>/comment', trips_views.add_comment, name='add_comment'),
    path('trip/<int:trip_id>/rate', trips_views.add_rate, name='add_rate'),
    path('search', trips_views.SearchView.as_view(), name='search'),
    path('ads/new', trips_views.NewAdsView.as_view(), name='new_ads'),
    path('ads/list', trips_views.AdsListView.as_view(), name='list_ads'),
    path('ads/approve/<int:ad_id>', trips_views.ads_approve, name="approve_ad")
]
