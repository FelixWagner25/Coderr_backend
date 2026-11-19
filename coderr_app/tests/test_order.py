from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from coderr_app.models import FileUpload, Offer, OfferDetail, Order, User
from ..api.serializers import OrderSerializer


class OrderListCreateTest(APITestCase):
    url = reverse('order-list')

    def setUp(self):
        self.customer_user = User.objects.create_user(
            username='testCustomer', password='asdasd')
        self.business_user = User.objects.create_user(
            username='testBusinessUser', password='asdasd')
        self.image = FileUpload.objects.create(file='uploads/testBild.png')
        self.offer = Offer.objects.create(
            user=self.business_user, title='Test Offer', image=self.image, description='test offer description')
        self.offer_detail_basic = OfferDetail.objects.create(title='Basic offer detail', revisions=2, delivery_time_in_days=5, price=100.0, features=[
                                                             'Feat1, Feat2'], offer_type=OfferDetail.OfferType.BASIC, offer=self.offer)
        self.order = Order.objects.create(customer=self.customer_user, business_user=self.business_user, title='Test Order', revisions=2, delivery_time_in_days=5, price=100.0, features=[
                                          'Feat1, Feat2'], offer_type=OfferDetail.OfferType.BASIC, offer=self.offer, status=Order.OrderStatus.IN_PROGRESS)
        self.customer_token = Token.objects.create(user=self.customer_user)
        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.customer_token.key)

    def test_list_get_order_200(self):
        response = self.client.get(self.url)
        expected_data = [OrderSerializer(self.order).data]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
