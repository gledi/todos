from django.urls import path

from . import views

urlpatterns = [
    path("", views.show_posts, name="post_list"),
    path("add/", views.create_post, name="post_add"),
    path("<int:pk>/", views.show_post, name="post_detail"),
]