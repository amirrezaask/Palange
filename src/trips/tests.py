from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy

from trips.models import Trip
from user_auth.models import Profile


class NewTripViewTest(TestCase):
    def setUp(self):
        self.organizer_profile = mommy.make(Profile, is_organizer=True)
        self.non_organizer_profile = mommy.make(Profile, is_organizer=False)

    def test_new_trip_works_correctly(self):
        self.client.force_login(self.organizer_profile.user)
        self.client.post(reverse('trips:new'), data=dict(
            title='title',
            description='description',
            start_date='2020-02-02 20:20:20',
            end_date='3030-03-03 20:30:30',
            capacity='10',
        ))
        self.assertEqual(self.organizer_profile.trip_set.first().title, 'title')

    def test_non_organizer_can_not_submit_new_trip(self):
        self.client.force_login(self.non_organizer_profile.user)
        response = self.client.get(reverse('trips:new'))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('trips:new'))
        self.assertEqual(response.status_code, 403)


class EditTripViewTest(TestCase):
    def setUp(self):
        self.organizer_profile_1 = mommy.make(Profile, is_organizer=True)
        self.organizer_profile_2 = mommy.make(Profile, is_organizer=True)
        mommy.make(Trip, _quantity=2, organizer=self.organizer_profile_1)
        mommy.make(Trip, _quantity=3, organizer=self.organizer_profile_2)
        self.non_organizer_profile = mommy.make(Profile, is_organizer=False)

    def test_edit_trip_works_correctly(self):
        self.client.force_login(self.organizer_profile_1.user)
        editing_trip = self.organizer_profile_1.trip_set.first()
        self.client.post(reverse('trips:edit', args=[editing_trip.id]), data=dict(
            title='new title',
            description='new description',
            start_date='2020-02-02 20:20:20',
            end_date='3030-03-03 20:30:30',
            capacity='10',
        ))
        editing_trip.refresh_from_db()
        self.assertEqual(editing_trip.title, 'new title')
        self.assertEqual(editing_trip.description, 'new description')
        self.assertEqual(str(editing_trip.start_date), '2020-02-02 16:50:20+00:00')
        self.assertEqual(str(editing_trip.end_date), '3030-03-03 17:00:30+00:00')
        self.assertEqual(editing_trip.capacity, 10)

    def test_non_organizer_can_not_edit_trip(self):
        self.client.force_login(self.non_organizer_profile.user)
        response = self.client.get(reverse('trips:edit', args=[1]))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('trips:edit', args=[1]))
        self.assertEqual(response.status_code, 403)

    def test_not_related_organizer_can_not_edit_trip(self):
        self.client.force_login(self.organizer_profile_1.user)
        response = self.client.get(reverse('trips:edit', args=[self.organizer_profile_2.trip_set.first().id]))
        self.assertEqual(response.status_code, 403)
        response = self.client.post(reverse('trips:edit', args=[self.organizer_profile_2.trip_set.first().id]))
        self.assertEqual(response.status_code, 403)


class MyTripsViewTest(TestCase):
    def setUp(self):
        self.organizer_profile_1 = mommy.make(Profile, is_organizer=True)
        self.organizer_profile_2 = mommy.make(Profile, is_organizer=True)
        mommy.make(Trip, _quantity=2, organizer=self.organizer_profile_1)
        mommy.make(Trip, _quantity=3, organizer=self.organizer_profile_2)

    def test_my_trips_works_correctly(self):
        self.client.force_login(self.organizer_profile_1.user)
        response = self.client.get(reverse('trips:my'))
        self.assertListEqual(list(self.organizer_profile_1.trip_set.all()), list(response.context['trip_list']))
