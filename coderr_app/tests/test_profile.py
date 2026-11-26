from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from ..models import BusinessUserProfile, CustomerProfile, FileUpload, User
from ..api.serializers import BusinessProfileSerializer, CustomerProfileSerializer, ProfileDetailSerializer


class ProfileTest(APITestCase):

    def setUp(self):
        self.image = FileUpload.objects.create(file='uploads/testBild.png')
        self.customer_user_1 = User.objects.create_user(
            username='Test Customer 1', password='asdasd', type=User.UserType.CUSTOMER)
        self.customer_user_2 = User.objects.create_user(
            username='Test Customer 2', password='asdasd', type=User.UserType.CUSTOMER)
        self.business_user_1 = User.objects.create_user(
            username='Test Business User 1', password='asdasd', type=User.UserType.BUSINESS)
        self.business_user_2 = User.objects.create_user(
            username='Test Business User 2', password='asdasd', type=User.UserType.BUSINESS)
        self.customer_profile_1 = CustomerProfile.objects.create(user=self.customer_user_1,
                                                                 file=self.image)
        self.customer_profile_2 = CustomerProfile.objects.create(
            user=self.customer_user_2)
        self.business_user_profile_1 = BusinessUserProfile.objects.create(
            user=self.business_user_1)
        self.business_user_profile_2 = BusinessUserProfile.objects.create(
            user=self.business_user_2, file=self.image, location='Hannover', tel='0511 1234 5678', description='Business User 2 Description', working_hours='9:00-17:00')
        self.client = APIClient()

    def login_test_user(self, test_user):
        self.client.logout()
        self.token, created = Token.objects.get_or_create(user=test_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_list_business_200(self):
        url = reverse('business-profile-list')
        self.login_test_user(self.customer_user_1)
        response = self.client.get(url)
        expected_data = [BusinessProfileSerializer(
            self.business_user_profile_1).data, BusinessProfileSerializer(self.business_user_profile_2).data]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_list_business_401(self):
        self.client.logout()
        url = reverse('business-profile-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_customer_200(self):
        url = reverse('customer-profile-list')
        self.login_test_user(self.business_user_1)
        response = self.client.get(url)
        expected_data = [CustomerProfileSerializer(
            self.customer_profile_1).data, CustomerProfileSerializer(self.customer_profile_2).data]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_list_customer_401(self):
        self.client.logout()
        url = reverse('customer-profile-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_busniness_200(self):
        url = reverse('profile-detail',
                      kwargs={'pk': self.business_user_1.id})
        self.login_test_user(self.business_user_1)
        response = self.client.get(url)
        expected_data = ProfileDetailSerializer(self.business_user_1).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.data['file'], None)

    def test_retrieve_customer_200(self):
        url = reverse('profile-detail',
                      kwargs={'pk': self.customer_user_1.id})
        self.login_test_user(self.business_user_1)
        response = self.client.get(url)
        expected_data = ProfileDetailSerializer(self.customer_user_1).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.data['file'], self.image.file.url)

    def test_retrieve_business_401(self):
        self.client.logout()
        url = reverse('profile-detail',
                      kwargs={'pk': self.business_user_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_404(self):
        not_found_id = 1023
        url = reverse('profile-detail',
                      kwargs={'pk': not_found_id})
        self.login_test_user(self.business_user_1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_business_200(self):
        url = reverse('profile-detail',
                      kwargs={'pk': self.business_user_1.id})
        self.login_test_user(self.business_user_1)
        response = self.client.patch(
            url, data={'first_name': 'Max', 'last_name': 'Mustermann'})
        expected_data = ProfileDetailSerializer(self.business_user_1).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.keys(), expected_data.keys())
        self.assertEqual(response.data['first_name'], 'Max')

    def test_update_customer_200(self):
        url = reverse('profile-detail',
                      kwargs={'pk': self.customer_user_1.id})
        self.login_test_user(self.customer_user_1)
        response = self.client.patch(
            url, data={'first_name': 'Max', 'last_name': 'Mustermann'})
        expected_data = ProfileDetailSerializer(self.customer_user_1).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.keys(), expected_data.keys())
        self.assertEqual(response.data['first_name'], 'Max')

    def test_update_401(self):
        self.client.logout()
        url = reverse('profile-detail',
                      kwargs={'pk': self.customer_user_1.id})
        response = self.client.patch(
            url, data={'first_name': 'Max', 'last_name': 'Mustermann'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_403(self):
        url = reverse('profile-detail',
                      kwargs={'pk': self.business_user_1.id})
        self.login_test_user(self.customer_user_1)
        response = self.client.patch(
            url, data={'first_name': 'Max', 'last_name': 'Mustermann'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_404(self):
        not_found_id = 1023
        url = reverse('profile-detail',
                      kwargs={'pk': not_found_id})
        self.login_test_user(self.customer_user_1)
        response = self.client.patch(
            url, data={'first_name': 'Max', 'last_name': 'Mustermann'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
