from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from ..models import FileUpload, Offer, OfferDetail, User
from ..api.serializers import OfferRetrieveSerializer, OfferUpdateSerializer


class OfferTest(APITestCase):

    def setUp(self):
        self.customer_user_1 = User.objects.create_user(
            username='testCustomer1', password='asdasd', type='customer')
        self.business_user_1 = User.objects.create_user(
            username='Test Business User 1', password='asdasd', type=User.UserType.BUSINESS)
        self.business_user_2 = User.objects.create_user(
            username='Test Business User 2', password='asdasd', type=User.UserType.BUSINESS)
        self.image = FileUpload.objects.create(file='uploads/testBild.png')
        self.offer_1 = Offer.objects.create(
            user=self.business_user_1, title='Test offer 1', image=self.image, description='Test offer 1 description')
        self.offer_detail_1 = OfferDetail.objects.create(title='Test Offer Detail 1', revisions=4, delivery_time_in_days=24, price=100.00, features=[
                                                         'feat1', 'feat2'], offer_type=OfferDetail.OfferType.BASIC, offer=self.offer_1)
        self.offer_detail_2 = OfferDetail.objects.create(title='Test Offer Detail 2', revisions=5, delivery_time_in_days=32, price=200.00, features=[
                                                         'feat1', 'feat2'], offer_type=OfferDetail.OfferType.STANDARD, offer=self.offer_1)
        self.offer_detail_3 = OfferDetail.objects.create(title='Test Offer Detail 3', revisions=6, delivery_time_in_days=48, price=300.00, features=[
                                                         'feat1', 'feat2'], offer_type=OfferDetail.OfferType.PREMIUM, offer=self.offer_1)
        self.client = APIClient()

    def login_test_user(self, test_user):
        self.client.logout()
        self.token, created = Token.objects.get_or_create(user=test_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_retrieve_200(self):
        url = reverse('offer-detail', kwargs={'id': self.offer_1.id})
        self.login_test_user(self.customer_user_1)
        response = self.client.get(url)
        expected_data = OfferRetrieveSerializer(
            self.offer_1, context={'request': response.renderer_context['request']}).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.data['min_price'], 100.00)

    def test_retrieve_401(self):
        self.client.logout()
        url = reverse('offer-detail', kwargs={'id': self.offer_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_404(self):
        not_found_id = 1023
        url = reverse('offer-detail', kwargs={'id': not_found_id})
        self.login_test_user(self.customer_user_1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_200(self):
        url = reverse('offer-detail', kwargs={'id': self.offer_1.id})
        self.login_test_user(self.business_user_1)
        response = self.client.patch(url, data={'title': 'Test Update Offer'})
        expected_data = OfferUpdateSerializer(
            self.offer_1, context={'request': response.renderer_context['request']}).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.keys(), expected_data.keys())
        self.assertEqual(response.data['title'], 'Test Update Offer')

    def test_update_incomplete_data_400(self):
        url = reverse('offer-detail', kwargs={'id': self.offer_1.id})
        self.login_test_user(self.business_user_1)
        response = self.client.patch(url, data={'title': 'Test Update Offer', 'details': [
                                     {'title': 'Incomplete detail'}]})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_401(self):
        self.client.logout()
        url = reverse('offer-detail', kwargs={'id': self.offer_1.id})
        response = self.client.patch(url, data={'title': 'Test Update Offer'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_403(self):
        url = reverse('offer-detail', kwargs={'id': self.offer_1.id})
        self.login_test_user(self.business_user_2)
        response = self.client.patch(url, data={'title': 'Test Update Offer'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_404(self):
        not_found_id = 1023
        url = reverse('offer-detail', kwargs={'id': not_found_id})
        self.login_test_user(self.business_user_1)
        response = self.client.patch(url, data={'title': 'Test Update Offer'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_destroy_204(self):
        url = reverse('offer-detail', kwargs={'id': self.offer_1.id})
        self.login_test_user(self.business_user_1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)

    def test_destroy_401(self):
        self.client.logout()
        url = reverse('offer-detail', kwargs={'id': self.offer_1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_destroy_403(self):
        url = reverse('offer-detail', kwargs={'id': self.offer_1.id})
        self.login_test_user(self.business_user_2)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_404(self):
        not_found_id = 1023
        url = reverse('offer-detail', kwargs={'id': not_found_id})
        self.login_test_user(self.business_user_1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
