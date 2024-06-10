from django.contrib.auth import get_user_model
from rest_framework import serializers

from applications.spam.models import Contact

User = get_user_model()


class ContactSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)

    class Meta:
        model = Contact
        fields = '__all__'

    def create(self, validated_data):
        if Contact.objects.filter(email=validated_data.get('email')).exists():
            raise serializers.ValidationError('Вы уже подписались')
        return super().create(validated_data)





