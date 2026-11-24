from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from ..models import FileUpload, Offer, OfferDetail, User
from ..api.serializers import OfferDetailSerializer


class OfferDetailTest(APITestCase):

    def setUp(self):
        self.customer_user_1 = User.objects.create_user(
            username='testCustomer1', password='asdasd', type='customer')
        self.image = FileUpload.objects.create(file='uploads/testBild.png')
        self.offer_1 = Offer.objects.create(
            user=self.customer_user_1, title='Test offer 1', image=self.image, description='Test offer 1 description')
        self.offer_detail_1 = OfferDetail.objects.create(title='Test Offer Detail 1', revisions=4, delivery_time_in_days=24, price=100.00, features=[
                                                         'feat1', 'feat2'], offer_type=OfferDetail.OfferType.BASIC, offer=self.offer_1)
        self.client = APIClient()

    def login_test_user(self, test_user):
        self.client.logout()
        self.token, created = Token.objects.get_or_create(user=test_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_retrieve_200(self):
        url = reverse('offerdetail', kwargs={'id': self.offer_detail_1.id})
        self.login_test_user(self.customer_user_1)
        response = self.client.get(url)
        expected_data = OfferDetailSerializer(self.offer_detail_1).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_retrieve_401(self):
        url = reverse('offerdetail', kwargs={'id': self.offer_detail_1.id})
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_404(self):
        not_found_id = 1023
        url = reverse('offerdetail', kwargs={'id': not_found_id})
        self.login_test_user(self.customer_user_1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
