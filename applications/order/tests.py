from django.test import TestCase
from django.contrib.auth import get_user_model
from applications.apartment.models import Category, Apartment, ApartmentAmenity
from .models import Order

User = get_user_model()


# class OrderModelTest(TestCase):
#     def setUp(self):
#         user = User.objects.create_user(email='testuser@example.com', password='testpassword')
#         category = Category.objects.create(name='Test Category')
#         apartment = Apartment.objects.create(
#             owner=user,
#             category=category,
#             title='Test Apartment',
#             location='Test Location',
#             price=100.00,
#             education='Test Education',
#             description='Test Description'
#         )
#         self.order = Order.objects.create(
#             user=user,
#             apartment=apartment,
#             start_date='2023-01-01',
#             end_date='2023-01-10',
#             man=2,
#             kids=1,
#             animals=True,
#             street='Test Street',
#             city='Test City',
#             state='Test State',
#             postal_code='12345',
#             country='Test Country',
#         )
#
#     def test_order_creation(self):
#         self.assertEqual(self.order.user.email, 'testuser@example.com')
#         self.assertEqual(self.order.apartment.title, 'Test Apartment')
#         self.assertEqual(str(self.order.start_date), '2023-01-01')
#         self.assertEqual(str(self.order.end_date), '2023-01-10')
#         self.assertEqual(self.order.man, 2)
#         self.assertEqual(self.order.kids, 1)
#         self.assertTrue(self.order.animals)
#         self.assertEqual(self.order.street, 'Test Street')
#         self.assertEqual(self.order.city, 'Test City')
#         self.assertEqual(self.order.state, 'Test State')
#         self.assertEqual(self.order.postal_code, '12345')
#         self.assertEqual(self.order.country, 'Test Country')
#         self.assertFalse(self.order.is_active)  # The default value is False
#         self.assertEqual(self.order.activation_code, '')  # It should be empty initially
#
#     def test_create_activation_code(self):
#         self.order.create_activation_code()
#         self.assertTrue(self.order.activation_code)
