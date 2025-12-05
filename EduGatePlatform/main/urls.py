from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path("classes/", views.schoolclass_list, name="schoolclass_list"),
    path("create-class/", views.create_class, name="create_class"),
    path("classes/<int:class_id>/edit/", views.schoolclass_update, name="schoolclass_update"),
    path("classes/<int:class_id>/delete/", views.schoolclass_delete, name="schoolclass_delete"),
    path("announcements/", views.announcement_list, name="announcement_list"),
    path("announcements/add/", views.add_announcement, name="add_announcement"),
    path("announcements/<int:ann_id>/edit/", views.announcement_update, name="announcement_update"),
    path("announcements/<int:ann_id>/delete/", views.announcement_delete, name="announcement_delete"),
]