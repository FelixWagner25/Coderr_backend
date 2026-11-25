from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from ..models import BusinessUserProfile, CustomerProfile, FileUpload, User
from ..api.serializers import BusinessProfileSerializer


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

    def test_get_business_200(self):
        url = reverse('business-profile-list')
        self.login_test_user(self.customer_user_1)
        response = self.client.get(url)
        expected_data = [BusinessProfileSerializer(
            self.business_user_profile_1).data, BusinessProfileSerializer(self.business_user_profile_2).data]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
