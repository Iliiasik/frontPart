from django.db import models
from django.contrib.auth import get_user_model

from applications.apartment.models import Apartment

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders'
    )
    apartment = models.ForeignKey(
        Apartment, on_delete=models.CASCADE, related_name='orders'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    man = models.PositiveIntegerField()
    kids = models.PositiveIntegerField()
    animals = models.BooleanField()
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата и время создания заказа')
    is_active = models.BooleanField(default=False, help_text='Флаг активности заказа')
    activation_code = models.CharField(max_length=40, blank=True, help_text='Код активации заказа')

    def create_activation_code(self):
        """
        Метод для создания и сохранения кода активации заказа.
        """
        import uuid
        code = str(uuid.uuid4())
        self.activation_code = code
        self.save()

    def __str__(self):
        return (f"Order for "
                f"{self.user.username}, "
                f"{self.start_date}, "
                f"{self.end_date}, "
                f"{self.street}, "
                f"{self.city}, "
                f"{self.country}")


