from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Questions(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='questions')
    body = models.TextField('Вопрос пользователя')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата и время создания')
    updated_at = models.DateTimeField(auto_now=True, help_text='Дата и время последнего обновления')

    def __str__(self):
        return f"{self.user.username}: {self.body[:50]}"


class Complaint(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='complaints')
    body = models.TextField('Жалоба пользователя')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата и время создания')
    updated_at = models.DateTimeField(auto_now=True, help_text='Дата и время последнего обновления')

    def __str__(self):
        return f"{self.user.username}: {self.body[:50]}"


class SendProblem(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='send_problems')
    body = models.TextField('Сообщения об проблеме')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата и время создания')
    updated_at = models.DateTimeField(auto_now=True, help_text='Дата и время последнего обновления')

    def __str__(self):
        return f"{self.user.username}: {self.body[:50]}"


