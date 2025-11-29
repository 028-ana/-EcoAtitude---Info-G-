from django.urls import path
from . import views
from .views import SubmissionDeleteView

urlpatterns = [
    path('', views.home_view, name='home'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dropoff-points/', views.DropOffPointListView.as_view(), name='dropoff-point-list'),
    path('submissions/', views.SubmissionListView.as_view(), name='submission-list'),
    path('submissions/<int:pk>/', views.SubmissionDetailView.as_view(), name='submission-detail'),
    path('submissions/create/', views.create_submission, name='submission-create'),
    path('submissions/<int:pk>/delete/', SubmissionDeleteView.as_view(), name='submission-delete'),
    path('rewards/', views.RewardListView.as_view(), name='reward-list'),
    path('rewards/<int:reward_id>/redeem/', views.redeem_reward, name='redeem-reward'),
    path('descarte/cadastrar/', views.cadastrar_descarte, name='cadastrar-descarte'),
]
