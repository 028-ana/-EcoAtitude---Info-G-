from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Submission, DropOffPoint, Reward
from .serializers import SubmissionCreateSerializer, SubmissionSerializer
from .gemini_client import GeminiClient

# ========================
# Usuários
# ========================
class UserListView(ListView):
    model = User
    template_name = 'core/user_list.html'
    context_object_name = 'users'

class UserDetailView(DetailView):
    model = User
    template_name = 'core/user_detail.html'
    context_object_name = 'user'

# ========================
# Pontos de coleta
# ========================
class DropOffPointListView(ListView):
    model = DropOffPoint
    template_name = 'core/dropoffpoint_list.html'
    context_object_name = 'dropoff_points'

# ========================
# Submissions
# ========================
class SubmissionListView(ListView):
    model = Submission
    template_name = 'core/submission_list.html'
    context_object_name = 'submissions'

class SubmissionDetailView(DetailView):
    model = Submission
    template_name = 'core/submission_detail.html'
    context_object_name = 'submission'

@api_view(['POST'])
def create_submission(request):
    serializer = SubmissionCreateSerializer(data=request.data)
    if serializer.is_valid():
        submission = serializer.save(user=request.user)
        try:
            gemini = GeminiClient()
            is_valid, message = gemini.validate_submission_image(
                submission.image.path,
                submission.description or ""
            )
        except Exception as e:
            print(f"Erro no Gemini Client, usando simulador: {e}")
            from .gemini_client_simple import SimpleGeminiClient
            simple_gemini = SimpleGeminiClient()
            is_valid, message = simple_gemini.validate_submission_image(
                submission.image.path,
                submission.description or ""
            )
        
        submission.status = 'approved' if is_valid else 'rejected'
        submission.validation_message = message
        
        # Pontuação
        if is_valid:
            import re
            points_match = re.search(r'\+(\d+)', message)
            submission.points_awarded = int(points_match.group(1)) if points_match else 50
            request.user.pontos += submission.points_awarded
            request.user.save()
        else:
            submission.points_awarded = 0
        
        submission.save()
        response_data = SubmissionSerializer(submission).data
        response_data['validation_message'] = message
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ========================
# Rewards
# ========================
class RewardListView(ListView):
    model = Reward
    template_name = 'recompensas.html'
    context_object_name = 'rewards'

@api_view(['POST'])
def redeem_reward(request, reward_id):
    reward = get_object_or_404(Reward, id=reward_id)
    if request.user.pontos >= reward.cost:
        request.user.pontos -= reward.cost
        request.user.save()
        return Response({"message": "Reward redeemed successfully"}, status=status.HTTP_200_OK)
    return Response({"message": "Insufficient points"}, status=status.HTTP_400_BAD_REQUEST)

# ========================
# Registro e Login
# ========================
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('user-list')
    return render(request, 'core/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('user-list')
    return render(request, 'core/login.html')

def home_view(request):
    return render(request, "home.html")

def cadastrar_descarte(request):
    if request.method == 'POST':
        # Aqui você processa o formulário de cadastro de descarte
        # Exemplo:
        # descricao = request.POST.get('descricao')
        # drop_off_point = request.POST.get('drop_off_point')
        # Submission.objects.create(user=request.user, description=descricao, drop_off_point_id=drop_off_point)
        return redirect('home')  # ou outra página após cadastro

    # Se GET, apenas renderiza o formulário
    return render(request, 'cadastrar_descarte.html')
