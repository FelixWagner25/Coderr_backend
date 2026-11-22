from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from ..models import Review, User


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

    def test_list_reviews_all_200(self):
        url = reverse('review-list')
        self.login_test_user(self.customer_user_1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
