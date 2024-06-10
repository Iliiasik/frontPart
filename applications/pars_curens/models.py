from django.db import models


class DollarRate(models.Model):
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Rate: {self.rate} on {self.date}'
