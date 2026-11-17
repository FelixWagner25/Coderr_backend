from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from coderr_app.models import User


class LoginTests(APITestCase):
    def setUp(self):
        self.testUser = User.objects.create_user(
            username='testUser', password='asdasd', email="testmail@testuser.de")
        self.token = Token.objects.create(user=self.testUser)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_user_login_200(self):
        url = reverse('login')
        data = {'username': 'testUser',
                'password': 'asdasd'}
        response = self.client.post(url, data, format='json')
        self.testUser = User.objects.get(username='testUser')
        self.token = Token.objects.get(user=self.testUser)
        expected_data = {'token': self.token.key,
                         'username': self.testUser.username, 'email': self.testUser.email, 'user_id': self.testUser.id}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_user_login_400(self):
        url = reverse('login')
        data = {'username': 'testUser',
                'password': 'jkljkl'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
