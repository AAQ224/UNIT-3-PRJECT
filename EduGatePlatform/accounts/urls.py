from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('student/subjects/', views.student_subjects, name='student_subjects'),
    path('student/grades/', views.student_grades, name='student_grades'),
    path('parent/child/<int:student_id>/grades/', views.parent_child_grades, name='parent_child_grades'),
    path("link-parent-children/", views.link_parent_children, name="link_parent_children"),
    path("manage-parent-links/", views.manage_parent_links, name="manage_parent_links"),
    path("manage-parent-links/<int:relation_id>/delete/", views.delete_parent_link, name="delete_parent_link"),
    path("manage-users/", views.manage_users, name="manage_users"),
    path("manage-users/<int:user_id>/edit/", views.edit_user, name="edit_user"),
    path("manage-users/<int:user_id>/delete/", views.delete_user, name="delete_user"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html",
            email_template_name="accounts/password_reset_email.txt",
            subject_template_name="accounts/password_reset_subject.txt",
            success_url=reverse_lazy("accounts:password_reset_done"),
        ),
        name="password_reset",
    ),

    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_done",
    ),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),

    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
