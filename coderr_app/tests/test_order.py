from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token
from coderr_app.models import FileUpload, Offer, OfferDetail, Order, User
from ..api.serializers import OrderCreateSerializer, OrderListSerializer, OrderUpdateSerializer


class OrderTest(APITestCase):
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
        self.client = APIClient()

    def login_test_customer(self):
        self.client.logout()
        self.customer_token = Token.objects.create(user=self.customer_user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.customer_token.key)

    def login_test_business_user(self):
        self.client.logout()
        self.business_user_token = Token.objects.create(
            user=self.business_user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.business_user_token.key)

    def test_list_get_order_200(self):
        url = reverse('order-list')
        self.login_test_customer()
        response = self.client.get(url)
        expected_data = [OrderListSerializer(self.order).data]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_list_get_order_logged_out_401(self):
        url = reverse('order-list')
        self.client.logout()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_201(self):
        url = reverse('order-list')
        self.login_test_customer()
        response = self.client.post(
            url, data={'offer_detail_id': self.offer_detail_basic.id})
        expected_data = OrderCreateSerializer(self.order).data

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.keys(), expected_data.keys())

    def test_create_order_400(self):
        url = reverse('order-list')
        self.login_test_customer()
        response = self.client.post(
            url, data={'offer_detail_id': 'x'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_401(self):
        url = reverse('order-list')
        self.client.logout()
        response = self.client.post(
            url, data={'offer_detail_id': self.offer_detail_basic.id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_403(self):
        url = reverse('order-list')
        self.login_test_business_user()
        response = self.client.post(
            url, data={'offer_detail_id': self.offer_detail_basic.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_order_404(self):
        url = reverse('order-list')
        self.login_test_customer()
        not_found_id = self.offer_detail_basic.id + 2
        response = self.client.post(
            url, data={'offer_detail_id': not_found_id})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_order_200(self):
        url = reverse('order-detail', kwargs={'id': self.order.id})
        self.login_test_business_user()
        response = self.client.patch(
            url, data={'status': Order.OrderStatus.COMPLETED})
        expected_data = OrderUpdateSerializer(self.order).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.keys(), expected_data.keys())

    def test_update_order_400(self):
        url = reverse('order-detail', kwargs={'id': self.order.id})
        self.login_test_business_user()
        response = self.client.patch(
            url, data={'status': 'asdfasd'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_order_401(self):
        url = reverse('order-detail', kwargs={'id': self.order.id})
        self.client.logout()
        response = self.client.patch(
            url, data={'status': Order.OrderStatus.COMPLETED})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_order_403(self):
        url = reverse('order-detail', kwargs={'id': self.order.id})
        self.login_test_customer()
        response = self.client.patch(
            url, data={'status': Order.OrderStatus.COMPLETED})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_order_404(self):
        not_found_id = 1024
        url = reverse('order-detail', kwargs={'id': not_found_id})
        self.login_test_business_user()
        response = self.client.patch(
            url, data={'status': Order.OrderStatus.COMPLETED})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
