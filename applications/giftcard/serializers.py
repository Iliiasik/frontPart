from rest_framework import serializers
from applications.apartment.models import *
from applications.giftcard.models import *


class GiftCardSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = GiftCard
        fields = '__all__'

