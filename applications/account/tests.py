from django.test import TestCase
from django.core.cache import cache
from .models import CustomUser


class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="testpassword",
            name="Test",
            surname="User"
        )

    def test_create_user(self):
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertEqual(self.user.name, "Test")
        self.assertEqual(self.user.surname, "User")
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertFalse(self.user.is_active)

    def test_create_superuser(self):
        superuser = CustomUser.objects.create_superuser(
            email="superuser@example.com",
            password="superpassword",
            name="Super",
            surname="User"
        )
        self.assertEqual(superuser.email, "superuser@example.com")
        self.assertEqual(superuser.name, "Super")
        self.assertEqual(superuser.surname, "User")
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)

    def test_create_activation_code(self):
        self.user.create_activation_code()
        self.assertIsNotNone(self.user.activation_code)

    def test_str_representation(self):
        self.assertEqual(str(self.user), "testuser@example.com")


class MyCacheTestCase(TestCase):
    """
        Тесты для кэша.
    """

    def test_caching(self):
        """
            Проверка кэширования значения.
        """
        cache.set('my_key', 'my_value', 60)

        cached_value = cache.get('my_key')
        self.assertEqual(cached_value, 'my_value')

    def test_cache_timeout(self):
        """
            Проверка срока действия кэша.
        """
        cache.set('my_key', 'my_value', 1)

        import time
        time.sleep(2)

        cached_value = cache.get('my_key')
        self.assertIsNone(cached_value)

