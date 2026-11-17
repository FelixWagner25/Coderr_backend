from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from coderr_app.models import User


class RegistrationTests(APITestCase):
    url = reverse('registration')

    def test_user_registration_201(self):
        data = {'username': 'testRegistrationUser', 'email': 'testemail@testuser.de',
                'password': 'asdasd', 'repeated_password': 'asdasd', 'type': 'customer'}
        response = self.client.post(self.url, data, format='json')
        new_test_user = User.objects.get(username='testRegistrationUser')
        new_test_user_token = Token.objects.get(user=new_test_user)
        expected_data = {'token': new_test_user_token.key, 'username': 'testRegistrationUser',
                         'email': 'testemail@testuser.de', 'user_id': new_test_user.id}
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_data)

    def test_user_registration_400(self):
        pass

    def test_user_registration_invalid_type_400(self):
        pass

    def test_user_registration_repeated_400(self):
        pass


class LoginTests(APITestCase):
    url = reverse('login')

    def setUp(self):
        self.testUser = User.objects.create_user(
            username='testUser', password='asdasd', email="testmail@testuser.de")
        self.token = Token.objects.create(user=self.testUser)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_user_login_200(self):
        data = {'username': 'testUser',
                'password': 'asdasd'}
        response = self.client.post(self.url, data, format='json')
        self.testUser = User.objects.get(username='testUser')
        self.token = Token.objects.get(user=self.testUser)
        expected_data = {'token': self.token.key,
                         'username': self.testUser.username, 'email': self.testUser.email, 'user_id': self.testUser.id}

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_user_login_400(self):
        data = {'username': 'testUser',
                'password': 'jkljkl'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
