from django.contrib import admin
from django.utils.html import mark_safe
from applications.apartment.models import Comment, Apartment, Category, ApartmentAmenity, PostImage

class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="150" height="150" />')
        return "No Image"

    image_tag.short_description = 'Image'

@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'like_count']
    list_filter = ['owner']
    search_fields = ['title']
    inlines = [PostImageInline]

    def like_count(self, obj):
        return obj.likes.filter(is_like=True).count()

@admin.register(ApartmentAmenity)
class ApartmentAmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(PostImage)
