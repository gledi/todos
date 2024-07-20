from django.urls import path

from . import views

urlpatterns = [
    path("", views.show_tasks, name="task_list"),
    path("add/", views.create_task, name="task_add"),
    path("<int:pk>/", views.show_task, name="task_detail"),
    path("<int:pk>/update/", views.update_task, name="task_update"),
    path("<int:pk>/delete/", views.delete_task, name="task_delete"),
]
