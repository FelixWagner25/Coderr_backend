from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from ..models import Review, User
from ..api.serializers import ReviewSerializer


class ReviewTest(APITestCase):

    def setUp(self):
        self.customer_user_1 = User.objects.create_user(
            username='testCustomer1', password='asdasd', type='customer')
        self.business_user_1 = User.objects.create_user(
            username='testBusinessUser1', password='asdasd', type='business')
        self.customer_user_2 = User.objects.create_user(
            username='testCustomer2', password='asdasd', type='customer')
        self.business_user_2 = User.objects.create_user(
            username='testBusinessUser2', password='asdasd', type='business')
        self.review_1 = Review.objects.create(
            business_user=self.business_user_1, reviewer=self.customer_user_1, rating=5, description='Five stars')
        self.review_2 = Review.objects.create(
            business_user=self.business_user_2, reviewer=self.customer_user_2, rating=4, description='Four stars')
        self.review_3 = Review.objects.create(
            business_user=self.business_user_1, reviewer=self.customer_user_2, rating=3, description='Three stars')
        self.client = APIClient()

    def login_test_user(self, test_user):
        self.client.logout()
        self.token, created = Token.objects.get_or_create(user=test_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_list_all_200(self):
        url = reverse('review-list')
        self.login_test_user(self.customer_user_1)
        response = self.client.get(url)
        expected_data = [ReviewSerializer(self.review_1).data, ReviewSerializer(
            self.review_2).data, ReviewSerializer(self.review_3).data]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_list_all_401(self):
        self.client.logout()
        url = reverse('review-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_201(self):
        url = reverse('review-list')
        self.login_test_user(self.customer_user_1)
        response = self.client.post(
            url, data={'business_user': 2, 'rating': 4, 'description': 'Schön'})
        expected_data = ReviewSerializer(self.review_1).data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.keys(), expected_data.keys())

    def test_create_missing_data_400(self):
        url = reverse('review-list')
        self.login_test_user(self.customer_user_1)
        response = self.client.post(
            url, data={'business_user': 2, 'description': 'Schön'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_401(self):
        url = reverse('review-list')
        self.client.logout()
        response = self.client.post(
            url, data={'business_user': 2, 'rating': 4, 'description': 'Schön'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_no_customer_403(self):
        url = reverse('review-list')
        self.login_test_user(self.business_user_1)
        response = self.client.post(
            url, data={'business_user': 4, 'rating': 4, 'description': 'Schön'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
