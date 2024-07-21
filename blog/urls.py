from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('posts/', views.get_post_list, name="post_list"),
    path('posts/add/', views.create_post, name="post_add"),
    path('posts/<slug>/', views.get_post_detail, name="post_detail"),
    path('posts/<slug>/edit/', views.edit_post, name="post_edit"),
    path('posts/<slug>/remove/', views.remove_post, name="post_remove"),
]
