from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order
import qrcode
from applications.order.serializers import OrderSerializer
from django.conf import settings
import os
from .utils import send_order_email
from ..apartment.models import Apartment
from .utils import calculate_booking_price


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(user=self.request.user)

        return Response('Заказ успешно принят, но требует подтверждения.', status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def confirm_order(self, activation_code):
        order = get_object_or_404(Order, activation_code=activation_code)
        if not order.is_active:
            order.is_active = True
            order.activation_code = ''
            order.save(update_fields=['is_active', 'activation_code'])

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            data = f"Order ID: {order.id}\nTicket: {order.ticket.title}\nOwner: {order.user.username}"
            qr.add_data(data)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            img_path = os.path.join(settings.MEDIA_ROOT, f'qrcodes/order_{order.id}.png')
            img.save(img_path, format="PNG")

            email = order.user.email
            code = order.activation_code
            name = order.user.username
            send_order_email(email, code, name, img_path)

            return Response('Заказ успешно подтвержден и QR-код отправлен на вашу почту', status=status.HTTP_200_OK)
        else:
            return Response('Заказ уже был подтвержден', status=status.HTTP_400_BAD_REQUEST)


class OrderActivationAPIView(APIView):

    def get(self, request, activation_code):
        # Ищем заказ по коду активации
        order = get_object_or_404(Order, activation_code=activation_code)

        if not order:
            return Response('Заказ не найден', status=status.HTTP_404_NOT_FOUND)

        # Проверяем, не был ли заказ уже подтвержден
        if order.is_active:
            img_url = os.path.join(settings.MEDIA_URL, f'qrcodes/order_{order.id}.png')

            full_img_url = f'http://127.0.0.1:8000{img_url}'
            return Response({'message': 'Заказ уже был подтвержден', 'qr_code_image_url': full_img_url}, status=status.HTTP_400_BAD_REQUEST)

        if order.user == request.user:
            return Response({'message': 'Вы уже активировали этот заказ'}, status=status.HTTP_400_BAD_REQUEST)

        order.is_active = True
        order.save(update_fields=['is_active'])

        total_price = calculate_booking_price(
            apartment=order.apartment,
            start_date=order.start_date,
            end_date=order.end_date,
            man=order.man,
            kids=order.kids,
            animals=order.animals
        )

        ticket_id = order.apartment.id
        ticket_title = order.apartment.title
        location = order.apartment.location
        start_date = order.start_date
        end_date = order.end_date
        man = order.man
        kids = order.kids
        phone_number = "0507812318"
        message = "Для связи с нами"
        animals = "Да" if order.animals else "Нет"
        data = (f"Apartment ID: {ticket_id}"
                f"\nTitle: {ticket_title}"
                f"\nLocation: {location}"
                f"\nStart_Date: {start_date}"
                f"\nFinal_Price {total_price}"
                f"\nEnd_Date: {end_date}"
                f"\nКоличество взрослых: {man}"
                f"\nКоличество детей: {kids}"
                f"\nНаличие животных: {animals}"
                f"\nPhone: {phone_number}"
                f"\nMessage: {message}")

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        img_path = os.path.join(settings.MEDIA_ROOT, f'qrcodes/order_{order.id}.png')
        img.save(img_path, format="PNG")

        img_url = os.path.join(settings.MEDIA_URL, f'qrcodes/order_{order.id}.png')

        full_img_url = f'http://127.0.0.1:8000{img_url}'

        response_data = {
            'message': 'Успешно, Вы подтвердили покупку',
            'qr_code_image_url': full_img_url
        }

        return Response({'message': 'Заказ успешно подтвержден и QR-код отправлен на вашу почту',
                         'qr_code_image_url': full_img_url}, status=status.HTTP_200_OK)


class OrderQRCodeAPIView(generics.RetrieveAPIView):
    # Ваши представления для генерации QR-кода здесь

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if not instance.is_active:
            return Response('Заказ не был подтвержден', status=status.HTTP_400_BAD_REQUEST)

        apartment = instance.apartment

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        data = (
            f"Start Date: {instance.start_date}\n"
            f"End Date: {instance.end_date}\n"
            f"Man: {instance.man}\n"
            f"Kids: {instance.kids}\n"
            f"Animals: {instance.animals}\n"
            f"Apartment: {apartment.title}\n"
            f"Location: {apartment.location}\n"
            f"Price: {apartment.price}\n"
        )

        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        media_root = settings.MEDIA_ROOT
        img_path = os.path.join(media_root, f'qr_codes/order_{instance.id}.png')
        img.save(img_path, format="PNG")

        img_url = os.path.join(settings.MEDIA_URL[1:], f'qr_codes/order_{instance.id}.png')

        return Response({'qr_code_image_url': img_url})


class UserOrderHistoryAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
