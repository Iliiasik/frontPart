from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Order
from .utils import send_order_email

User = get_user_model()


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user  # Замените 'user' на 'owner'
        # Замените 'user' на 'owner'
        instance = super().create(validated_data)
        instance.create_activation_code()
        send_order_email(request.user.email, instance.activation_code, request.user.username)
        return instance





