from django.test import TestCase
from .models import DollarRate
from decimal import Decimal
from django.utils import timezone


class DollarRateModelTestCase(TestCase):
    def test_create_dollar_rate(self):

        dollar_rate = DollarRate(rate=Decimal('1.25'))
        dollar_rate.save()

        # Получаем объект из базы данных
        saved_dollar_rate = DollarRate.objects.get(id=dollar_rate.id)

        self.assertEqual(saved_dollar_rate.rate, Decimal('1.25'))

    def test_str_representation(self):

        dollar_rate = DollarRate(rate=Decimal('1.25'))
        dollar_rate.save()

        self.assertEqual(str(dollar_rate), f'Rate: 1.25 on {dollar_rate.date}')
