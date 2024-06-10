from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Category(models.Model):
    """
        Модель категории
    """
    name = models.CharField(primary_key=True, unique=True, max_length=50)

    def __str__(self):
        return self.name


class ApartmentAmenity(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name


class Apartment(models.Model):
    """
        Модель дома(квартиры)
    """
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField('Название', max_length=75)
    location = models.CharField('Локация', max_length=40)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    price_dollar = models.DecimalField('Цена в долларах', max_digits=10, decimal_places=2, blank=True, null=True)
    education = models.CharField('Характеристики', max_length=100)
    description = models.TextField('Описание')
    count_views = models.PositiveIntegerField('Количество просмотров', default=0)
    amenities = models.ManyToManyField(ApartmentAmenity, related_name='apartments', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    def __str__(self):
        return f'{self.title}'


class PostImage(models.Model):
    """
        Картинки к постам
    """
    image = models.ImageField(upload_to='images/')
    post = models.ForeignKey(
        Apartment, on_delete=models.CASCADE,
        related_name='images'
    )

    def __str__(self):
        return f'Image for {self.post.title}'


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', help_text='Автор комментария')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='comments', help_text='Квартира, к которому оставлен комментарий')
    body = models.TextField(help_text='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата и время создания комментария')
    updated_at = models.DateTimeField(auto_now=True, help_text='Дата и время последнего обновления комментария')

    def __str__(self):
        return f'{self.owner} -> {self.apartment.title}'


class Like(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='likes'
    )
    apartment = models.ForeignKey(
        Apartment, on_delete=models.CASCADE,
        related_name='likes'
    )
    is_like = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner} liked - {self.post.title}'


class Favorite(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='favorites'
    )
    apartment = models.ForeignKey(
        Apartment, on_delete=models.CASCADE,
        related_name='favorites'
    )
    is_favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner} liked - {self.post.title}'


class Rating(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='ratings')
    post = models.ForeignKey(
        Apartment, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner} --> {self.post.title}'



