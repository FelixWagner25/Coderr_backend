from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from coderr_app.models import User
from ..api.serializers import UserLoginSerializer


class LoginTests(APITestCase):
    def setUp(self):
        self.testUser = User.objects.create_user(
            username='testUser', password='asdasd')

    def test_user_login_200(self):
        url = reverse('login')
        data = {'username': 'testUser',
                'password': 'asdasd'}
        response = self.client.post(url, data, format='json')
        expected_data = UserLoginSerializer(self.testUser).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_user_login_400(self):
        url = reverse('login')
        data = {'username': 'testUser',
                'password': 'jkljkl'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
