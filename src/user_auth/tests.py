from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from user_auth.models import Profile


class SignupTest(TestCase):
    def test_profile_is_created_correctly(self):
        self.client.post(path=reverse('auth:signup'), data=dict(
            username='some',
            phone_number='09123456789',
            password1='secure12345password',
            password2='secure12345password',
        ))
        user = User.objects.get(username='some')
        self.assertEqual(user.profile.phone_number, '09123456789')


class LoginTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='username', password='password', email='email@email.com')
        Profile.objects.create(user=user, phone_number='09123456789')

    def test_login_with_username(self):
        response = self.client.post(path=reverse('auth:login'), follow=True, data=dict(
            username='username',
            password='password',
        ))
        self.assertTrue(response.context['user'].is_active)

    def test_login_with_email(self):
        response = self.client.post(path=reverse('auth:login'), follow=True, data=dict(
            username='09123456789',
            password='password',
        ))
        self.assertTrue(response.context['user'].is_active)

    def test_login_with_phone_number(self):
        response = self.client.post(path=reverse('auth:login'), follow=True, data=dict(
            username='email@email.com',
            password='password',
        ))
        self.assertTrue(response.context['user'].is_active)

    def test_login_with_invalid_credentials(self):
        response = self.client.post(path=reverse('auth:login'), follow=True, data=dict(
            username='invalid',
            password='invalid',
        ))
        self.assertFalse(response.context['user'].is_active)
