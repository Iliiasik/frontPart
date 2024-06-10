from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Category, Apartment, Comment, Like, Favorite, Rating, ApartmentAmenity, PostImage
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Apartment, Category, Like
from .serializers import ApartmentSerializer
from ..account.models import CustomUser

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Apartment
from .serializers import ApartmentSerializer
from applications.account.models import CustomUser
from .models import Apartment, Like, Category

User = get_user_model()


class CategoryModelTest(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(name='Test Category')
        self.assertEqual(category.name, 'Test Category')


class ApartmentAmenityModelTest(TestCase):
    def test_amenity_creation(self):
        amenity = ApartmentAmenity.objects.create(name='Amenity Name')
        self.assertEqual(amenity.name, 'Amenity Name')


class ApartmentModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        category = Category.objects.create(name='Test Category')
        self.apartment = Apartment.objects.create(
            owner=user,
            category=category,
            title='Test Apartment',
            location='Test Location',
            price=100.00,
            education='Test Education',
            description='Test Description'
        )

    def test_apartment_creation(self):
        self.assertEqual(self.apartment.title, 'Test Apartment')
        self.assertEqual(self.apartment.location, 'Test Location')
        self.assertEqual(self.apartment.price, 100.00)
        self.assertEqual(self.apartment.education, 'Test Education')
        self.assertEqual(self.apartment.description, 'Test Description')


class CommentModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        category = Category.objects.create(name='Test Category')
        apartment = Apartment.objects.create(
            owner=user,
            category=category,
            title='Test Apartment',
            location='Test Location',
            price=100.00,
            education='Test Education',
            description='Test Description'
        )
        self.comment = Comment.objects.create(owner=user, apartment=apartment, body='Test Comment')

    def test_comment_creation(self):
        self.assertEqual(self.comment.owner.email, 'testuser@example.com')
        self.assertEqual(self.comment.apartment.title, 'Test Apartment')
        self.assertEqual(self.comment.body, 'Test Comment')


class LikeModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        category = Category.objects.create(name='Test Category')
        apartment = Apartment.objects.create(
            owner=user,
            category=category,
            title='Test Apartment',
            location='Test Location',
            price=100.00,
            education='Test Education',
            description='Test Description'
        )
        self.like = Like.objects.create(owner=user, apartment=apartment, is_like=True)

    def test_like_creation(self):
        self.assertEqual(self.like.owner.email, 'testuser@example.com')
        self.assertEqual(self.like.apartment.title, 'Test Apartment')
        self.assertTrue(self.like.is_like)


class FavoriteModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        category = Category.objects.create(name='Test Category')
        apartment = Apartment.objects.create(
            owner=user,
            category=category,
            title='Test Apartment',
            location='Test Location',
            price=100.00,
            education='Test Education',
            description='Test Description'
        )
        self.favorite = Favorite.objects.create(owner=user, apartment=apartment, is_favorite=True)

    def test_favorite_creation(self):
        self.assertEqual(self.favorite.owner.email, 'testuser@example.com')
        self.assertEqual(self.favorite.apartment.title, 'Test Apartment')
        self.assertTrue(self.favorite.is_favorite)


class RatingModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        category = Category.objects.create(name='Test Category')
        apartment = Apartment.objects.create(
            owner=user,
            category=category,
            title='Test Apartment',
            location='Test Location',
            price=100.00,
            education='Test Education',
            description='Test Description'
        )
        self.rating = Rating.objects.create(owner=user, post=apartment, rating=5)

    def test_rating_creation(self):
        self.assertEqual(self.rating.owner.email, 'testuser@example.com')
        self.assertEqual(self.rating.post.title, 'Test Apartment')
        self.assertEqual(self.rating.rating, 5)


class PostImageModelTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        category = Category.objects.create(name='Test Category')
        apartment = Apartment.objects.create(
            owner=user,
            category=category,
            title='Test Apartment',
            location='Test Location',
            price=100.00,
            education='Test Education',
            description='Test Description'
        )
        self.post_image = PostImage.objects.create(image='image.jpg', post=apartment)

    def test_post_image_creation(self):
        self.assertEqual(self.post_image.image, 'image.jpg')
        self.assertEqual(self.post_image.post.title, 'Test Apartment')


class RecommendationSystemTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='testuser@gmail.com', password='testpassword')
        self.client = APIClient()
        category1 = Category.objects.create(name='Category 1')
        category2 = Category.objects.create(name='Category 2')

        self.apartment1 = Apartment.objects.create(
            title='Apartment 1',
            location='Location 1',
            price=1000.00,
            description='Description for Apartment 1',
            owner=self.user,
            category=category1
        )

        self.apartment2 = Apartment.objects.create(
            title='Apartment 2',
            location='Location 2',
            price=1200.00,
            description='Description for Apartment 2',
            owner=self.user,
            category=category2
        )

        self.like1 = Like.objects.create(owner=self.user, apartment=self.apartment1, is_like=True)
        self.like2 = Like.objects.create(owner=self.user, apartment=self.apartment2, is_like=True)

    def test_get_recommendations(self):
        url = '/api/v1/apartment/recommendations/'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        recommended_apartments = Apartment.objects.exclude(id__in=[self.apartment1.id, self.apartment2.id])
        serializer = ApartmentSerializer(recommended_apartments, many=True)
        self.assertEqual(response.data, serializer.data)
