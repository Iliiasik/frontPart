from django.db import models


class Contact(models.Model):
    """
        Модель для подписки на рассылку
    """
    email = models.EmailField('Почта', unique=True, help_text='Введите почту пользователя')

    def __str__(self):
        return f'{self.email}'


