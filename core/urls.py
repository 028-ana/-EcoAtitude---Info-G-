from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import redeem_reward

urlpatterns = [
    path('', views.home.html, name='home'),

    # users
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),

    # auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # dropoff points
    path('dropoff-points/', views.DropOffPointListView.as_view(), name='dropoff-point-list'),

    # submissions
    path('submissions/', views.SubmissionListView.as_view(), name='submission-list'),
    path('submissions/<int:pk>/', views.SubmissionDetailView.as_view(), name='submission-detail'),
    path('submissions/create/', views.create_submission, name='submission-create'),

    # rewards
    path('rewards/', views.RewardListView.as_view(), name='reward-list'),
    path('reward/<int:reward_id>/redeem/', redeem_reward, name='redeem-reward'),

    # formulário de descarte
    path('descarte/cadastrar/', views.cadastrar_descarte, name='cadastrar_descarte'),
]
