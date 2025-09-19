from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, DropOffPoint, Submission, Reward

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'pontos', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Pontuação', {'fields': ('pontos',)}),
    )

@admin.register(DropOffPoint)
class DropOffPointAdmin(admin.ModelAdmin):
    list_display = ('nome', 'endereco', 'latitude', 'longitude')
    search_fields = ('nome', 'endereco')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'points_awarded', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'description')

@admin.register(Reward)
class RewardAdmin(admin.ModelAdmin):
    list_display = ('title', 'points_required')
    search_fields = ('title', 'description')