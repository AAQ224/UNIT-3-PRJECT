from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path("classes/", views.schoolclass_list, name="schoolclass_list"),
    path("create-class/", views.create_class, name="create_class"),
    path("classes/<int:class_id>/edit/", views.schoolclass_update, name="schoolclass_update"),
    path("classes/<int:class_id>/delete/", views.schoolclass_delete, name="schoolclass_delete"),
    path("add-announcement/", views.add_announcement, name="add_announcement"),
]