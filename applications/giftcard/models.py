from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class GiftCard(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    title = models.CharField('Название', max_length=75)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    image = models.ImageField('Изображение', upload_to='giftcards')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    def __str__(self):
        return f'{self.title}'





