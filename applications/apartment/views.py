from django.shortcuts import render
import logging
from rest_framework.parsers import MultiPartParser, FormParser
from django.views import View
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
import django
from applications.apartment.paginations import LargeResultsSetPagination
from applications.apartment.permissions import IsOwnerOrAdminOrReadOnly
from applications.apartment.serializers import *
from applications.apartment.models import Apartment
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import mixins
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import translation
from django.db.models import Q


logger = logging.getLogger(__name__)

from django.shortcuts import render


def main_page(request):
    category_filter = request.GET.get('category', 'All')
    search_query = request.GET.get('search', '')
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)

    apartments = Apartment.objects.all()

    if category_filter != 'All':
        apartments = apartments.filter(category__name=category_filter)

    if search_query:
        apartments = apartments.filter(
            Q(title__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if min_price:
        apartments = apartments.filter(price__gte=min_price)

    if max_price:
        apartments = apartments.filter(price__lte=max_price)

    no_apartments = apartments.count() == 0
    category_name = {
        'All': 'Доступные',
        'B&B': 'B&B',
        'Houses': 'Дома',
        'Views': 'Виды',
        'Swimming': 'Плавание',
        'Yurt': 'Юрты',
        'Campings': 'Кемпинги'
    }.get(category_filter, 'Доступные')

    context = {
        'apartments': apartments,
        'search_query': search_query,
        'no_apartments': no_apartments,
        'category_name': category_name,
    }

    return render(request, 'apartmen/main_page.html', context)
from django.shortcuts import render, get_object_or_404
def apartment_detail(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    return render(request, 'apartmen/apartment_detail.html', {'apartment': apartment})

# applications/apartment/views.py


from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages


class CategoryModelViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwnerOrAdminOrReadOnly]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class ApartmentAPIVIew(viewsets.ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['owner', 'title']
    search_fields = ['title']
    ordering_fields = ['id']  # Подключите парсеры для обработки multipart/form-data

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwnerOrAdminOrReadOnly]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        instance.count_views += 1
        instance.save(update_fields=['count_views'])
        return Response(serializer.data)

    @action(methods=['POST'], detail=True)
    def like(self, request, pk, *args, **kwargs):
        user = request.user
        like_obj, _ = Like.objects.get_or_create(owner=user, apartment_id=pk)
        like_obj.is_like = not like_obj.is_like
        like_obj.save()
        like_status = 'liked'
        if not like_obj.is_like:
            like_status = 'unliked'

        return Response({'status': like_status})

    @action(methods=['POST'], detail=True)
    def favorite(self, request, pk, *args, **kwargs):
        # logger = logging.getLogger(__name__)
        user = request.user

        favorite_obj, _ = Favorite.objects.get_or_create(owner=user, apartment_id=pk)
        favorite_obj.is_favorite = not favorite_obj.is_favorite
        favorite_obj.save()
        status = 'favorites'
        if not favorite_obj.is_favorite:
            status = 'not favorite'

        return Response({'status': status})

    @action(methods=['POST'], detail=True)
    def rating(self, request, pk, *args, **kwargs):
        user = request.user
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rating_obj, _ = Rating.objects.get_or_create(owner=request.user, post_id=pk)
        rating_obj.rating = serializer.data['rating']
        rating_obj.save()
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def get_recommendations(self, request, *args, **kwargs):
        user = request.user

        liked_apartment_ids = user.likes.filter(is_like=True).values_list('apartment_id', flat=True)

        recommended_apartments = Apartment.objects.filter(likes__is_like=True).exclude(id__in=liked_apartment_ids)

        recommended_apartments = recommended_apartments.annotate(like_count=Count('likes'))

        recommended_apartments = recommended_apartments.order_by('-like_count')

        serializer = ApartmentSerializer(recommended_apartments, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        logger.info(f"Apartment created by user {self.request.user.username}: {serializer.data}")

    def perform_update(self, serializer):
        instance = self.get_object()
        serializer.save()
        logger.info(f"Apartment updated by user {self.request.user.username}: {serializer.data}")

    def perform_destroy(self, instance):
        logger.info(f"Apartment deleted by user {self.request.user.username}: {instance}")
        instance.delete()


class CommentModelViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ImageModelViewSet(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]


class UserActionHistoryAPIView(APIView):
    def get(self, request, name):
        if name == "like":
            likes = Like.objects.filter(owner=request.user)

            liked_posts = []

            for like in likes:
                post = like.apartment

                post_data = {
                    "id": post.id,
                    "title": post.title,
                    "liked_at": like.created_at,
                }
                liked_posts.append(post_data)

            return Response({"liked_posts": liked_posts})

        elif name == "favorite":
            favorites = Favorite.objects.filter(owner=request.user)

            favorite_posts = []

            for favorite in favorites:
                post = favorite.apartment

                post_data = {
                    "id": post.id,
                    "title": post.title,
                    "favorited_at": favorite.created_at,
                }
                favorite_posts.append(post_data)

            return Response({"favorite_posts": favorite_posts})

        elif name == "rating":

            ratings = Rating.objects.filter(owner=request.user)

            rated_posts = []

            for rating in ratings:
                post = rating.post

                post_data = {
                    "id": post.id,
                    "title": post.title,
                    "rating": rating.rating,
                    "rated_at": rating.created_at,
                }
                rated_posts.append(post_data)

            return Response({"rated_posts": rated_posts})

        elif name == "comment":

            comments = Comment.objects.filter(owner=request.user)

            commented_posts = []

            for comment in comments:
                post = comment.apartment
                post_data = {
                    "id": post.id,
                    "title": post.title,
                    "commented_at": comment.created_at,
                }
                commented_posts.append(post_data)

            return Response({"commented_posts": commented_posts})

        return Response("Invalid action name", status=status.HTTP_400_BAD_REQUEST)



