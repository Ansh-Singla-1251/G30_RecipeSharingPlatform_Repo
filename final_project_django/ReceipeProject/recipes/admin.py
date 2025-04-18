from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import mark_safe
from .models import User, Recipe, Contact

# Custom UserAdmin
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'name', 'mobile', 'role', 'is_admin', 'is_staff', 'is_active')
    list_filter = ('is_admin', 'is_staff', 'is_active', 'role')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'mobile', 'role', 'is_admin')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'mobile', 'role', 'is_admin', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'name', 'mobile')
    ordering = ('email',)
    filter_horizontal = ()  # Override default to remove 'groups' and 'user_permissions'

# Custom RecipeAdmin
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_vegetarian', 'price', 'user')
    list_filter = ('category', 'is_vegetarian', 'user')
    search_fields = ('title', 'description', 'category')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'ingredients', 'instructions', 'user')
        }),
        ('Media', {
            'fields': ('image_filename', 'image_preview', 'youtube_link')
        }),
        ('Details', {
            'fields': ('category', 'occasion', 'is_vegetarian', 'price')
        }),
    )
    filter_horizontal = ('wishlist',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image_filename:
            return mark_safe(f'<img src="/static/images/{obj.image_filename}" width="100" />')
        return '(No image)'

# Default Contact admin
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')

# Register User with CustomUserAdmin
admin.site.register(User, CustomUserAdmin)