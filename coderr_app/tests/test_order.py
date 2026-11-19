from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from coderr_app.models import FileUpload, Offer, OfferDetail, Order, User
from ..api.serializers import OrderCreateSerializer, OrderListSerializer


class OrderListCreateTest(APITestCase):
    url = reverse('order-list')

    def setUp(self):
        self.customer_user = User.objects.create_user(
            username='testCustomer', password='asdasd', type='customer')
        self.business_user = User.objects.create_user(
            username='testBusinessUser', password='asdasd', type='business')
        self.image = FileUpload.objects.create(file='uploads/testBild.png')
        self.offer = Offer.objects.create(
            user=self.business_user, title='Test Offer', image=self.image, description='test offer description')
        self.offer_detail_basic = OfferDetail.objects.create(title='Basic offer detail', revisions=2, delivery_time_in_days=5, price=100.0, features=[
                                                             'Feat1, Feat2'], offer_type=OfferDetail.OfferType.BASIC, offer=self.offer)
        self.order = Order.objects.create(customer=self.customer_user, business_user=self.business_user, title='Test Order', revisions=2, delivery_time_in_days=5, price=100.0, features=[
                                          'Feat1, Feat2'], offer_type=OfferDetail.OfferType.BASIC, status=Order.OrderStatus.IN_PROGRESS)
        self.customer_token = Token.objects.create(user=self.customer_user)
        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.customer_token.key)

    def test_list_get_order_200(self):
        response = self.client.get(self.url)
        expected_data = [OrderListSerializer(self.order).data]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_list_get_order_logged_out_401(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_201(self):
        response = self.client.post(
            self.url, data={'offer_detail_id': self.offer_detail_basic.id})
        expected_data = OrderCreateSerializer(self.order).data

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.keys(), expected_data.keys())
