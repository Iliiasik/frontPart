from django.db.models import Count
from rest_framework import serializers

from applications.helpcenter.models import *


class QuestionsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Questions
        fields = '__all__'


class ComplaintSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Complaint
        fields = '__all__'


class SendProblemSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = SendProblem
        fields = '__all__'

