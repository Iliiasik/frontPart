from django.db.models import Count
from rest_framework import serializers
# from applications.apartment.utils import send_order_email
from applications.apartment.models import *
from django.db import connection

from applications.pars_curens.models import DollarRate


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Like
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Comment
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Rating
        fields = ('rating',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Favorite
        fields = '__all__'


class PostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImage
        fields = '__all__'


class PostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImage
        fields = '__all__'


class ApartmentAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentAmenity
        fields = '__all__'


class ApartmentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    amenities = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    images = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Apartment
        fields = '__all__'

    def create(self, validated_data):
        apartment = Apartment.objects.create(**validated_data)
        request = self.context.get('request')
        files = request.FILES

        try:
            dollar_rate = DollarRate.objects.latest('id')
            usd_rate = dollar_rate.rate
        except DollarRate.DoesNotExist:
            usd_rate = 1  # Default rate in case no DollarRate instances exist

        validated_data['price_dollar'] = validated_data['price'] / usd_rate  # Calculate price_dollar
        apartment = Apartment.objects.create(**validated_data)

        image_objects = []
        for file in files.getlist('images'):
            PostImage.objects.create(apartment=apartment, image=file)
        PostImage.objects.bulk_create(image_objects)

        return apartment

    def get_amenities(self, instance):
        amenities_queryset = instance.amenities.all()
        amenities_dict = {}

        for amenity in amenities_queryset:
            if amenity.parent:
                parent_name = amenity.parent.name
                if parent_name not in amenities_dict:
                    amenities_dict[parent_name] = []
                amenities_dict[parent_name].append(amenity.name)
            else:
                if amenity.name not in amenities_dict:
                    amenities_dict[amenity.name] = []

        return amenities_dict

    def get_amenities_recursive(self, queryset):
        amenities_list = []
        for amenity in queryset:
            amenities_list.append(amenity.name)
            children = amenity.children.all()
            if children:
                children_list = self.get_amenities_recursive(children)
                amenities_list.extend(children_list)
        return amenities_list

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        # Получаем количество лайков
        like_count = instance.likes.filter(is_like=True).count()
        rep['like_count'] = like_count

        # Получаем средний рейтинг
        ratings = instance.ratings.all()
        rating_result = sum(rating.rating for rating in ratings)
        if ratings.exists():
            average_rating = rating_result / ratings.count()
        else:
            average_rating = 0
        rep['rating'] = average_rating

        # Попробуем получить последний сохраненный курс доллара
        try:
            dollar_rate = DollarRate.objects.latest('id')
            usd_rate = dollar_rate.rate
            rep['dollar_rate'] = usd_rate  # Добавляем поле с курсом доллара в JSON
        except DollarRate.DoesNotExist:
            usd_rate = None
            rep['dollar_rate'] = 'не найдено'  # Сообщение "не найдено" вместо курса

        return rep

