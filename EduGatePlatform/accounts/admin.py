from django.contrib import admin
from .models import Profile, ParentStudentRelation

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'role', 'national_id')
    list_filter = ('role',)
    search_fields = ('full_name', 'user__username', 'national_id')


@admin.register(ParentStudentRelation)
class ParentStudentRelationAdmin(admin.ModelAdmin):
    list_display = ('parent', 'student')
    search_fields = ('parent__username', 'student__username')
