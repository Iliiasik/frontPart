from django.utils.crypto import get_random_string
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .utils import send_activation_code
from applications.account.serializers import *
from rest_framework import generics
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


User = get_user_model()

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages

# def create_apartment(request):
#     if request.method == 'POST':
#         # Получаем данные из запроса
#         title = request.POST.get('title')
#         category_id = request.POST.get('category_id')
#         location = request.POST.get('location')
#         price = request.POST.get('price')
#         price_dollar = request.POST.get('price_dollar')
#         education = request.POST.get('education')
#         description = request.POST.get('description')
#
#         # Создаем новое объявление
#         new_apartment = Apartment.objects.create(
#             title=title,
#             category_id=category_id,
#             location=location,
#             price=price,
#             price_dollar=price_dollar,
#             education=education,
#             description=description
#         )
#
#         # Возвращаем успешный ответ
#         return JsonResponse({'success': True})
#     else:
#         # Возвращаем ошибку, если метод запроса не POST
#         return JsonResponse({'error': 'Метод запроса должен быть POST'})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile_view')  # Перенаправление на страницу профиля после успешного входа
        else:
            messages.error(request, 'Неверный адрес электронной почты или пароль.')

    return render(request, 'apartmen/login.html')

def profile_view(request):
    return render(request, 'apartmen/profile.html')


def register_view(request):
    return render(request, 'apartmen/register.html')

def register_done(request):
    return render(request, 'apartmen/registration_success.html')



class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Вы успешно зарегистрировались. Вам отправлено письмо на почту с активацией', status=201)


class ActivationAPIView(APIView):
    def get(self, request, activation_code):
        user = get_object_or_404(User, activation_code=activation_code)
        if user.is_active:
            message = "Ваш аккаунт уже активирован."
        else:
            user.is_active = True
            user.activation_code = ''
            user.save(update_fields=['is_active', 'activation_code'])
            message = "Ваш аккаунт успешно активирован."
        return render(request, 'apartmen/activation.html', {'message': message})
class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializers = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializers.is_valid(raise_exception=True)
        serializers.set_new_password()
        return Response('Пароль изменен', status=200)


class ForgotPasswordAPIView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_code()
        return Response('Вам отправлено на эту почту письмо с кодом для восстановления пароля ', status=200)


class ForgotPasswordConfirmAPIView(APIView):
    def post(self, request):
        serializer = ForgotPasswordConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Пароль успешно обновлен', status=200)


@api_view(['GET'])
def send_mail_view(request):
    from applications.account.tasks import send_test_message
    send_test_message.delay()
    return Response('Отправлено')


class OwnerUserApartmentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Передаем данные из запроса в сериализатор
        serializer = RegisterOwnerApartmentSerializer(data=request.data)

        if serializer.is_valid():
            # Создаем нового пользователя-владельца квартиры
            user = User.objects.get(pk=request.user.pk)  # Получаем текущего пользователя
            user.where_studied = serializer.validated_data.get('where_studied')
            user.profession = serializer.validated_data.get('profession')
            user.interesting_fact = serializer.validated_data.get('interesting_fact')
            user.hobbies = serializer.validated_data.get('hobbies')
            user.languages_spoken = serializer.validated_data.get('languages_spoken')
            user.location = serializer.validated_data.get('location')
            user.description = serializer.validated_data.get('description')
            user.is_owner = True
            user.save()

            return Response({'message': 'Поздравляю Вы теперь являетесь Хозяином!'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInfoAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer  # Замените на ваш сериализатор пользователя

    def get_object(self):
        # Возвращает текущего пользователя
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class OwnerApartmentInfoByEmailView(generics.RetrieveAPIView):
    serializer_class = OwnerApartmentProfileSerializer

    def get(self, request, *args, **kwargs):
        email = self.kwargs.get('email')  # Получаем адрес электронной почты из URL

        try:
            owner_apartment_user = User.objects.get(email=email, is_owner=True)
            serializer = self.serializer_class(owner_apartment_user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'Владелец квартиры с указанным email не найден.'}, status=status.HTTP_404_NOT_FOUND)

@login_required
def home(request):
    return render(request, 'main_page.html')