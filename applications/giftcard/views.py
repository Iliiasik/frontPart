from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from applications.apartment.paginations import LargeResultsSetPagination
from applications.giftcard.models import GiftCard
from applications.giftcard.serializers import GiftCardSerializer
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response


class GiftCardAPIView(viewsets.ModelViewSet):
    queryset = GiftCard.objects.all()
    serializer_class = GiftCardSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['owner', 'title']
    search_fields = ['title']
    ordering_fields = ['id']

