from rest_framework.viewsets import ModelViewSet, GenericViewSet
from applications.spam.models import Contact
from applications.spam.serializers import ContactSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins


class ContactAPIView(mixins.CreateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(email=self.request.user.email)



