from django.contrib import admin

from .models import User, Post


class PostInline(admin.TabularInline):
    model = Post


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name',)
    inlines = [PostInline]
