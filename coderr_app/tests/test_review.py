from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from ..models import Review, User
from ..api.serializers import ReviewListCreateSerializer, ReviewUpdateSerializer


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
        expected_data = [ReviewListCreateSerializer(self.review_1).data, ReviewListCreateSerializer(
            self.review_2).data, ReviewListCreateSerializer(self.review_3).data]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_list_all_401(self):
        self.client.logout()
        url = reverse('review-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_filter_business_user_200(self):
        url = reverse(
            'review-list')
        self.login_test_user(self.customer_user_1)
        response = self.client.get(
            url, {'business_user_id': self.business_user_1.id})
        expected_data = [ReviewListCreateSerializer(
            self.review_1).data, ReviewListCreateSerializer(self.review_3).data]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_list_filter_business_user_and_reviewer_200(self):
        url = reverse(
            'review-list')
        self.login_test_user(self.customer_user_1)
        response = self.client.get(
            url, {'business_user_id': self.business_user_1.id, 'reviewer_id': self.customer_user_2.id})
        expected_data = [ReviewListCreateSerializer(self.review_3).data]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_list_ordering_updated_at_200(self):
        url = reverse('review-list')
        self.login_test_user(self.customer_user_1)
        response = self.client.get(url, {'ordering': 'updated_at'})
        expected_data = [ReviewListCreateSerializer(self.review_1).data, ReviewListCreateSerializer(
            self.review_2).data, ReviewListCreateSerializer(self.review_3).data]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_list_ordering_rating_200(self):
        url = reverse('review-list')
        self.login_test_user(self.customer_user_1)
        response = self.client.get(url, {'ordering': '-rating'})
        expected_data = [ReviewListCreateSerializer(self.review_1).data, ReviewListCreateSerializer(
            self.review_2).data, ReviewListCreateSerializer(self.review_3).data]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_list_ordering_rating_reverse_200(self):
        url = reverse('review-list')
        self.login_test_user(self.customer_user_1)
        response = self.client.get(url, {'ordering': 'rating'})
        expected_data = [ReviewListCreateSerializer(self.review_3).data, ReviewListCreateSerializer(
            self.review_2).data, ReviewListCreateSerializer(self.review_1).data]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_create_201(self):
        url = reverse('review-list')
        self.login_test_user(self.customer_user_1)
        response = self.client.post(
            url, data={'business_user': 2, 'rating': 4, 'description': 'Schön'})
        expected_data = ReviewListCreateSerializer(self.review_1).data
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

    def test_retrieve_405(self):
        url = reverse('review-detail', kwargs={'id': self.review_1.id})
        self.login_test_user(self.customer_user_1)
        response = self.client.get(url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_200(self):
        url = reverse('review-detail', kwargs={'id': 1})
        self.login_test_user(self.customer_user_1)
        response = self.client.patch(
            url, data={'rating': 4, 'description': 'Update: Schön'})
        expected_data = ReviewUpdateSerializer(self.review_1).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.keys(), expected_data.keys())

    def test_update_invalid_data_400(self):
        url = reverse('review-detail', kwargs={'id': 1})
        self.login_test_user(self.customer_user_1)
        response = self.client.patch(
            url, data={'rating': 6, 'description': 'Update: Schön'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_401(self):
        self.client.logout()
        url = reverse('review-detail', kwargs={'id': 1})
        response = self.client.patch(
            url, data={'rating': 4, 'description': 'Update: Schön'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_403(self):
        url = reverse('review-detail', kwargs={'id': 1})
        self.login_test_user(self.customer_user_2)
        response = self.client.patch(
            url, data={'rating': 4, 'description': 'Update: Schön'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_404(self):
        not_found_id = 1024
        url = reverse('review-detail', kwargs={'id': not_found_id})
        self.login_test_user(self.customer_user_1)
        response = self.client.patch(
            url, data={'rating': 4, 'description': 'Update: Schön'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_204(self):
        url = reverse('review-detail', kwargs={'id': 1})
        self.login_test_user(self.customer_user_1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_401(self):
        self.client.logout()
        url = reverse('review-detail', kwargs={'id': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_403(self):
        url = reverse('review-detail', kwargs={'id': 1})
        self.login_test_user(self.customer_user_2)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_404(self):
        not_found_id = 1024
        url = reverse('review-detail', kwargs={'id': not_found_id})
        self.login_test_user(self.customer_user_1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
